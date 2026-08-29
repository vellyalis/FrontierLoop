#!/usr/bin/env python3
"""Compare FrontierLoop 0.7.0 and 0.8.0 in isolated OpenCode runtimes.

This is a no-cost fallback live lane for periods when Codex CLI quota is not
available.  Both versions run under the same OpenCode binary, free model,
prompts, and isolated project configuration.  The user's active Skill
junctions are never modified.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


IMPLICIT_SKILLS = {
    "frontier-architecture",
    "frontier-core",
    "frontier-debug-investigation",
    "frontier-performance-engineering",
    "frontier-portfolio",
    "frontier-recovery",
    "frontier-security-review",
}
ACTIVATION_PROBE_SKILLS = IMPLICIT_SKILLS | {"frontier-migration"}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def http_json(url: str, timeout: float = 10.0) -> Any:
    request = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def locate_opencode(explicit: Path | None) -> Path:
    candidates: list[Path | None] = [explicit]
    if os.environ.get("OPENCODE_EXE"):
        candidates.append(Path(os.environ["OPENCODE_EXE"]))
    which = shutil.which("opencode")
    if which:
        candidates.append(Path(which))
    appdata = os.environ.get("APPDATA")
    if appdata:
        candidates.append(Path(appdata) / "npm" / "node_modules" / "opencode-ai" / "bin" / "opencode.exe")
    temp_root = Path(os.environ.get("TEMP", os.environ.get("TMP", ".")))
    candidates.extend(
        sorted(
            temp_root.glob("frontier-opencode-eval-*/node_modules/opencode-ai/bin/opencode.exe"),
            reverse=True,
        )
    )
    for candidate in candidates:
        if candidate and candidate.is_file():
            return candidate.resolve()
    raise SystemExit("OpenCode executable was not found; pass --opencode")


def create_isolated_project(
    source: Path, destination: Path, *, selected_skills: set[str] | None = None
) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    (destination / ".opencode").mkdir(parents=True)
    target_skills = destination / ".opencode" / "skills"
    target_skills.mkdir(parents=True)
    for skill_dir in sorted((source / "skills").iterdir()):
        if not skill_dir.is_dir() or not (skill_dir / "SKILL.md").is_file():
            continue
        if selected_skills is not None and skill_dir.name not in selected_skills:
            continue
        shutil.copytree(skill_dir, target_skills / skill_dir.name)
    config = {
        "$schema": "https://opencode.ai/config.json",
        "permission": {
            "edit": "deny",
            "bash": "deny",
            "task": "deny",
            "question": "deny",
            "skill": "allow",
            "read": "allow",
            "glob": "deny",
            "grep": "deny",
            "list": "deny",
        },
        "lsp": False,
        "formatter": False,
        "agent": {
            "frontier-probe": {
                "description": "Read-only FrontierLoop activation probe with a bounded tool budget.",
                "mode": "primary",
                "steps": 10,
                "prompt": (
                    "You are a read-only routing evaluator. Decide only from the supplied request, "
                    "the selected FrontierLoop Skill bodies, and their referenced Doctrine. Use "
                    "only the skill tool, reads inside .opencode/skills, and at most one read of "
                    "the .opencode catalog root when resolving a referenced Skill path. Do not inspect the "
                    "project, search for repository facts, edit files, run shell commands, "
                    "delegate, or ask questions. Finish with the requested JSON before the step "
                    "budget ends."
                ),
                "permission": {
                    "edit": "deny",
                    "bash": "deny",
                    "task": "deny",
                    "question": "deny",
                    "skill": "allow",
                    "read": "allow",
                    "glob": "deny",
                    "grep": "deny",
                    "list": "deny"
                }
            }
        }
    }
    dump(destination / "opencode.json", config)


class Server:
    def __init__(
        self,
        *,
        executable: Path,
        project: Path,
        home: Path,
        log_path: Path,
        timeout: float,
    ) -> None:
        self.project = project.resolve()
        self.home = home.resolve()
        self.log_path = log_path.resolve()
        self.port = free_port()
        self.endpoint = f"http://127.0.0.1:{self.port}"
        self.timeout = timeout
        self.process: subprocess.Popen[str] | None = None
        self._log_handle = None
        self.executable = executable

    def start(self) -> None:
        self.home.mkdir(parents=True, exist_ok=True)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        env = os.environ.copy()
        env["USERPROFILE"] = str(self.home)
        env["HOME"] = str(self.home)
        env["OPENCODE_PURE"] = "1"
        env["OPENCODE_DISABLE_DEFAULT_PLUGINS"] = "1"
        env["OPENCODE_DISABLE_EXTERNAL_SKILLS"] = "1"
        self._log_handle = self.log_path.open("w", encoding="utf-8")
        self.process = subprocess.Popen(
            [
                str(self.executable),
                "serve",
                "--pure",
                "--hostname",
                "127.0.0.1",
                "--port",
                str(self.port),
            ],
            cwd=self.project,
            env=env,
            stdout=self._log_handle,
            stderr=subprocess.STDOUT,
            text=True,
            shell=False,
        )
        deadline = time.monotonic() + self.timeout
        last_error: Exception | None = None
        while time.monotonic() < deadline:
            if self.process.poll() is not None:
                break
            try:
                health = http_json(f"{self.endpoint}/global/health", timeout=2.0)
                if isinstance(health, dict) and health.get("healthy"):
                    return
            except (OSError, urllib.error.URLError, json.JSONDecodeError) as exc:
                last_error = exc
            time.sleep(0.25)
        excerpt = ""
        if self.log_path.is_file():
            excerpt = self.log_path.read_text(encoding="utf-8", errors="replace")[-4096:]
        raise RuntimeError(
            f"OpenCode server did not become healthy; last={last_error!r}; log={excerpt}"
        )

    def stop(self) -> None:
        if self.process and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=15)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait(timeout=10)
        if self._log_handle:
            self._log_handle.close()


def validate_catalog(
    endpoint: str, project: Path, *, expected_names: set[str]
) -> dict[str, Any]:
    skills = http_json(f"{endpoint}/skill", timeout=30.0)
    if not isinstance(skills, list):
        raise RuntimeError("OpenCode /skill did not return an array")
    frontier = [row for row in skills if isinstance(row, dict) and str(row.get("name", "")).startswith("frontier-")]
    names = sorted(str(row["name"]) for row in frontier)
    locations = {str(row["name"]): str(row.get("location", "")) for row in frontier}
    expected_root = str((project / ".opencode" / "skills").resolve()).lower()
    bad_locations = {
        name: location
        for name, location in locations.items()
        if not location.lower().startswith(expected_root)
    }
    if set(names) != expected_names or len(set(names)) != len(expected_names) or bad_locations:
        raise RuntimeError(
            f"isolated FrontierLoop catalog invalid: count={len(frontier)}, "
            f"unique={len(set(names))}, expected={sorted(expected_names)}, "
            f"bad_locations={bad_locations}"
        )
    return {"frontier_skill_count": len(frontier), "names": names, "locations": locations}


def run_checked(command: list[str], *, cwd: Path, timeout: float) -> None:
    process = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True,
        timeout=timeout,
        shell=False,
    )
    if process.returncode:
        raise RuntimeError(
            f"command failed ({process.returncode}): {' '.join(command)}\n"
            f"stdout={process.stdout[-4096:]}\nstderr={process.stderr[-4096:]}"
        )


def evaluate_activation(report: dict[str, Any]) -> dict[str, Any]:
    failures: list[dict[str, Any]] = []
    for row in report.get("rows", []):
        if row.get("error") or not isinstance(row.get("response"), dict):
            failures.append(
                {
                    "trial": row.get("trial"),
                    "id": row.get("id"),
                    "reasons": ["probe-execution"],
                    "error": row.get("error"),
                }
            )
            continue
        expected = row["expected"]
        response = row["response"]
        metrics = row["metrics"]
        required = set(expected["required_selected_skills"])
        optional = set(expected.get("allowed_optional_selected_skills", []))
        selected = set(response["selected_skills"])
        reads = set(row["activation_evidence"]["execution_skill_reads"])
        expected_doctrine = bool(expected["engineering_judgment_applied"])
        doctrine_read = bool(metrics["doctrine_reference_observed"])
        reasons: list[str] = []
        if not metrics["decision_correct"]:
            reasons.append("decision")
        if not required.issubset(reads) or not reads.issubset(required | optional):
            reasons.append("successful-read-set")
        if not selected.issubset(reads):
            reasons.append("unread-self-report")
        if not metrics["doctrine_correct"]:
            reasons.append("doctrine-self-report")
        if doctrine_read != expected_doctrine:
            reasons.append("doctrine-observation")
        if metrics.get("out_of_scope_read_count", 0) > 0:
            reasons.append("out-of-scope-read")
        if reasons:
            failures.append(
                {
                    "trial": row["trial"],
                    "id": row["id"],
                    "reasons": reasons,
                    "expected_decision": expected["decision"],
                    "accepted_decisions": expected.get(
                        "accepted_decisions", [expected["decision"]]
                    ),
                    "actual_decision": response["decision"],
                    "required_skills": sorted(required),
                    "allowed_optional_skills": sorted(optional),
                    "selected_skills": sorted(selected),
                    "successful_skill_reads": sorted(reads),
                    "expected_doctrine": expected_doctrine,
                    "observed_doctrine_read": doctrine_read,
                    "out_of_scope_reads": row["activation_evidence"].get(
                        "out_of_scope_read_paths", []
                    ),
                }
            )
    return {
        "pass": not failures,
        "failure_count": len(failures),
        "failures": failures,
    }


def run_version(
    *,
    root: Path,
    source: Path,
    label: str,
    executable: Path,
    model: str,
    batch_trials: int,
    activation_trials: int,
    attempts: int,
    run_batch: bool,
    activation_cases: list[str],
    timeout: float,
) -> dict[str, Any]:
    runtime_root = root / "evaluation" / "results" / "opencode-runtime" / label
    project = runtime_root / "project"
    home = runtime_root / "home"
    selected_catalog = None if run_batch else ACTIVATION_PROBE_SKILLS
    create_isolated_project(source, project, selected_skills=selected_catalog)
    if home.exists():
        shutil.rmtree(home)
    server = Server(
        executable=executable,
        project=project,
        home=home,
        log_path=runtime_root / "server.log",
        timeout=60.0,
    )
    server.start()
    try:
        expected_names = (
            {
                path.name
                for path in (source / "skills").iterdir()
                if path.is_dir() and (path / "SKILL.md").is_file()
            }
            if selected_catalog is None
            else set(selected_catalog)
        )
        catalog = validate_catalog(
            server.endpoint, project, expected_names=expected_names
        )
        wrapper = root / "scripts" / "opencode_final_json_wrapper.py"
        batch_trace = root / "evaluation" / "results" / "activation-traces" / f"opencode-batch-{label}"
        activation_trace = root / "evaluation" / "results" / "activation-traces" / f"opencode-engineering-{label}"
        shutil.rmtree(batch_trace, ignore_errors=True)
        shutil.rmtree(activation_trace, ignore_errors=True)
        batch_output = root / "evaluation" / "results" / f"live-opencode-{label}.json"
        activation_output = root / "evaluation" / "results" / f"engineering-activation-opencode-{label}.json"
        if run_batch:
            wrapper_command = (
                f"{sys.executable} {wrapper} --endpoint {server.endpoint} "
                f"--cwd {project} --trace-dir {batch_trace} --timeout {timeout} --model {model}"
            )
            run_checked(
                [
                    sys.executable,
                    str(root / "scripts" / "run_live_benchmark.py"),
                    "--root",
                    str(root),
                    "--label",
                    label,
                    "--trials",
                    str(batch_trials),
                    "--timeout",
                    str(timeout + 30),
                    "--command",
                    wrapper_command,
                    "--output",
                    str(batch_output),
                ],
                cwd=root,
                timeout=(timeout + 60) * batch_trials,
            )
        activation_command = [
            sys.executable,
            str(root / "scripts" / "run_engineering_judgment_activation.py"),
            "--root",
            str(root),
            "--cwd",
            str(project),
            "--trials",
            str(activation_trials),
            "--attempts",
            str(attempts),
            "--timeout",
            str(timeout),
            "--trace-dir",
            str(activation_trace),
            "--output",
            str(activation_output),
            "--label",
            label,
            "--wrapper",
            str(wrapper),
            "--wrapper-arg=--endpoint",
            f"--wrapper-arg={server.endpoint}",
            "--wrapper-arg=--model",
            f"--wrapper-arg={model}",
            "--wrapper-arg=--agent",
            "--wrapper-arg=frontier-probe",
        ]
        for case_id in activation_cases:
            activation_command.extend(["--case", case_id])
        run_checked(
            activation_command,
            cwd=root,
            timeout=(timeout + 60) * activation_trials * 10,
        )
        batch = load(batch_output) if run_batch else None
        activation = load(activation_output)
        return {
            "label": label,
            "source": str(source),
            "server_endpoint": server.endpoint,
            "catalog": catalog,
            "batch_output": str(batch_output) if run_batch else None,
            "batch_aggregate": batch.get("aggregate") if batch else None,
            "activation_output": str(activation_output),
            "activation_aggregate": activation.get("aggregate"),
            "activation_gate": evaluate_activation(activation),
        }
    finally:
        server.stop()


def main() -> int:
    parser = argparse.ArgumentParser()
    root_default = Path(__file__).resolve().parents[1]
    parser.add_argument("--root", type=Path, default=root_default)
    parser.add_argument(
        "--baseline-source",
        type=Path,
        default=Path.home() / ".codex" / "plugins" / "cache" / "personal" / "frontier-loop" / "0.7.0",
    )
    parser.add_argument("--candidate-source", type=Path, default=root_default)
    parser.add_argument("--opencode", type=Path)
    parser.add_argument("--model", default="opencode/big-pickle")
    parser.add_argument("--batch-trials", type=int, default=3)
    parser.add_argument("--activation-trials", type=int, default=3)
    parser.add_argument("--attempts", type=int, default=3)
    parser.add_argument(
        "--only",
        choices=("baseline", "candidate", "both"),
        default="both",
        help="Run only one version or both matched versions.",
    )
    parser.add_argument(
        "--activation-case",
        action="append",
        default=[],
        help="Limit the activation lane to one case ID; repeat as needed.",
    )
    parser.add_argument(
        "--run-batch",
        action="store_true",
        help="Also run the 23-case strict batch schema lane. Disabled by default because the activation lane is the decisive live evidence.",
    )
    parser.add_argument("--timeout", type=float, default=180.0)
    parser.add_argument(
        "--output",
        type=Path,
        default=root_default / "evaluation" / "results" / "opencode-0.7.0-vs-0.8.0-summary.json",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    baseline = args.baseline_source.resolve()
    candidate = args.candidate_source.resolve()
    executable = locate_opencode(args.opencode)
    if not (baseline / "skills").is_dir():
        raise SystemExit(f"baseline Skills missing: {baseline}")
    if not (candidate / "skills").is_dir():
        raise SystemExit(f"candidate Skills missing: {candidate}")
    if args.batch_trials < 1 or args.activation_trials < 1 or args.attempts < 1:
        raise SystemExit("trial counts must be positive")

    baseline_report = None
    candidate_report = None
    if args.only in {"baseline", "both"}:
        baseline_report = run_version(
            root=root,
            source=baseline,
            label="baseline-0.7.0",
            executable=executable,
            model=args.model,
            batch_trials=args.batch_trials,
            activation_trials=args.activation_trials,
            attempts=args.attempts,
            run_batch=args.run_batch,
            activation_cases=args.activation_case,
            timeout=args.timeout,
        )
    if args.only in {"candidate", "both"}:
        candidate_report = run_version(
            root=root,
            source=candidate,
            label="candidate-0.8.0",
            executable=executable,
            model=args.model,
            batch_trials=args.batch_trials,
            activation_trials=args.activation_trials,
            attempts=args.attempts,
            run_batch=args.run_batch,
            activation_cases=args.activation_case,
            timeout=args.timeout,
        )

    summary = {
        "schema": "frontierloop-opencode-version-comparison/v1",
        "opencode": str(executable),
        "opencode_version": subprocess.check_output(
            [str(executable), "--version"], text=True, timeout=30
        ).strip(),
        "model": args.model,
        "batch_trials": args.batch_trials,
        "activation_trials": args.activation_trials,
        "attempts": args.attempts,
        "batch_lane_run": args.run_batch,
        "only": args.only,
        "activation_cases": args.activation_case,
        "baseline": baseline_report,
        "candidate": candidate_report,
        "candidate_pass": (
            bool(candidate_report["activation_gate"]["pass"])
            if candidate_report is not None
            else None
        ),
        "active_user_skill_junctions_modified": False,
    }
    dump(args.output, summary)
    print(json.dumps(summary, sort_keys=True, ensure_ascii=False))
    selected_reports = [report for report in (baseline_report, candidate_report) if report]
    return 0 if selected_reports and all(report["activation_gate"]["pass"] for report in selected_reports) else 1


if __name__ == "__main__":
    raise SystemExit(main())
