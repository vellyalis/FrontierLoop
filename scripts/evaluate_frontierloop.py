#!/usr/bin/env python3
"""Deterministic FrontierLoop static and baseline/candidate evaluator."""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from pathlib import Path

IMPLICIT = {"frontier-core","frontier-architecture","frontier-debug-investigation","frontier-security-review","frontier-performance-engineering","frontier-portfolio","frontier-recovery"}
FORBIDDEN = {"vh.exe","mission.db","events.db","frontierloop.db"}

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def stable_hash(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",",":"), ensure_ascii=False).encode()).hexdigest()

def frontmatter(text: str):
    match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not match: raise ValueError("missing YAML frontmatter")
    data = {}
    for line in match.group(1).splitlines():
        found = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if found: data[found.group(1)] = found.group(2).strip().strip("\"'")
    if not data.get("name") or not data.get("description"): raise ValueError("frontmatter requires name and description")
    return data

def implicit_policy(text: str) -> bool:
    hits = re.findall(r"(?mi)^\s*allow_implicit_invocation:\s*(true|false)\s*$", text)
    if len(hits) != 1: raise ValueError("allow_implicit_invocation must occur exactly once")
    return hits[0].lower() == "true"

def search(pattern: str, text: str) -> bool:
    try: return re.search(pattern, text, re.I | re.S) is not None
    except re.error as exc: raise ValueError(f"invalid capability regex {pattern!r}: {exc}")

def evaluate_capabilities(root: Path, benchmark: dict, skills: set[str], full_text: str):
    results = []
    for cap in benchmark.get("capabilities", []):
        attempts = []
        for alt in cap.get("alternatives", []):
            missing_skills = [x for x in alt.get("required_skills_all", []) if x not in skills]
            path_keys = ("required_paths_all", "required_source_paths_all")
            paths = [p for key in path_keys for p in alt.get(key, [])]
            missing_paths = [p for p in paths if not (root / p).is_file()]
            relevant = full_text
            present_paths = [root / p for p in paths if (root / p).is_file()]
            if present_paths:
                relevant = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in present_paths)
            patterns = list(alt.get("required_text_all", [])) + list(alt.get("required_source_text_all", []))
            missing_text = [p for p in patterns if not search(p, relevant)]
            passed = not (missing_skills or missing_paths or missing_text)
            attempts.append({"passed":passed,"missing_skills":missing_skills,"missing_paths":missing_paths,"missing_text":missing_text})
        passed = any(a["passed"] for a in attempts)
        results.append({"id":cap["id"],"class":cap["class"],"description":cap.get("description",""),"passed":passed,"alternatives":attempts})
    return results

