#!/usr/bin/env python3
"""Run one read-only OpenCode probe and emit only the final JSON object.

The wrapper talks to an already-running isolated OpenCode server.  It records
only observable activation evidence (successful Skill-tool calls and file-read
paths), never model reasoning or a raw conversation transcript.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from collections import Counter
from pathlib import Path
from typing import Any


SKILL_FILE = re.compile(
    r"(?i)(?:^|[\\/])(frontier-[a-z0-9-]+)[\\/]SKILL\.md$"
)
DOCTRINE_FILE = re.compile(
    r"(?i)(?:^|[\\/])ENGINEERING_JUDGMENT\.md$"
)


def _request_json(
    method: str,
    url: str,
    *,
    body: dict[str, Any] | None = None,
    timeout: float,
) -> Any:
    data = None
    headers = {"Accept": "application/json"}
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = response.read()
    except urllib.error.HTTPError as exc:
        excerpt = exc.read().decode("utf-8", errors="replace")[-4096:]
        raise RuntimeError(f"HTTP {exc.code} for {url}: {excerpt}") from exc
    if not payload:
        return None
    return json.loads(payload.decode("utf-8"))


def _extract_json_object(text: str) -> dict[str, Any]:
    value = text.strip()
    fenced = re.fullmatch(r"```(?:json)?\s*(\{.*\})\s*```", value, re.I | re.S)
    if fenced:
        value = fenced.group(1)
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        start = value.find("{")
        end = value.rfind("}")
        if start < 0 or end <= start:
            raise ValueError("assistant final message did not contain a JSON object")
        parsed = json.loads(value[start : end + 1])
    if isinstance(parsed, list) and all(isinstance(row, dict) for row in parsed):
        parsed = {"cases": parsed}
    if not isinstance(parsed, dict):
        raise ValueError("assistant final JSON must be an object")
    return parsed


def _tool_input(part: dict[str, Any]) -> dict[str, Any]:
    state = part.get("state")
    if not isinstance(state, dict):
        return {}
    value = state.get("input")
    return value if isinstance(value, dict) else {}


def _tool_succeeded(part: dict[str, Any]) -> bool:
    state = part.get("state")
    return isinstance(state, dict) and state.get("status") in {
        "completed",
        "success",
        "succeeded",
    }


def _has_final_assistant_text(messages: Any) -> bool:
    if not isinstance(messages, list):
        return False
    for message in reversed(messages):
        if not isinstance(message, dict):
            continue
        info = message.get("info")
        if not isinstance(info, dict) or info.get("role") != "assistant":
            continue
        parts = message.get("parts")
        if not isinstance(parts, list):
            continue
        has_text = any(
            isinstance(part, dict)
            and part.get("type") == "text"
            and isinstance(part.get("text"), str)
            and bool(part["text"].strip())
            for part in parts
        )
        if has_text and info.get("finish") in {
            "stop",
            "completed",
            "end_turn",
            "length",
        }:
            return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint", required=True)
    parser.add_argument("--cwd", type=Path, required=True)
    parser.add_argument("--trace-dir", type=Path, required=True)
    parser.add_argument("--timeout", type=float, default=180.0)
    parser.add_argument("--model", default="opencode/big-pickle")
    parser.add_argument("--agent", default="build")
    args = parser.parse_args()

    prompt = sys.stdin.read()
    if not prompt.strip():
        raise SystemExit("stdin prompt is empty")

    endpoint = args.endpoint.rstrip("/")
    provider_id, separator, model_id = args.model.partition("/")
    if not separator or not provider_id or not model_id:
        raise SystemExit("--model must be provider/model")

    health = _request_json("GET", f"{endpoint}/global/health", timeout=args.timeout)
    if not isinstance(health, dict) or not health.get("healthy"):
        raise SystemExit(f"OpenCode server is not healthy: {health!r}")

    args.trace_dir.mkdir(parents=True, exist_ok=True)
    run_id = f"{int(time.time() * 1000)}-{uuid.uuid4().hex[:8]}"
    query = urllib.parse.urlencode({"directory": str(args.cwd.resolve())})
    session = _request_json(
        "POST",
        f"{endpoint}/session?{query}",
        body={"title": f"FrontierLoop activation {run_id}"},
        timeout=args.timeout,
    )
    if not isinstance(session, dict) or not isinstance(session.get("id"), str):
        raise SystemExit(f"OpenCode did not create a session: {session!r}")
    session_id = session["id"]

    timed_out = False
    request_state: dict[str, Any] = {}
    try:
        def send_prompt() -> None:
            try:
                request_state["response"] = _request_json(
                    "POST",
                    f"{endpoint}/session/{urllib.parse.quote(session_id)}/message?{query}",
                    body={
                        "model": {"providerID": provider_id, "modelID": model_id},
                        "agent": args.agent,
                        "parts": [{"type": "text", "text": prompt}],
                    },
                    timeout=args.timeout + 15.0,
                )
            except Exception as exc:
                request_state["error"] = f"{type(exc).__name__}: {exc}"

        sender = threading.Thread(target=send_prompt, daemon=True)
        sender.start()
        deadline = time.monotonic() + args.timeout
        messages: Any = []
        while time.monotonic() < deadline:
            messages = _request_json(
                "GET",
                f"{endpoint}/session/{urllib.parse.quote(session_id)}/message?{query}",
                timeout=min(args.timeout, 15.0),
            )
            if _has_final_assistant_text(messages):
                break
            if not sender.is_alive() and request_state.get("error"):
                break
            time.sleep(0.25)
        else:
            timed_out = True
            try:
                _request_json(
                    "POST",
                    f"{endpoint}/session/{urllib.parse.quote(session_id)}/abort?{query}",
                    timeout=15.0,
                )
            except Exception:
                pass
        sender.join(timeout=2.0)
        messages = _request_json(
            "GET",
            f"{endpoint}/session/{urllib.parse.quote(session_id)}/message?{query}",
            timeout=args.timeout,
        )
        if not isinstance(messages, list):
            raise RuntimeError("OpenCode messages response is not an array")

        part_counts: Counter[str] = Counter()
        successful_skill_reads: set[str] = set()
        attempted_skill_reads: set[str] = set()
        successful_read_paths: set[str] = set()
        tool_sequence: list[dict[str, Any]] = []
        doctrine_read_succeeded = False
        final_text = ""

        for message in messages:
            if not isinstance(message, dict):
                continue
            info = message.get("info")
            if not isinstance(info, dict) or info.get("role") != "assistant":
                continue
            parts = message.get("parts")
            if not isinstance(parts, list):
                continue
            for part in parts:
                if not isinstance(part, dict):
                    continue
                part_type = str(part.get("type", "unknown"))
                part_counts[part_type] += 1
                if part_type == "text" and isinstance(part.get("text"), str):
                    final_text = part["text"]
                if part_type != "tool":
                    continue
                tool = part.get("tool")
                tool_input = _tool_input(part)
                succeeded = _tool_succeeded(part)
                sequence_input: dict[str, Any] = {}
                if tool == "skill" and isinstance(tool_input.get("name"), str):
                    sequence_input["name"] = tool_input["name"]
                if tool == "read":
                    path_value = tool_input.get("filePath") or tool_input.get("path")
                    if isinstance(path_value, str):
                        sequence_input["path"] = path_value
                tool_sequence.append(
                    {
                        "tool": tool,
                        "succeeded": succeeded,
                        "input": sequence_input,
                    }
                )
                if tool == "skill":
                    name = tool_input.get("name")
                    if isinstance(name, str) and name.startswith("frontier-"):
                        attempted_skill_reads.add(name)
                        if succeeded:
                            successful_skill_reads.add(name)
                elif tool == "read":
                    path = tool_input.get("filePath") or tool_input.get("path")
                    if isinstance(path, str):
                        normalized = str(Path(path))
                        if succeeded:
                            successful_read_paths.add(normalized)
                        skill_match = SKILL_FILE.search(path)
                        if skill_match:
                            attempted_skill_reads.add(skill_match.group(1).lower())
                            if succeeded:
                                successful_skill_reads.add(skill_match.group(1).lower())
                        if DOCTRINE_FILE.search(path) and succeeded:
                            doctrine_read_succeeded = True

        final_object: dict[str, Any] | None = None
        canonical_final = ""
        final_parse_error: str | None = None
        try:
            final_object = _extract_json_object(final_text)
            canonical_final = json.dumps(
                final_object, sort_keys=True, ensure_ascii=True, separators=(",", ":")
            )
        except Exception as exc:
            final_parse_error = f"{type(exc).__name__}: {exc}"
        trace = {
            "schema": "frontierloop-opencode-activation-trace/v1",
            "run_id": run_id,
            "server_version": health.get("version"),
            "model": args.model,
            "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
            "final_sha256": hashlib.sha256(final_text.encode("utf-8")).hexdigest(),
            "final_text_present": bool(final_text.strip()),
            "final_json_valid": final_object is not None,
            "final_parse_error": final_parse_error,
            "part_counts": dict(sorted(part_counts.items())),
            "tool_sequence": tool_sequence,
            "execution_skill_reads": sorted(attempted_skill_reads),
            "successful_execution_skill_reads": sorted(successful_skill_reads),
            "successful_read_paths": sorted(successful_read_paths),
            "engineering_judgment_reference_read_succeeded": doctrine_read_succeeded,
            "timed_out": timed_out,
            "request_error": request_state.get("error"),
        }
        trace_path = args.trace_dir / f"activation-{run_id}.json"
        trace_path.write_text(
            json.dumps(trace, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        if timed_out:
            raise SystemExit(f"OpenCode probe timed out; activation trace: {trace_path}")
        if request_state.get("error") and final_object is None:
            raise SystemExit(
                f"OpenCode request failed; activation trace: {trace_path}"
            )
        if final_object is None:
            raise SystemExit(
                f"OpenCode produced no valid final JSON; activation trace: {trace_path}"
            )
        sys.stdout.write(canonical_final + "\n")
    finally:
        try:
            _request_json(
                "DELETE",
                f"{endpoint}/session/{urllib.parse.quote(session_id)}?{query}",
                timeout=min(args.timeout, 30.0),
            )
        except Exception:
            pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
