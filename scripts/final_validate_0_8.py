#!/usr/bin/env python3
"""Run the evidence gates required to accept FrontierLoop 0.8.0 locally."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


def run_step(
    name: str,
    command: list[str],
    *,
    cwd: Path,
    timeout: int,
) -> dict[str, Any]:
    started = time.time()
    try:
        process = subprocess.run(
            command,
            cwd=cwd,
            text=True,
            capture_output=True,
            timeout=timeout,
            shell=False,
            env=os.environ.copy(),
        )
        return {
            "name": name,
            "passed": process.returncode == 0,
            "returncode": process.returncode,
            "elapsed_seconds": round(time.time() - started, 3),
            "command": command,
            "stdout_tail": process.stdout[-12000:],
            "stderr_tail": process.stderr[-12000:],
        }
    except subprocess.TimeoutExpired as error:
        stdout = error.stdout.decode(errors="replace") if isinstance(error.stdout, bytes) else (error.stdout or "")
        stderr = error.stderr.decode(errors="replace") if isinstance(error.stderr, bytes) else (error.stderr or "")
        return {
            "name": name,
            "passed": False,
            "returncode": None,
            "elapsed_seconds": round(time.time() - started, 3),
            "command": command,
            "stdout_tail": stdout[-12000:],
            "stderr_tail": (stderr + f"\nTimed out after {timeout}s")[-12000:],
        }
    except Exception as error:  # pragma: no cover - defensive audit boundary
        return {
            "name": name,
            "passed": False,
            "returncode": None,
            "elapsed_seconds": round(time.time() - started, 3),
            "command": command,
            "stdout_tail": "",
            "stderr_tail": repr(error),
        }


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_active_junctions(root: Path, baseline: Path) -> dict[str, Any]:
    user_root = Path.home() / ".agents" / "skills"
    canonical_names = sorted(
        path.name
        for path in (root / "skills").iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    )
    rows: list[dict[str, Any]] = []
    expected_root = (baseline / "skills").resolve()
    for name in canonical_names:
        entry = user_root / name
        exists = entry.exists()
        resolved = entry.resolve() if exists else None
        expected = (expected_root / name).resolve()
        rows.append(
            {
                "name": name,
                "exists": exists,
                "resolved": str(resolved) if resolved else None,
                "expected": str(expected),
                "ok": bool(exists and resolved == expected),
            }
        )
    return {
        "count": len(rows),
        "all_on_preserved_0_7_0": len(rows) == 23 and all(row["ok"] for row in rows),
        "rows": rows,
    }


def activation_summary(path: Path, cases_path: Path) -> dict[str, Any]:
    payload = load_json(path)

    def find_activation(value: Any) -> dict[str, Any] | None:
        if isinstance(value, dict):
            if isinstance(value.get("trials"), list) and (
                "gate_pass" in value or "aggregate" in value
            ):
                return value
            for child in value.values():
                found = find_activation(child)
                if found is not None:
                    return found
        elif isinstance(value, list):
            for child in value:
                found = find_activation(child)
                if found is not None:
                    return found
        return None

    activation = find_activation(payload) or payload.get("activation", payload)

    def collect_rows(value: Any) -> list[dict[str, Any]]:
        found: list[dict[str, Any]] = []
        if isinstance(value, dict):
            if (
                isinstance(value.get("id"), str)
                and (
                    "decision" in value
                    or "selected_skills" in value
                    or "successful_skill_reads" in value
                )
            ):
                found.append(value)
            else:
                for child in value.values():
                    found.extend(collect_rows(child))
        elif isinstance(value, list):
            for child in value:
                found.extend(collect_rows(child))
        return found

    trials = activation.get("trials", [])
    rows = collect_rows(trials)
    case_payload = load_json(cases_path)
    case_list = case_payload.get("cases", case_payload)
    expected_by_id = {
        str(case["id"]): bool(
            case.get("expected_doctrine", case.get("doctrine_expected", False))
        )
        for case in case_list
    }

    def observed_doctrine(row: dict[str, Any]) -> bool:
        for key in (
            "doctrine_observed",
            "doctrine_reference_observed",
            "doctrine_read",
            "doctrine_used",
        ):
            if key in row:
                return bool(row.get(key))
        for key in (
            "successful_doctrine_reads",
            "doctrine_read_paths",
            "successful_reads",
        ):
            value = row.get(key)
            if isinstance(value, list):
                return any("ENGINEERING_JUDGMENT.md" in str(item) for item in value)
        return False

    expected_doctrine = sum(expected_by_id.get(str(row.get("id")), False) for row in rows)
    observed_doctrine_count = sum(observed_doctrine(row) for row in rows)
    case_ids = sorted({str(row.get("id")) for row in rows})
    return {
        "gate_pass": bool(activation.get("gate_pass")),
        "trial_count": activation.get("trial_count", len(trials)),
        "row_count": len(rows),
        "case_ids": case_ids,
        "case_count": len(case_ids),
        "expected_doctrine_reads": expected_doctrine,
        "observed_doctrine_reads": observed_doctrine_count,
        "execution_error_count": sum(bool(row.get("execution_error")) for row in rows),
        "aggregate": activation.get("aggregate", {}),
        "failed_rows": [
            {
                "id": row.get("id"),
                "errors": row.get("errors", []),
                "selected_skills": row.get("selected_skills", []),
                "successful_skill_reads": row.get("successful_skill_reads", []),
                "decision": row.get("decision"),
                "doctrine_observed": observed_doctrine(row),
            }
            for row in rows
            if row.get("errors") or row.get("execution_error")
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument(
        "--baseline",
        type=Path,
        default=Path.home() / ".codex" / "plugins" / "cache" / "personal" / "frontier-loop" / "0.7.0",
    )
    parser.add_argument("--activation-trials", type=int, default=3)
    parser.add_argument("--activation-attempts", type=int, default=3)
    parser.add_argument("--activation-timeout", type=int, default=90)
    parser.add_argument(
        "--reuse-activation",
        action="store_true",
        help="Reuse an existing candidate-0.8.0-live-3x10.json and rerun all non-model gates.",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    baseline = args.baseline.resolve()
    results = root / "evaluation" / "results"
    results.mkdir(parents=True, exist_ok=True)
    running = results / "0.8.0-VALIDATION-RUNNING"
    pass_sentinel = results / "0.8.0-FINAL-PASS"
    fail_sentinel = results / "0.8.0-FINAL-FAIL"
    audit_path = results / "0.8.0-final-audit.json"
    for marker in (pass_sentinel, fail_sentinel):
        marker.unlink(missing_ok=True)
    running.write_text(str(time.time()) + "\n", encoding="utf-8")

    python = sys.executable
    pwsh = shutil.which("pwsh") or shutil.which("powershell")
    if not pwsh:
        raise SystemExit("PowerShell is required")

    activation_path = results / "candidate-0.8.0-live-3x10.json"
    static_json = results / "0.8.0-final-static.json"
    static_md = results / "0.8.0-final-static.md"
    release_zip = results / "frontier-loop-0.8.0-final.zip"
    activation_trace = results / "activation-traces" / "candidate-0.8.0-3x10"
    if activation_trace.exists() and not args.reuse_activation:
        shutil.rmtree(activation_trace)

    steps: list[dict[str, Any]] = []
    steps.append(
        run_step(
            "python-compile",
            [
                python,
                "-m",
                "py_compile",
                "scripts/codex_final_json_wrapper.py",
                "scripts/opencode_final_json_wrapper.py",
                "scripts/run_engineering_judgment_activation.py",
                "scripts/run_opencode_frontierloop_comparison.py",
                "scripts/sync_skill_source_map.py",
                "scripts/final_validate_0_8.py",
            ],
            cwd=root,
            timeout=60,
        )
    )
    steps.append(
        run_step(
            "activation-runner-self-test",
            [
                python,
                "scripts/run_engineering_judgment_activation.py",
                "--cwd",
                str(results / "probe-workspace"),
                "--trace-dir",
                str(results / "activation-self-test"),
                "--output",
                str(results / "activation-self-test.json"),
                "--self-test",
            ],
            cwd=root,
            timeout=60,
        )
    )
    if args.reuse_activation:
        steps.append(
            {
                "name": "actual-skill-activation-3x10-reused",
                "passed": activation_path.is_file(),
                "returncode": 0 if activation_path.is_file() else 1,
                "elapsed_seconds": 0.0,
                "command": [],
                "stdout_tail": str(activation_path),
                "stderr_tail": "" if activation_path.is_file() else "activation result is missing",
            }
        )
    else:
        steps.append(
            run_step(
                "actual-skill-activation-3x10",
                [
                    python,
                    "scripts/run_opencode_frontierloop_comparison.py",
                    "--only",
                    "candidate",
                    "--activation-trials",
                    str(args.activation_trials),
                    "--attempts",
                    str(args.activation_attempts),
                    "--timeout",
                    str(args.activation_timeout),
                    "--model",
                    "opencode/big-pickle",
                    "--output",
                    str(activation_path),
                ],
                cwd=root,
                timeout=max(1800, args.activation_trials * 10 * args.activation_timeout * args.activation_attempts),
            )
        )

    activation: dict[str, Any]
    try:
        activation = activation_summary(
            activation_path,
            root / "evaluation" / "engineering-judgment-activation-cases.json",
        )
    except Exception as error:
        activation = {"gate_pass": False, "read_error": repr(error)}

    steps.append(
        run_step(
            "source-verifier",
            [pwsh, "-NoProfile", "-File", "scripts/Verify-FrontierLoop.ps1", "-Root", str(root)],
            cwd=root,
            timeout=180,
        )
    )
    steps.append(
        run_step(
            "static-baseline-comparison",
            [
                python,
                "scripts/evaluate_frontierloop.py",
                "--root",
                str(root),
                "--baseline-root",
                str(baseline),
                "--json-out",
                str(static_json),
                "--markdown-out",
                str(static_md),
                "--self-test",
            ],
            cwd=root,
            timeout=240,
        )
    )
    steps.append(
        run_step(
            "installer-lifecycle-tests",
            [pwsh, "-NoProfile", "-File", "tests/Test-FrontierLoopInstall.ps1", "-Source", str(root)],
            cwd=root,
            timeout=600,
        )
    )
    steps.append(
        run_step(
            "deterministic-release-build",
            [python, "scripts/build_release.py", "--root", str(root), "--output", str(release_zip)],
            cwd=root,
            timeout=300,
        )
    )
    steps.append(
        run_step(
            "deterministic-release-byte-verify",
            [python, "scripts/build_release.py", "--root", str(root), "--output", str(release_zip), "--verify"],
            cwd=root,
            timeout=300,
        )
    )

    try:
        static = load_json(static_json)
        comparison = static.get("comparison", {})
        static_summary = {
            "candidate_valid": bool(static.get("candidate", {}).get("valid")),
            "promotion_eligible": bool(comparison.get("promotion_eligible")),
            "candidate_gains": comparison.get("candidate_gains", []),
            "retained_regressions": comparison.get("retained_capability_regressions", []),
            "implicit_count_delta": comparison.get("implicit_count_delta"),
            "implicit_catalog_bytes_delta": comparison.get("implicit_catalog_bytes_delta"),
        }
    except Exception as error:
        static_summary = {"candidate_valid": False, "read_error": repr(error)}

    junctions = resolve_active_junctions(root, baseline)
    release = {
        "exists": release_zip.is_file(),
        "path": str(release_zip),
        "bytes": release_zip.stat().st_size if release_zip.is_file() else None,
        "sha256": sha256(release_zip) if release_zip.is_file() else None,
    }
    all_steps_pass = all(step["passed"] for step in steps)
    overall_pass = bool(
        all_steps_pass
        and activation.get("gate_pass")
        and activation.get("trial_count") == args.activation_trials
        and activation.get("row_count") == args.activation_trials * 10
        and activation.get("case_count") == 10
        and activation.get("expected_doctrine_reads") == args.activation_trials * 8
        and activation.get("observed_doctrine_reads") == args.activation_trials * 8
        and activation.get("execution_error_count") == 0
        and static_summary.get("candidate_valid")
        and static_summary.get("promotion_eligible")
        and not static_summary.get("retained_regressions")
        and junctions["all_on_preserved_0_7_0"]
        and release["exists"]
    )
    audit = {
        "schema": "frontierloop-0.8.0-final-audit/v1",
        "generated_at_unix": time.time(),
        "root": str(root),
        "baseline": str(baseline),
        "overall_pass": overall_pass,
        "activation": activation,
        "static": static_summary,
        "active_junctions": junctions,
        "release": release,
        "steps": steps,
    }
    audit_path.write_text(
        json.dumps(audit, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    running.unlink(missing_ok=True)
    marker = pass_sentinel if overall_pass else fail_sentinel
    marker.write_text(
        json.dumps(
            {
                "overall_pass": overall_pass,
                "audit": str(audit_path),
                "release_sha256": release["sha256"],
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps(audit, indent=2, ensure_ascii=False))
    return 0 if overall_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
