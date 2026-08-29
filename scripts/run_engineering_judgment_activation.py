#!/usr/bin/env python3
"""Run independent read-only FrontierLoop activation probes.

Each case is a separate Codex session.  The persisted artifact contains only a
small structured decision and activation evidence; no hidden reasoning or raw
session transcript is retained.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


RESPONSE_KEYS = {
    "decision",
    "selected_skills",
    "engineering_judgment_applied",
    "canonical_owner",
    "responsibility_decision",
    "mechanisms_added",
    "mechanisms_removed_or_rejected",
    "verification",
}


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def is_allowed_probe_read_path(path: str) -> bool:
    normalized = path.replace("/", "\\").lower()
    return (
        "\\.opencode\\skills\\" in normalized
        or normalized.endswith("\\.opencode")
    )


def response_semantic_text(response: dict[str, Any]) -> str:
    values: list[str] = []
    for field in ("canonical_owner", "responsibility_decision"):
        value = response.get(field)
        if isinstance(value, str):
            values.append(value)
    for field in (
        "mechanisms_added",
        "mechanisms_removed_or_rejected",
        "verification",
    ):
        value = response.get(field)
        if isinstance(value, list):
            values.extend(str(item) for item in value if isinstance(item, str))
    return "\n".join(values)


def build_prompt(case: dict[str, Any], decisions: list[str]) -> str:
    contract = {
        "decision": f"one exact string from: {decisions}",
        "selected_skills": "exact FrontierLoop Skill IDs actually selected; include frontier-core when the request is non-trivial",
        "engineering_judgment_applied": "boolean",
        "canonical_owner": "one short factual sentence; use unknown when evidence is insufficient",
        "responsibility_decision": "one short factual sentence",
        "mechanisms_added": "array of mechanism names",
        "mechanisms_removed_or_rejected": "array of mechanism names",
        "verification": "array of observable checks",
    }
    return (
        "Handle the request under the actually installed FrontierLoop instructions. "
        "This is a read-only activation and engineering-decision probe: do not modify files, "
        "do not ask the user, do not run tests, do not inspect project files, and do not invent repository facts. "
        "The request is self-contained for routing. Do not call glob, grep, list, shell, task, or project-file reads; "
        "the only content reads allowed are selected Skill bodies through the skill tool and, after a positive "
        "material trigger, the canonical ENGINEERING_JUDGMENT.md through the read tool. Apply only "
        "the narrow Skills whose real trigger is present. TOOL-CALL GATE: before deciding, call "
        "the skill tool for every Skill that will govern the answer; a catalog description or "
        "remembered summary is not the Skill body. Do not list a Skill in selected_skills unless "
        "its skill-tool call completed successfully in this session, and do not open a Skill just "
        "to reject it when its catalog description already says it is explicit-only or out of "
        "scope. When engineering_judgment_applied is true, use the read tool to open the canonical "
        "ENGINEERING_JUDGMENT.md reference before returning; self-report without that successful "
        "read is invalid. Return raw JSON only, with exactly "
        "the fields in the response contract. Do not provide chain of thought or prose outside JSON.\n"
        f"Response contract: {json.dumps(contract, ensure_ascii=False, separators=(',', ':'))}\n"
        f"Request: {case['request']}"
    )


def validate_response(value: Any, decisions: set[str]) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != RESPONSE_KEYS:
        raise ValueError(f"response fields differ: {sorted(value) if isinstance(value, dict) else type(value)}")
    if (
        isinstance(value["decision"], list)
        and len(value["decision"]) == 1
        and isinstance(value["decision"][0], str)
    ):
        value["decision"] = value["decision"][0]
    if not isinstance(value["decision"], str) or value["decision"] not in decisions:
        raise ValueError(f"invalid decision: {value['decision']!r}")
    skills = value["selected_skills"]
    if isinstance(skills, str):
        extracted = re.findall(r"\bfrontier-[a-z0-9-]+\b", skills, re.IGNORECASE)
        if extracted:
            skills = list(dict.fromkeys(skill.lower() for skill in extracted))
            value["selected_skills"] = skills
    if not isinstance(skills, list) or any(
        not isinstance(skill, str) or not skill.startswith("frontier-") for skill in skills
    ):
        raise ValueError("selected_skills must contain FrontierLoop Skill IDs")
    if len(skills) != len(set(skills)):
        raise ValueError("selected_skills contains duplicates")
    doctrine = value["engineering_judgment_applied"]
    if isinstance(doctrine, list) and len(doctrine) == 1:
        doctrine = doctrine[0]
    if isinstance(doctrine, str) and doctrine.strip().lower() in {"true", "false"}:
        doctrine = doctrine.strip().lower() == "true"
    value["engineering_judgment_applied"] = doctrine
    if type(value["engineering_judgment_applied"]) is not bool:
        raise ValueError("engineering_judgment_applied must be boolean")
    for field in ("canonical_owner", "responsibility_decision"):
        if not isinstance(value[field], str) or not value[field].strip():
            raise ValueError(f"{field} must be a non-empty string")
    for field in ("mechanisms_added", "mechanisms_removed_or_rejected", "verification"):
        if not isinstance(value[field], list) or any(not isinstance(x, str) for x in value[field]):
            raise ValueError(f"{field} must be a string array")
    return value


def run_one(
    *,
    python_exe: str,
    wrapper: Path,
    wrapper_args: list[str],
    cwd: Path,
    trace_dir: Path,
    timeout: float,
    prompt: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    before = {path.name for path in trace_dir.glob("activation-*.json")} if trace_dir.is_dir() else set()
    command = [
        python_exe,
        str(wrapper),
        *wrapper_args,
        "--cwd",
        str(cwd),
        "--trace-dir",
        str(trace_dir),
        "--timeout",
        str(timeout),
    ]
    process = subprocess.run(
        command,
        input=prompt,
        text=True,
        capture_output=True,
        timeout=timeout + 30,
        shell=False,
    )
    if process.returncode:
        raise RuntimeError(f"wrapper exit {process.returncode}: {process.stderr[-4096:]}")
    response = json.loads(process.stdout)
    created = [path for path in trace_dir.glob("activation-*.json") if path.name not in before]
    if len(created) != 1:
        raise RuntimeError(f"expected one activation trace, found {len(created)}")
    trace = load(created[0])
    return response, trace


def main() -> int:
    parser = argparse.ArgumentParser()
    root_default = Path(__file__).resolve().parents[1]
    parser.add_argument("--root", type=Path, default=root_default)
    parser.add_argument(
        "--cases", type=Path, default=root_default / "evaluation" / "engineering-judgment-activation-cases.json"
    )
    parser.add_argument("--cwd", type=Path, required=True)
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument(
        "--attempts",
        type=int,
        default=3,
        help="Maximum attempts per case before recording a failed probe row.",
    )
    parser.add_argument("--timeout", type=float, default=180.0)
    parser.add_argument("--trace-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--label", default="candidate")
    parser.add_argument(
        "--case",
        action="append",
        default=[],
        help="Run only the named case ID; repeat to select multiple cases.",
    )
    parser.add_argument(
        "--wrapper",
        type=Path,
        default=root_default / "scripts" / "codex_final_json_wrapper.py",
    )
    parser.add_argument(
        "--wrapper-arg",
        action="append",
        default=[],
        help="Additional argument passed to the selected wrapper; repeat as needed.",
    )
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    data = load(args.cases)
    cases = data.get("cases", [])
    if args.case:
        requested = set(args.case)
        known = {case["id"] for case in cases}
        missing = sorted(requested - known)
        if missing:
            raise SystemExit(f"unknown activation case IDs: {missing}")
        cases = [case for case in cases if case["id"] in requested]
    decisions = set(data.get("decision_vocabulary", []))
    if not cases or len({case["id"] for case in cases}) != len(cases):
        raise SystemExit("activation cases must be non-empty with unique IDs")
    if args.trials < 1:
        raise SystemExit("--trials must be positive")
    if args.attempts < 1:
        raise SystemExit("--attempts must be positive")

    if args.self_test:
        sample = {
            "decision": next(iter(decisions)),
            "selected_skills": ["frontier-core"],
            "engineering_judgment_applied": False,
            "canonical_owner": "unknown",
            "responsibility_decision": "No structural change.",
            "mechanisms_added": [],
            "mechanisms_removed_or_rejected": [],
            "verification": [],
        }
        validate_response(sample, decisions)
        print(json.dumps({"self_test": "Pass", "case_count": len(cases)}, sort_keys=True))
        return 0

    wrapper = args.wrapper
    if not wrapper.is_absolute():
        wrapper = args.root / wrapper
    if not wrapper.is_file():
        raise SystemExit(f"wrapper missing: {wrapper}")
    args.cwd.mkdir(parents=True, exist_ok=True)
    args.trace_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, Any]] = []
    for trial in range(1, args.trials + 1):
        for case in cases:
            case_trace_dir = args.trace_dir / f"trial-{trial}" / case["id"]
            case_trace_dir.mkdir(parents=True, exist_ok=True)
            prompt = build_prompt(case, sorted(decisions))
            response: dict[str, Any] | None = None
            trace: dict[str, Any] | None = None
            last_raw_response: Any = None
            last_error: str | None = None
            used_attempt = 0
            for attempt in range(1, args.attempts + 1):
                used_attempt = attempt
                try:
                    raw_response, trace = run_one(
                        python_exe=sys.executable,
                        wrapper=wrapper,
                        wrapper_args=args.wrapper_arg,
                        cwd=args.cwd,
                        trace_dir=case_trace_dir,
                        timeout=args.timeout,
                        prompt=prompt,
                    )
                    last_raw_response = raw_response
                    response = validate_response(raw_response, decisions)
                    last_error = None
                    break
                except Exception as exc:  # one failed probe must not discard prior evidence
                    last_error = f"{type(exc).__name__}: {exc}"

            required = set(case.get("required_selected_skills", []))
            optional = set(case.get("allowed_optional_selected_skills", []))
            forbidden = set(case.get("forbidden_selected_skills", []))
            required_response_patterns = [
                str(pattern) for pattern in case.get("required_response_patterns", [])
            ]
            expected = {
                "decision": case["expected_decision"],
                "accepted_decisions": case.get(
                    "accepted_decisions", [case["expected_decision"]]
                ),
                "required_selected_skills": sorted(required),
                "allowed_optional_selected_skills": sorted(optional),
                "forbidden_selected_skills": sorted(forbidden),
                "engineering_judgment_applied": case["expected_doctrine"],
                "required_response_patterns": required_response_patterns,
            }
            if response is None or trace is None:
                row = {
                    "trial": trial,
                    "id": case["id"],
                    "attempts": used_attempt,
                    "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
                    "response": None,
                    "raw_response": last_raw_response,
                    "expected": expected,
                    "metrics": {
                        "decision_correct": False,
                        "required_skill_recall": 0.0 if required else 1.0,
                        "unexpected_skill_count": 0,
                        "forbidden_skill_count": 0,
                        "doctrine_correct": False,
                        "execution_body_read_recall": 0.0 if required else 1.0,
                        "doctrine_reference_observed": False,
                        "out_of_scope_read_count": 0,
                        "response_pattern_recall": 0.0
                        if required_response_patterns
                        else 1.0,
                        "missing_response_pattern_count": len(
                            required_response_patterns
                        ),
                    },
                    "activation_evidence": {
                        "execution_skill_reads": [],
                        "attempted_execution_skill_reads": [],
                        "execution_skill_mentions": [],
                        "event_counts": {},
                        "trace_run_id": None,
                        "successful_read_paths": [],
                        "out_of_scope_read_paths": [],
                        "missing_response_patterns": required_response_patterns,
                    },
                    "error": last_error,
                }
                rows.append(row)
                args.output.parent.mkdir(parents=True, exist_ok=True)
                args.output.write_text(
                    json.dumps(
                        {
                            "schema": "frontierloop-engineering-judgment-activation/checkpoint-v1",
                            "label": args.label,
                            "trial_count": args.trials,
                            "case_count": len(cases),
                            "rows": rows,
                        },
                        indent=2,
                        sort_keys=True,
                        ensure_ascii=False,
                    )
                    + "\n",
                    encoding="utf-8",
                )
                continue

            selected = set(response["selected_skills"])
            execution_reads = set(trace.get("successful_execution_skill_reads", []))
            successful_read_paths = [
                str(path) for path in trace.get("successful_read_paths", [])
            ]
            out_of_scope_read_paths = [
                path
                for path in successful_read_paths
                if not is_allowed_probe_read_path(path)
            ]
            activated = selected | execution_reads
            row = {
                "trial": trial,
                "id": case["id"],
                "attempts": used_attempt,
                "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
                "response": response,
                "raw_response": response,
                "expected": expected,
                "metrics": {
                    "decision_correct": response["decision"]
                    in set(case.get("accepted_decisions", [case["expected_decision"]])),
                    "required_skill_recall": len(selected & required) / len(required) if required else 1.0,
                    "unexpected_skill_count": len(activated - required - optional),
                    "forbidden_skill_count": len(activated & forbidden),
                    "doctrine_correct": response["engineering_judgment_applied"] == case["expected_doctrine"],
                    "execution_body_read_recall": len(execution_reads & required) / len(required) if required else 1.0,
                    "doctrine_reference_observed": bool(
                        trace.get("engineering_judgment_reference_read_succeeded")
                    ),
                    "out_of_scope_read_count": len(out_of_scope_read_paths),
                },
                "activation_evidence": {
                    "execution_skill_reads": sorted(execution_reads),
                    "attempted_execution_skill_reads": trace.get("execution_skill_reads", []),
                    "execution_skill_mentions": trace.get("execution_skill_mentions", []),
                    "event_counts": trace.get("event_counts", {}),
                    "trace_run_id": trace.get("run_id"),
                    "successful_read_paths": successful_read_paths,
                    "out_of_scope_read_paths": out_of_scope_read_paths,
                },
                "error": None,
            }
            rows.append(row)
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(
                json.dumps(
                    {
                        "schema": "frontierloop-engineering-judgment-activation/checkpoint-v1",
                        "label": args.label,
                        "trial_count": args.trials,
                        "case_count": len(cases),
                        "rows": rows,
                    },
                    indent=2,
                    sort_keys=True,
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )

    n = len(rows)
    required_denominator = sum(len(row["expected"]["required_selected_skills"]) for row in rows)
    required_hits = sum(
        len(
            set(row["response"]["selected_skills"])
            & set(row["expected"]["required_selected_skills"])
        )
        if isinstance(row.get("response"), dict)
        else 0
        for row in rows
    )
    forbidden_total = sum(row["metrics"]["forbidden_skill_count"] for row in rows)
    aggregate = {
        "decision_accuracy": sum(row["metrics"]["decision_correct"] for row in rows) / n,
        "required_skill_recall": required_hits / required_denominator if required_denominator else 1.0,
        "forbidden_skill_activation_count": forbidden_total,
        "doctrine_accuracy": sum(row["metrics"]["doctrine_correct"] for row in rows) / n,
        "execution_body_read_recall": sum(row["metrics"]["execution_body_read_recall"] for row in rows) / n,
        "doctrine_reference_observation_rate": sum(
            row["metrics"]["doctrine_reference_observed"] for row in rows
        )
        / n,
        "execution_error_count": sum(bool(row.get("error")) for row in rows),
    }
    report = {
        "schema": "frontierloop-engineering-judgment-activation/v1",
        "label": args.label,
        "trial_count": args.trials,
        "case_count": len(cases),
        "case_definition_sha256": hashlib.sha256(
            json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        ).hexdigest(),
        "aggregate": aggregate,
        "rows": rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"output": str(args.output), "aggregate": aggregate}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
