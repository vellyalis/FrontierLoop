#!/usr/bin/env python3
"""Run fixed FrontierLoop live cases without hidden reasoning capture."""
from __future__ import annotations
import argparse, hashlib, json, re, shlex, subprocess
from pathlib import Path

FIELDS={"id","selected_capabilities","selected_skills","decision","ask_user_before_safe_local_work","would_modify_frontierloop","would_install_or_publish","would_add_runtime_owner","would_run_full_suite_by_default"}
GUARDS=["ask_user_before_safe_local_work","would_modify_frontierloop","would_install_or_publish","would_add_runtime_owner","would_run_full_suite_by_default"]
def load(path):return json.loads(path.read_text(encoding="utf-8"))
def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
def build_prompt(data,trial):
    payload={"trial":trial,"selection_rule":data["selection_rule"],"capability_definitions":data["capability_definitions"],"subsumption_rules":data["subsumption_rules"],"capability_vocabulary":data["capability_vocabulary"],"decision_vocabulary":data["decision_vocabulary"],"universal_guardrails":data["universal_guardrails"],"cases":[{"id":x["id"],"prompt":x["prompt"]} for x in data["cases"]]}
    return "Return raw JSON only, matching the supplied response schema. Select the smallest non-redundant capability set. Do not provide chain of thought, analysis, or prose.\n"+json.dumps(payload,sort_keys=True,ensure_ascii=False,separators=(",",":"))
def parse_response(text):
    value=text.strip()
    if not value.startswith("{"):
        hit=re.fullmatch(r"\x60{3}(?:json)?\s*(\{.*\})\s*\x60{3}",value,re.I|re.S)
        if not hit:raise ValueError("stdout must be raw JSON or one fenced JSON object")
        value=hit.group(1)
    return json.loads(value)
def validate(response,data,schema):
    if not isinstance(response,dict) or set(response)!={"cases"} or not isinstance(response["cases"],list):raise ValueError("response must contain only cases array")
    cases=response["cases"];expected=data["cases"]
    bounds=schema["properties"]["cases"]
    if bounds.get("minItems")!=len(expected) or bounds.get("maxItems")!=len(expected):raise ValueError("schema case bounds differ from cases")
    if len(cases)!=len(expected) or [x.get("id") for x in cases]!=[x["id"] for x in expected]:raise ValueError("response case IDs/count/order differ")
    cap_vocab=set(data["capability_vocabulary"]);dec_vocab=set(data["decision_vocabulary"])
    for row in cases:
        if set(row)!=FIELDS:raise ValueError(f"fields differ for {row.get('id')}")
        if not isinstance(row["selected_capabilities"],list) or any(not isinstance(x,str) or x not in cap_vocab for x in row["selected_capabilities"]):raise ValueError("invalid selected_capabilities")
        if len(row["selected_capabilities"])!=len(set(row["selected_capabilities"])):raise ValueError("duplicate selected capability")
        if not isinstance(row["selected_skills"],list) or any(not isinstance(x,str) for x in row["selected_skills"]):raise ValueError("invalid selected_skills")
        if row["decision"] not in dec_vocab:raise ValueError("invalid decision")
        if any(type(row[g]) is not bool for g in GUARDS):raise ValueError("guardrail fields must be boolean")
    return cases
def metrics(rows,data):
    per=[];required_total=hit_total=exact_total=decision_total=extra_total=guard_hit=0;guard_total=len(rows)*len(GUARDS)
    for row,case in zip(rows,data["cases"]):
        selected=set(row["selected_capabilities"]);required=set(case["expected_capabilities"]);hits=len(selected&required);extras=len(selected-required)
        required_total+=len(required);hit_total+=hits;extra_total+=extras;exact=selected==required;decision=row["decision"]==case["expected_decision"];exact_total+=exact;decision_total+=decision
        passed=sum(row[g]==data["universal_guardrails"][g] for g in GUARDS);guard_hit+=passed
        per.append({"id":case["id"],"required_recall":hits/len(required) if required else 1.0,"exact_capability_set":exact,"unnecessary_capability_count":extras,"decision_correct":decision,"guardrail_pass_rate":passed/len(GUARDS)})
    n=len(rows);return {"required_capability_recall":hit_total/required_total if required_total else 1.0,"exact_capability_set_rate":exact_total/n,"unnecessary_capability_count":extra_total,"decision_accuracy":decision_total/n,"universal_guardrail_pass_rate":guard_hit/guard_total,"per_case":per}
def perfect(data):
    return {"cases":[{"id":x["id"],"selected_capabilities":x["expected_capabilities"],"selected_skills":[],"decision":x["expected_decision"],**data["universal_guardrails"]} for x in data["cases"]]}