def validate_root(root: Path, role="candidate", benchmark_override=None, user_skills_root=None):
    root = root.resolve(); errors=[]; skill_rows=[]; files={}
    try:
        for path in sorted(p for p in root.rglob("*") if p.is_file()):
            rel=path.relative_to(root).as_posix(); files[rel]=path.read_text(encoding="utf-8",errors="replace")
    except Exception as exc: errors.append(f"file inventory: {exc}")
    skill_root=root/"skills"; dirs=[]
    if skill_root.is_dir(): dirs=sorted(p for p in skill_root.iterdir() if p.is_dir() and (p/"SKILL.md").is_file())
    for directory in dirs:
        try:
            meta=frontmatter((directory/"SKILL.md").read_text(encoding="utf-8"))
            if meta["name"] != directory.name: raise ValueError(f"name {meta['name']!r} != directory")
            policy_path=directory/"agents"/"openai.yaml"
            if not policy_path.is_file(): raise ValueError("missing agents/openai.yaml")
            skill_rows.append({"name":directory.name,"description":meta["description"],"implicit":implicit_policy(policy_path.read_text(encoding="utf-8"))})
        except Exception as exc: errors.append(f"skill {directory.name}: {exc}")
    names={x["name"] for x in skill_rows}; implicit={x["name"] for x in skill_rows if x["implicit"]}
    if len(skill_rows)!=23: errors.append(f"skill count {len(skill_rows)} != 23")
    if implicit!=IMPLICIT: errors.append(f"implicit set mismatch: {sorted(implicit)}")
    manifest=benchmark=cases=schema={}; readme=routing=""; version="unknown"
    required={"manifest":root/".codex-plugin"/"plugin.json","README":root/"README.md","routing":root/"references"/"ROUTING_MATRIX.md","benchmark":root/"evaluation"/"improvement-benchmark.json","cases":root/"evaluation"/"live-benchmark-cases.json","schema":root/"evaluation"/"live-benchmark-response.schema.json"}
    for label,path in required.items():
        if not path.is_file(): errors.append(f"missing {path.relative_to(root).as_posix()}")
    try: manifest=load_json(required["manifest"]);version=str(manifest.get("version","unknown"))
    except Exception as exc: errors.append(f"plugin manifest: {exc}")
    try: readme=required["README"].read_text(encoding="utf-8")
    except Exception as exc: errors.append(f"README: {exc}")
    try: routing=required["routing"].read_text(encoding="utf-8")
    except Exception as exc: errors.append(f"routing matrix: {exc}")
    try: benchmark=load_json(required["benchmark"])
    except Exception as exc: errors.append(f"improvement benchmark: {exc}")
    try: cases=load_json(required["cases"])
    except Exception as exc: errors.append(f"live cases: {exc}")
    try: schema=load_json(required["schema"])
    except Exception as exc: errors.append(f"response schema: {exc}")
    case_list=cases.get("cases",[]) if isinstance(cases,dict) else []
    case_ids=[x.get("id") for x in case_list if isinstance(x,dict)]
    if len(case_ids)!=len(set(case_ids)): errors.append("live case IDs are not unique")
    bounds=schema.get("properties",{}).get("cases",{}) if isinstance(schema,dict) else {}
    if bounds.get("minItems")!=len(case_list) or bounds.get("maxItems")!=len(case_list): errors.append(f"response schema count {bounds.get('minItems')}/{bounds.get('maxItems')} != {len(case_list)}")
    item_props=bounds.get("items",{}).get("properties",{}) if isinstance(bounds,dict) else {}
    schema_caps=set(item_props.get("selected_capabilities",{}).get("items",{}).get("enum",[]))
    schema_decisions=set(item_props.get("decision",{}).get("enum",[]))
    case_caps=set(cases.get("capability_vocabulary",[])) if isinstance(cases,dict) else set()
    case_decisions=set(cases.get("decision_vocabulary",[])) if isinstance(cases,dict) else set()
    if schema_caps!=case_caps: errors.append("response schema capability vocabulary differs from live cases")
    if schema_decisions!=case_decisions: errors.append("response schema decision vocabulary differs from live cases")
    for row in case_list:
        if not set(row.get("expected_capabilities",[]))<=case_caps: errors.append(f"live case {row.get('id')} uses an unknown capability")
        if row.get("expected_decision") not in case_decisions: errors.append(f"live case {row.get('id')} uses an unknown decision")
    implicit_section=""
    match=re.search(r"(?ms)^## Implicit set\s*(.*?)(?=^## Explicit-only set)",routing)
    if match: implicit_section=match.group(1)
    else: errors.append("routing matrix lacks bounded implicit set section")
    routed=set(re.findall(r"frontier-[a-z0-9-]+",implicit_section))
    if routed!=IMPLICIT: errors.append(f"routing implicit names mismatch: {sorted(routed)}")
    explicit_section=""
    match=re.search(r"(?ms)^## Explicit-only set\s*(.*?)(?=^## )",routing)
    if match: explicit_section=match.group(1)
    explicit_routed=set(re.findall(r"frontier-[a-z0-9-]+",explicit_section))
    all_text="\n".join(files.values())
    effective_benchmark=benchmark_override or benchmark
    capabilities=evaluate_capabilities(root,effective_benchmark,names,all_text) if effective_benchmark else []
    gate=(effective_benchmark or {}).get("promotion_gate",{})
    manifest_count=sum(1 for p in root.rglob("plugin.json") if p.parent.name==".codex-plugin")
    forbidden=[p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file() and (p.name.lower() in FORBIDDEN or p.suffix.lower() in {".sqlite",".sqlite3"})]
    guardrails={
      "no-forbidden-runtime-files":not forbidden,
      "no-plugin-agents-md":not any(p.is_file() for p in root.rglob("AGENTS.md")),
      "implicit-skill-budget":len(implicit)<=int(gate.get("maximum_implicit_skills",7)),
      "routing-contract-floor":len(explicit_routed)>=int(gate.get("minimum_routing_contracts",16)),
      "no-automatic-mutation-contract":bool(re.search(r"never automatically modifies",readme,re.I) and re.search(r"automatic recovery",files.get("references/RUNTIME_BOUNDARY.md",""),re.I)),
      "one-plugin-manifest":manifest_count==1,
    }
    links=[]
    if user_skills_root:
        user=Path(user_skills_root); entries=sorted(p for p in user.glob("frontier-*")) if user.is_dir() else []
        if [p.name for p in entries]!=sorted(names): errors.append("user skill frontier-* entry set differs from canonical")
        for entry in entries:
            target=(skill_root/entry.name).resolve(); resolved=entry.resolve()
            ok=resolved==target
            links.append({"name":entry.name,"resolved":str(resolved),"expected":str(target),"ok":ok,"is_symlink":entry.is_symlink()})
            if not ok: errors.append(f"user skill link target mismatch: {entry.name}")
    retained_fail=[x["id"] for x in capabilities if x["class"]=="retained" and not x["passed"]]
    candidate_fail=[x["id"] for x in capabilities if x["class"]=="candidate" and not x["passed"]]
    invalid_caps=retained_fail + (candidate_fail if role=="candidate" else [])
    failed_guards=[k for k,v in guardrails.items() if not v]
    if failed_guards: errors.append("guardrail failure: "+", ".join(failed_guards))
    if invalid_caps: errors.append(f"{role} capability failure: "+", ".join(invalid_caps))
    implicit_bytes=sum((skill_root/n/"SKILL.md").stat().st_size+(skill_root/n/"agents"/"openai.yaml").stat().st_size for n in implicit if (skill_root/n/"SKILL.md").is_file() and (skill_root/n/"agents"/"openai.yaml").is_file())
    return {"role":role,"root":str(root),"valid":not errors,"version":version,"skill_counts":{"total":len(skill_rows),"implicit":len(implicit),"explicit":len(skill_rows)-len(implicit)},"implicit_names":sorted(implicit),"implicit_catalog_bytes":implicit_bytes,"case_count":len(case_list),"case_ids":case_ids,"capabilities":capabilities,"guardrails":guardrails,"link_status":links,"errors":errors}

