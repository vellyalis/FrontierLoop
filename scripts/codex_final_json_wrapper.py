#!/usr/bin/env python3
"""Run one Codex exec request and expose only its final message.

The wrapper is intentionally narrow.  It keeps the live benchmark's stdout
contract (one final JSON object) while recording only activation evidence from
Codex execution events.  It does not persist reasoning items, assistant prose,
or a raw session transcript.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from collections import Counter
from pathlib import Path
from typing import Any


SKILL_ID = re.compile(r"\bfrontier-[a-z0-9-]+\b", re.IGNORECASE)
SKILL_FILE = re.compile(
    r"(?i)(?:^|[\\/])(?:\.agents[\\/]skills[\\/])?"
    r"(frontier-[a-z0-9-]+)[\\/]SKILL\.md\b"
)
DOCTRINE_FILE = re.compile(
    r"(?i)(?:^|[\\/])references[\\/]ENGINEERING_JUDGMENT\.md\b"
)


def _walk_strings(value: Any):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from _walk_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_strings(child)


def _event_kind(event: dict[str, Any]) -> str:
    item = event.get("item")
    if isinstance(item, dict) and isinstance(item.get("type"), str):
        return f"{event.get('type', 'event')}:{item['type']}"
    return str(event.get("type", "unknown"))


def _is_observable_execution_event(event: dict[str, Any]) -> bool:
    """Exclude final/model text so model self-report cannot prove activation."""
    item = event.get("item")
    if isinstance(item, dict) and item.get("type") in {
        "agent_message",
        "reasoning",
        "message",
    }:
        return False
    return event.get("type") not in {"message", "assistant_message"}


def _execution_succeeded(event: dict[str, Any]) -> bool:
    item = event.get("item")
    if not isinstance(item, dict) or item.get("type") != "command_execution":
        return False
    exit_code = item.get("exit_code")
    status = item.get("status")
    return exit_code == 0 and status in {None, "completed", "success", "succeeded"}


def _extract_final_from_event(event: dict[str, Any]) -> str | None:
    item = event.get("item")
    if isinstance(item, dict) and item.get("type") in {"agent_message", "message"}:
        text = item.get("text") or item.get("content")
        if isinstance(text, str) and text.strip():
            return text
    if event.get("type") in {"message", "assistant_message"}:
        text = event.get("text") or event.get("content")
        if isinstance(text, str) and text.strip():
            return text
    return None


def _locate_codex(explicit: str | None) -> str:
    if explicit:
        return explicit
    local_appdata = os.environ.get("LOCALAPPDATA")
    candidates = [
        os.environ.get("CODEX_EXE"),
        str(Path(local_appdata) / "Programs" / "OpenAI" / "Codex" / "bin" / "codex.exe")
        if local_appdata
        else None,
        shutil.which("codex"),
    ]
    for candidate in candidates:
        if not candidate:
            continue
        if Path(candidate).is_file():
            return candidate
    raise SystemExit("Codex executable was not found; pass --codex")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--codex")
    parser.add_argument("--cwd", type=Path, default=Path.cwd())
    parser.add_argument("--trace-dir", type=Path, required=True)
    parser.add_argument("--timeout", type=float, default=180.0)
    parser.add_argument("--sandbox", default="read-only")
    parser.add_argument("--model")
    parser.add_argument("--reasoning-effort")
    args = parser.parse_args()

    prompt = sys.stdin.read()
    if not prompt.strip():
        raise SystemExit("stdin prompt is empty")

    args.trace_dir.mkdir(parents=True, exist_ok=True)
    run_id = f"{int(time.time() * 1000)}-{os.getpid()}-{uuid.uuid4().hex[:8]}"
    codex = _locate_codex(args.codex)

    with tempfile.TemporaryDirectory(prefix="frontier-codex-final-") as temp_dir:
        final_path = Path(temp_dir) / "final.txt"
        command = [
            codex,
            "exec",
            "--json",
            "--skip-git-repo-check",
            "--sandbox",
            args.sandbox,
            "--output-last-message",
            str(final_path),
        ]
        if args.model:
            command.extend(["--model", args.model])
        if args.reasoning_effort:
            command.extend(
                ["--config", f'model_reasoning_effort="{args.reasoning_effort}"']
            )
        command.append("-")

        try:
            process = subprocess.run(
                command,
                input=prompt,
                text=True,
                capture_output=True,
                cwd=args.cwd,
                timeout=args.timeout,
                shell=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise SystemExit(f"Codex timed out after {args.timeout} seconds") from exc

        event_counts: Counter[str] = Counter()
        execution_skill_reads: set[str] = set()
        successful_execution_skill_reads: set[str] = set()
        execution_skill_mentions: set[str] = set()
        doctrine_observed = False
        doctrine_read_succeeded = False
        parse_failures = 0
        final_from_events: str | None = None

        for line in process.stdout.splitlines():
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                parse_failures += 1
                continue
            if not isinstance(event, dict):
                continue
            event_counts[_event_kind(event)] += 1
            candidate = _extract_final_from_event(event)
            if candidate:
                final_from_events = candidate
            if not _is_observable_execution_event(event):
                continue
            succeeded = _execution_succeeded(event)
            for text in _walk_strings(event):
                for match in SKILL_FILE.finditer(text):
                    execution_skill_reads.add(match.group(1).lower())
                    if succeeded:
                        successful_execution_skill_reads.add(match.group(1).lower())
                for match in SKILL_ID.finditer(text):
                    execution_skill_mentions.add(match.group(0).lower())
                if DOCTRINE_FILE.search(text):
                    doctrine_observed = True
                    if succeeded:
                        doctrine_read_succeeded = True

        final_text = ""
        if final_path.is_file():
            final_text = final_path.read_text(encoding="utf-8", errors="replace").strip()
        if not final_text and final_from_events:
            final_text = final_from_events.strip()

        trace = {
            "schema": "frontierloop-codex-activation-trace/v1",
            "run_id": run_id,
            "exit_code": process.returncode,
            "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
            "final_sha256": hashlib.sha256(final_text.encode("utf-8")).hexdigest(),
            "event_counts": dict(sorted(event_counts.items())),
            "execution_skill_reads": sorted(execution_skill_reads),
            "successful_execution_skill_reads": sorted(successful_execution_skill_reads),
            "execution_skill_mentions": sorted(execution_skill_mentions),
            "engineering_judgment_reference_observed": doctrine_observed,
            "engineering_judgment_reference_read_succeeded": doctrine_read_succeeded,
            "jsonl_parse_failures": parse_failures,
            "stderr_excerpt": process.stderr[-4096:],
        }
        trace_path = args.trace_dir / f"activation-{run_id}.json"
        trace_path.write_text(
            json.dumps(trace, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

        if process.returncode:
            raise SystemExit(
                f"Codex exited {process.returncode}; activation trace: {trace_path}"
            )
        if not final_text:
            raise SystemExit(f"Codex produced no final message; activation trace: {trace_path}")
        sys.stdout.write(final_text)
        if not final_text.endswith("\n"):
            sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
