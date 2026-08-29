#!/usr/bin/env python3
"""Aggregate independent OpenCode activation case reports without schema guessing."""
from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path
from typing import Any


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def walk(value: Any, path: tuple[str, ...] = ()):
    yield path, value
    if isinstance(value, dict):
        for key, child in value.items():
            yield from walk(child, path + (str(key),))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk(child, path + (str(index),))


def scalar_values(payload: Any, key: str) -> list[Any]:
    return [
        value
        for path, value in walk(payload)
        if path and path[-1] == key and not isinstance(value, (dict, list))
    ]


def list_lengths(payload: Any, key: str) -> list[int]:
    return [
        len(value)
        for path, value in walk(payload)
        if path and path[-1] == key and isinstance(value, list)
    ]


def find_activation_gate(payload: Any) -> dict[str, Any] | None:
    for path, value in walk(payload):
        if path and path[-1] == "activation_gate" and isinstance(value, dict):
            return value
    return None


def false_boolean_paths(payload: Any) -> list[str]:
    return [
        ".".join(path)
        for path, value in walk(payload)
        if type(value) is bool and value is False
    ]


def error_findings(payload: Any) -> list[str]:
    findings: list[str] = []
    for path, value in walk(payload):
        if not path:
            continue
        key = path[-1].lower()
        joined = ".".join(path)
        if "error" in key:
            if isinstance(value, list) and value:
                findings.append(f"{joined}: non-empty list ({len(value)})")
            elif isinstance(value, str) and value.strip():
                findings.append(f"{joined}: {value[:300]}")
            elif isinstance(value, (int, float)) and not isinstance(value, bool) and value != 0:
                findings.append(f"{joined}: {value}")
            elif value is True:
                findings.append(f"{joined}: true")
    return findings


def quality_metrics(payload: Any) -> dict[str, list[float]]:
    result: dict[str, list[float]] = {}
    for path, value in walk(payload):
        if not path or isinstance(value, bool) or not isinstance(value, (int, float)):
            continue
        key = path[-1].lower()
        relevant = any(token in key for token in ("decision", "doctrine", "skill", "read"))
        quality = any(token in key for token in ("accuracy", "recall", "rate"))
        if relevant and quality:
            result.setdefault(path[-1], []).append(float(value))
    return result


def zero_cost_metrics(payload: Any) -> dict[str, list[float]]:
    result: dict[str, list[float]] = {}
    for path, value in walk(payload):
        if not path or isinstance(value, bool) or not isinstance(value, (int, float)):
            continue
        key = path[-1].lower()
        if any(token in key for token in ("forbidden", "unnecessary", "unexpected", "extra_skill", "execution_error")):
            result.setdefault(path[-1], []).append(float(value))
    return result


def evaluate_case(path: Path, case_id: str, expected_trials: int) -> dict[str, Any]:
    if not path.is_file():
        return {"id": case_id, "passed": False, "errors": ["result file missing"]}
    try:
        payload = load(path)
    except Exception as error:
        return {"id": case_id, "passed": False, "errors": [f"invalid JSON: {error!r}"]}

    errors: list[str] = []
    trial_lengths = list_lengths(payload, "trials")
    if expected_trials not in trial_lengths:
        errors.append(f"no trials list has expected length {expected_trials}; found {trial_lengths}")

    gate = find_activation_gate(payload)
    if gate is None:
        errors.append("activation_gate object missing")
        gate_false: list[str] = []
    else:
        gate_false = false_boolean_paths(gate)
        if gate_false:
            errors.append("activation_gate contains false conditions: " + ", ".join(gate_false))

    metrics = quality_metrics(payload)
    required_names = ("decision_accuracy", "doctrine_accuracy", "required_skill_recall")
    for name in required_names:
        values = metrics.get(name, [])
        if not values:
            errors.append(f"required metric missing: {name}")
        elif any(not math.isclose(value, 1.0, abs_tol=1e-12) for value in values):
            errors.append(f"{name} is not 1.0: {values}")

    zero_metrics = zero_cost_metrics(payload)
    for name, values in zero_metrics.items():
        if any(not math.isclose(value, 0.0, abs_tol=1e-12) for value in values):
            errors.append(f"{name} is not zero: {values}")

    reported_errors = error_findings(payload)
    if reported_errors:
        errors.extend(reported_errors)

    return {
        "id": case_id,
        "passed": not errors,
        "path": str(path),
        "trial_list_lengths": trial_lengths,
        "quality_metrics": metrics,
        "zero_cost_metrics": zero_metrics,
        "activation_gate_false_conditions": gate_false,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--cases", type=Path)
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    case_path = args.cases or root / "evaluation" / "engineering-judgment-activation-cases.json"
    case_payload = load(case_path)
    cases = case_payload.get("cases", case_payload)
    input_dir = args.input_dir.resolve()
    rows = [
        evaluate_case(input_dir / f"{case['id']}.json", str(case["id"]), args.trials)
        for case in cases
    ]
    passed = all(row["passed"] for row in rows) and len(rows) == 10
    report = {
        "schema": "frontierloop-split-activation/v1",
        "activation_gate_pass": passed,
        "trial_count": args.trials,
        "case_count": len(rows),
        "row_count": args.trials * len(rows),
        "expected_doctrine_reads": args.trials * sum(
            bool(case.get("expected_doctrine", case.get("doctrine_expected", False)))
            for case in cases
        ),
        "cases": rows,
        "failed_cases": [row for row in rows if not row["passed"]],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