def compare(candidate,baseline,gate):
    cp={x["id"]:x for x in candidate["capabilities"]};bp={x["id"]:x for x in baseline["capabilities"]}
    retained_regressions=sorted(k for k,v in cp.items() if v["class"]=="retained" and bp.get(k,{}).get("passed") and not v["passed"])
    gains=sorted(k for k,v in cp.items() if v["passed"] and not bp.get(k,{}).get("passed",False))
    candidate_fail=sorted(k for k,v in cp.items() if v["class"]=="candidate" and not v["passed"])
    baseline_retained_ok=not any(x["class"]=="retained" and not x["passed"] for x in baseline["capabilities"])
    candidate_retained_ok=not any(x["class"]=="retained" and not x["passed"] for x in candidate["capabilities"])
    candidate_caps_ok=not candidate_fail
    candidate_guards_ok=all(candidate["guardrails"].values())
    eligible=(not gate.get("require_all_retained_capabilities_in_baseline",True) or baseline_retained_ok) and (not gate.get("require_all_retained_capabilities_in_candidate",True) or candidate_retained_ok) and (not gate.get("require_all_candidate_capabilities",True) or candidate_caps_ok) and (not gate.get("require_all_candidate_guardrails",True) or candidate_guards_ok) and not retained_regressions and len(gains)>=int(gate.get("minimum_capability_gain",0))
    return {"retained_capability_regressions":retained_regressions,"candidate_gains":gains,"implicit_count_delta":candidate["skill_counts"]["implicit"]-baseline["skill_counts"]["implicit"],"implicit_catalog_bytes_delta":candidate["implicit_catalog_bytes"]-baseline["implicit_catalog_bytes"],"version_delta":{"baseline":baseline["version"],"candidate":candidate["version"]},"promotion_eligible":eligible}

