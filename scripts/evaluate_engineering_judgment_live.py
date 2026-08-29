#!/usr/bin/env python3
"""Hard-gate FrontierLoop engineering-judgment live evidence."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


CRITICAL_BATCH_CASES = {
    "new-state-owner",
    "large-ui-file-new-responsibility",
    "similar-code-speculative-core",
    "real-core-candidate",
    "stale-selection-cache",
    "continuous-selection-scan",
    "presentation-only-copy-edit",
}


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def per_case_trials(report: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    result: dict[str, list[dict[str, Any]]] = {}
    for trial in report.get("trials", []):
        metrics = {row["id"]: row for row in trial["metrics"]["per_case"]}
        responses = {row["id"]: row for row in trial["response"]["cases"]}
        for case_id, metric in metrics.items():
            result.setdefault(case_id, []).append(
                {"trial": trial["trial"], "metrics": metric, "response": responses[case_id]}
            )
    return result


def markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Engineering judgment live gate",
        "",
        f"Overall: {'Pass' if report['eligible'] else 'Fail'}",
        f"Baseline batch trials: {report['baseline_batch_trials']}",
        f"Candidate batch trials: {report['candidate_batch_trials']}",
        f"Candidate activation trials: {report['candidate_activation_trials']}",
        "",
        "## Gates",
    ]
    lines.extend(
        f"- {'Pass' if value else 'Fail'}: {name}"
        for name, value in report["gates"].items()
    )
    if report["failures"]:
        lines += ["", "## Failures"]
        for failure in report["failures"]:
            lines.append(f"- {failure['gate']}: {failure['id']} trial {failure.get('trial', '-')}: {failure['reason']}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline-batch", type=Path, required=True)
    parser.add_argument("--candidate-batch", type=Path, required=True)
    parser.add_argument("--baseline-activation", type=Path, required=True)
    parser.add_argument("--candidate-activation", type=Path, required=True)
    parser.add_argument("--json-out", type=Path, required=True)
    parser.add_argument("--markdown-out", type=Path, required=True)
    args = parser.parse_args()

    baseline_batch = load(args.baseline_batch)
    candidate_batch = load(args.candidate_batch)
    baseline_activation = load(args.baseline_activation)
    candidate_activation = load(args.candidate_activation)
    failures: list[dict[str, Any]] = []

    same_case_hash = (
        baseline_batch.get("case_definition_hash")
        == candidate_batch.get("case_definition_hash")
    )
    if not same_case_hash:
        failures.append({"gate": "matched-batch", "id": "case-set", "reason": "case hashes differ"})

    same_activation_case_hash = (
        baseline_activation.get("case_definition_sha256")
        == candidate_activation.get("case_definition_sha256")
        and baseline_activation.get("case_definition_sha256") is not None
    )
    if not same_activation_case_hash:
        failures.append(
            {"gate": "matched-activation", "id": "case-set", "reason": "activation case hashes differ"}
        )

    baseline_cases = per_case_trials(baseline_batch)
    candidate_cases = per_case_trials(candidate_batch)
    critical_batch_pass = True
    for case_id in sorted(CRITICAL_BATCH_CASES):
        rows = candidate_cases.get(case_id, [])
        if len(rows) != candidate_batch.get("trial_count"):
            critical_batch_pass = False
            failures.append(
                {"gate": "critical-batch", "id": case_id, "reason": "missing candidate trials"}
            )
            continue
        for row in rows:
            metric = row["metrics"]
            if (
                metric["required_recall"] < 1.0
                or not metric["exact_capability_set"]
                or metric["unnecessary_capability_count"] != 0
                or not metric["decision_correct"]
                or metric["guardrail_pass_rate"] < 1.0
            ):
                critical_batch_pass = False
                failures.append(
                    {
                        "gate": "critical-batch",
                        "id": case_id,
                        "trial": row["trial"],
                        "reason": (
                            f"recall={metric['required_recall']}, "
                            f"exact={metric['exact_capability_set']}, "
                            f"extras={metric['unnecessary_capability_count']}, "
                            f"decision={metric['decision_correct']}, "
                            f"guardrail={metric['guardrail_pass_rate']}"
                        ),
                    }
                )

    activation_rows = candidate_activation.get("rows", [])
    expected_activation_rows = (
        candidate_activation.get("trial_count", 0)
        * candidate_activation.get("case_count", 0)
    )
    activation_complete = len(activation_rows) == expected_activation_rows and expected_activation_rows > 0
    if not activation_complete:
        failures.append(
            {
                "gate": "activation-complete",
                "id": "activation",
                "reason": f"rows={len(activation_rows)}, expected={expected_activation_rows}",
            }
        )

    activation_decisions = activation_complete
    activation_routing = activation_complete
    activation_body_reads = activation_complete
    activation_minimal_reads = activation_complete
    activation_doctrine_reads = activation_complete
    routine_non_activation = activation_complete
    for row in activation_rows:
        metrics = row["metrics"]
        expected_doctrine = row["expected"]["engineering_judgment_applied"]
        required = set(row["expected"]["required_selected_skills"])
        selected = set(row["response"]["selected_skills"])
        successful_reads = set(row["activation_evidence"]["execution_skill_reads"])
        routine_optional = {"frontier-core"} if not expected_doctrine and not required else set()
        allowed = required | routine_optional
        if not metrics["decision_correct"]:
            activation_decisions = False
            failures.append(
                {
                    "gate": "activation-decision",
                    "id": row["id"],
                    "trial": row["trial"],
                    "reason": f"got {row['response']['decision']}, expected {row['expected']['decision']}",
                }
            )
        if (
            metrics["required_skill_recall"] < 1.0
            or metrics["forbidden_skill_count"]
            or not required.issubset(selected)
            or bool(selected - allowed)
        ):
            activation_routing = False
            failures.append(
                {
                    "gate": "activation-routing",
                    "id": row["id"],
                    "trial": row["trial"],
                    "reason": (
                        f"required_recall={metrics['required_skill_recall']}, "
                        f"forbidden={metrics['forbidden_skill_count']}, "
                        f"selected={sorted(selected)}, allowed={sorted(allowed)}"
                    ),
                }
            )
        if metrics["execution_body_read_recall"] < 1.0:
            activation_body_reads = False
            failures.append(
                {
                    "gate": "activation-body-read",
                    "id": row["id"],
                    "trial": row["trial"],
                    "reason": (
                        f"successful_read_recall={metrics['execution_body_read_recall']}; "
                        f"reads={row['activation_evidence']['execution_skill_reads']}"
                    ),
                }
            )
        if successful_reads - allowed:
            activation_minimal_reads = False
            failures.append(
                {
                    "gate": "activation-minimal-read-set",
                    "id": row["id"],
                    "trial": row["trial"],
                    "reason": (
                        f"successful_reads={sorted(successful_reads)}, "
                        f"allowed={sorted(allowed)}"
                    ),
                }
            )
        if expected_doctrine and (
            not metrics["doctrine_correct"]
            or not metrics["doctrine_reference_observed"]
        ):
            activation_doctrine_reads = False
            failures.append(
                {
                    "gate": "doctrine-read",
                    "id": row["id"],
                    "trial": row["trial"],
                    "reason": (
                        f"declared={row['response']['engineering_judgment_applied']}, "
                        f"successful_reference_read={metrics['doctrine_reference_observed']}"
                    ),
                }
            )
        if not expected_doctrine:
            forbidden = set(row["expected"]["forbidden_selected_skills"])
            if (
                metrics["doctrine_correct"] is False
                or metrics["doctrine_reference_observed"]
                or selected & forbidden
            ):
                routine_non_activation = False
                failures.append(
                    {
                        "gate": "routine-non-activation",
                        "id": row["id"],
                        "trial": row["trial"],
                        "reason": (
                            f"doctrine={row['response']['engineering_judgment_applied']}, "
                            f"successful_reference_read={metrics['doctrine_reference_observed']}, "
                            f"forbidden_selected={sorted(selected & forbidden)}"
                        ),
                    }
                )

    candidate_aggregate = candidate_batch.get("aggregate", {})
    baseline_aggregate = baseline_batch.get("aggregate", {})
    retained_no_critical_regression = all(
        candidate_aggregate.get(metric, 0.0) + 1e-12
        >= baseline_aggregate.get(metric, 0.0)
        for metric in (
            "required_capability_recall",
            "decision_accuracy",
            "universal_guardrail_pass_rate",
        )
    )
    if not retained_no_critical_regression:
        failures.append(
            {
                "gate": "retained-aggregate",
                "id": "batch",
                "reason": f"baseline={baseline_aggregate}, candidate={candidate_aggregate}",
            }
        )

    no_extra_growth = candidate_aggregate.get("unnecessary_capability_count", 10**9) <= baseline_aggregate.get(
        "unnecessary_capability_count", -1
    )
    if not no_extra_growth:
        failures.append(
            {
                "gate": "unnecessary-capability-growth",
                "id": "batch",
                "reason": (
                    f"baseline={baseline_aggregate.get('unnecessary_capability_count')}, "
                    f"candidate={candidate_aggregate.get('unnecessary_capability_count')}"
                ),
            }
        )

    gates = {
        "matched-batch-case-set": same_case_hash,
        "matched-activation-case-set": same_activation_case_hash,
        "critical-batch-all-trials": critical_batch_pass,
        "activation-complete": activation_complete,
        "activation-decisions": activation_decisions,
        "activation-routing": activation_routing,
        "activation-body-reads": activation_body_reads,
        "activation-minimal-read-set": activation_minimal_reads,
        "activation-doctrine-reads": activation_doctrine_reads,
        "routine-non-activation": routine_non_activation,
        "retained-no-critical-regression": retained_no_critical_regression,
        "no-unnecessary-capability-growth": no_extra_growth,
    }
    report = {
        "schema": "frontierloop-engineering-judgment-live-gate/v1",
        "eligible": all(gates.values()),
        "baseline_batch_trials": baseline_batch.get("trial_count"),
        "candidate_batch_trials": candidate_batch.get("trial_count"),
        "baseline_activation_trials": baseline_activation.get("trial_count"),
        "candidate_activation_trials": candidate_activation.get("trial_count"),
        "baseline_batch_aggregate": baseline_aggregate,
        "candidate_batch_aggregate": candidate_aggregate,
        "baseline_activation_aggregate": baseline_activation.get("aggregate"),
        "candidate_activation_aggregate": candidate_activation.get("aggregate"),
        "gates": gates,
        "failures": failures,
    }
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    args.markdown_out.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_out.write_text(markdown(report), encoding="utf-8")
    print(json.dumps({"eligible": report["eligible"], "failure_count": len(failures)}, sort_keys=True))
    return 0 if report["eligible"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