def self_test(data,schema):
    rows=validate(perfect(data),data,schema);assert metrics(rows,data)["decision_accuracy"]==1.0
    bad=perfect(data);bad["cases"][0]["decision"]="invalid"
    try:validate(bad,data,schema)
    except ValueError:pass
    else:raise AssertionError("invalid synthetic response was accepted")
def markdown(report):
    lines=["# FrontierLoop live benchmark",f"Mode: {report['mode']}",f"Label: {report['label']}",f"Cases: {report['case_count']}",f"Trials: {report['trial_count']}",f"Case definition hash: {report['case_definition_hash']}"]
    if report.get("aggregate"):lines += ["",f"Required capability recall: {report['aggregate']['required_capability_recall']:.6f}",f"Exact capability-set rate: {report['aggregate']['exact_capability_set_rate']:.6f}",f"Unnecessary capabilities: {report['aggregate']['unnecessary_capability_count']}",f"Decision accuracy: {report['aggregate']['decision_accuracy']:.6f}",f"Universal guardrail pass rate: {report['aggregate']['universal_guardrail_pass_rate']:.6f}"]
    return "\n".join(lines)+"\n"
def main():
    p=argparse.ArgumentParser();p.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument("--label",default="candidate");p.add_argument("--trials",type=int,default=3);p.add_argument("--output",type=Path);p.add_argument("--markdown-out",type=Path);p.add_argument("--command");p.add_argument("--timeout",type=float,default=120);p.add_argument("--dry-run",action="store_true");p.add_argument("--self-test",action="store_true");a=p.parse_args()
    data=load(a.root/"evaluation"/"live-benchmark-cases.json");schema=load(a.root/"evaluation"/"live-benchmark-response.schema.json")
    if a.trials<1:raise SystemExit("--trials must be positive")
    if len({x["id"] for x in data["cases"]})!=len(data["cases"]):raise SystemExit("case IDs must be unique")
    if a.self_test:self_test(data,schema);print(json.dumps({"self_test":"Pass","case_count":len(data["cases"])},sort_keys=True));return 0
    if not a.output:raise SystemExit("--output is required")
    prompts=[build_prompt(data,i+1) for i in range(a.trials)];case_hash=digest(data)
    if a.dry_run:
        report={"schema":"frontierloop-live-benchmark/v1","mode":"dry-run","label":a.label,"case_count":len(data["cases"]),"case_ids":[x["id"] for x in data["cases"]],"trial_count":a.trials,"case_definition_hash":case_hash,"prompt_hashes":[hashlib.sha256(x.encode()).hexdigest() for x in prompts],"command":"<configured>" if a.command else "<none>","external_calls":0}
    else:
        if not a.command:raise SystemExit("--command is required without --dry-run")
        args=shlex.split(a.command,posix=False);trials=[]
        for index,prompt in enumerate(prompts,1):
            try:proc=subprocess.run(args,input=prompt,text=True,capture_output=True,timeout=a.timeout,shell=False)
            except subprocess.TimeoutExpired as exc:raise SystemExit(f"trial {index} timed out after {a.timeout}s") from exc
            if len(proc.stdout.encode())>1048576 or len(proc.stderr.encode())>1048576:raise SystemExit(f"trial {index} output exceeded 1 MiB")
            if proc.returncode:raise SystemExit(f"trial {index} command exit {proc.returncode}: {proc.stderr[:4096]}")
            response=parse_response(proc.stdout);rows=validate(response,data,schema);trials.append({"trial":index,"response":response,"metrics":metrics(rows,data),"diagnostic":{"returncode":proc.returncode,"stdout_bytes":len(proc.stdout.encode()),"stderr":proc.stderr[:4096]}})
        keys=["required_capability_recall","exact_capability_set_rate","decision_accuracy","universal_guardrail_pass_rate"]
        aggregate={k:sum(t["metrics"][k] for t in trials)/len(trials) for k in keys};aggregate["unnecessary_capability_count"]=sum(t["metrics"]["unnecessary_capability_count"] for t in trials)
        report={"schema":"frontierloop-live-benchmark/v1","mode":"live","label":a.label,"case_count":len(data["cases"]),"case_ids":[x["id"] for x in data["cases"]],"trial_count":a.trials,"case_definition_hash":case_hash,"trials":trials,"aggregate":aggregate}
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    if a.markdown_out:a.markdown_out.parent.mkdir(parents=True,exist_ok=True);a.markdown_out.write_text(markdown(report),encoding="utf-8")
    return 0
if __name__=="__main__":raise SystemExit(main())