def markdown(report):
    c=report["candidate"];lines=["# FrontierLoop static evaluation","",f"Overall: {'Pass' if c['valid'] else 'Fail'}",f"Version: {c['version']}",f"Skills: {c['skill_counts']['total']} ({c['skill_counts']['implicit']} implicit, {c['skill_counts']['explicit']} explicit)",f"Implicit catalog bytes: {c['implicit_catalog_bytes']}","","## Capabilities"]
    lines += [f"- {'Pass' if x['passed'] else 'Fail'}: {x['id']} ({x['class']})" for x in c["capabilities"]]
    lines += ["","## Guardrails"]+[f"- {'Pass' if v else 'Fail'}: {k}" for k,v in c["guardrails"].items()]
    if c["errors"]: lines += ["","## Errors"]+[f"- {x}" for x in c["errors"]]
    if "comparison" in report:
        x=report["comparison"];lines += ["","## Baseline comparison",f"Promotion eligible: {'Pass' if x['promotion_eligible'] else 'Fail'}",f"Candidate gains: {', '.join(x['candidate_gains']) or 'none'}",f"Retained regressions: {', '.join(x['retained_capability_regressions']) or 'none'}",f"Implicit count delta: {x['implicit_count_delta']}",f"Implicit bytes delta: {x['implicit_catalog_bytes_delta']}"]
    return "\n".join(lines)+"\n"

def self_test():
    assert frontmatter("---\nname: x\ndescription: y\n---\n")=={"name":"x","description":"y"}
    assert implicit_policy("policy:\n  allow_implicit_invocation: true\n")
    assert search("a.*c","A b C")
    assert stable_hash({"b":2,"a":1})==stable_hash({"a":1,"b":2})

def main():
    p=argparse.ArgumentParser();p.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument("--baseline-root",type=Path);p.add_argument("--user-skills-root",type=Path);p.add_argument("--json-out",type=Path);p.add_argument("--markdown-out",type=Path);p.add_argument("--self-test",action="store_true");a=p.parse_args()
    if a.self_test:self_test()
    candidate=validate_root(a.root,"candidate",user_skills_root=a.user_skills_root);report={"schema":"frontierloop-static-evaluation/v1","self_test":"Pass" if a.self_test else "NotRun","candidate":candidate}
    ok=candidate["valid"]
    if a.baseline_root:
        benchmark=load_json(a.root/"evaluation"/"improvement-benchmark.json");baseline=validate_root(a.baseline_root,"baseline",benchmark_override=benchmark);report["baseline"]=baseline;report["comparison"]=compare(candidate,baseline,benchmark.get("promotion_gate",{}));ok=ok and report["comparison"]["promotion_eligible"]
    payload=json.dumps(report,indent=2,sort_keys=True,ensure_ascii=False)+"\n"
    if a.json_out:a.json_out.parent.mkdir(parents=True,exist_ok=True);a.json_out.write_text(payload,encoding="utf-8")
    if a.markdown_out:a.markdown_out.parent.mkdir(parents=True,exist_ok=True);a.markdown_out.write_text(markdown(report),encoding="utf-8")
    if not a.json_out:print(payload,end="")
    return 0 if ok else 1
if __name__=="__main__":raise SystemExit(main())
