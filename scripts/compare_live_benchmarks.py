#!/usr/bin/env python3
"""Compare FrontierLoop live benchmark result sets without blended-score masking."""
from __future__ import annotations
import argparse,json
from pathlib import Path
def load(path):return json.loads(path.read_text(encoding="utf-8"))
def case_scores(report):
    out={x:{"required_recall":[],"exact":[],"decision":[],"guards":[],"extras":[]} for x in report["case_ids"]}
    for trial in report.get("trials",[]):
        for row in trial["metrics"]["per_case"]:
            x=out[row["id"]];x["required_recall"].append(row["required_recall"]);x["exact"].append(float(row["exact_capability_set"]));x["decision"].append(float(row["decision_correct"]));x["guards"].append(row["guardrail_pass_rate"]);x["extras"].append(row["unnecessary_capability_count"])
    return {k:{n:sum(v[n])/len(v[n]) for n in v} for k,v in out.items()}
def compare(base,cand):
    if base.get("case_definition_hash")!=cand.get("case_definition_hash"):raise ValueError("case-definition hash mismatch")
    if base.get("case_ids")!=cand.get("case_ids"):raise ValueError("case IDs mismatch")
    b=case_scores(base);c=case_scores(cand);reg=[];gains=[];critical=[]
    for case in base["case_ids"]:
        changes={k:c[case][k]-b[case][k] for k in b[case]}
        if changes["required_recall"]<0 or changes["exact"]<0 or changes["decision"]<0 or changes["guards"]<0 or changes["extras"]>0:reg.append({"id":case,"delta":changes})
        if changes["required_recall"]>0 or changes["exact"]>0 or changes["decision"]>0 or changes["guards"]>0 or changes["extras"]<0:gains.append({"id":case,"delta":changes})
        if c[case]["guards"]<1.0:critical.append(case)
    ba=base["aggregate"];ca=cand["aggregate"]
    required_regression=ca["required_capability_recall"]<ba["required_capability_recall"] or any(x["delta"]["required_recall"]<0 for x in reg)
    eligible=not critical and not required_regression and not reg
    return {"schema":"frontierloop-live-comparison/v1","case_definition_hash":base["case_definition_hash"],"case_count":len(base["case_ids"]),"baseline_metrics":ba,"candidate_metrics":ca,"per_case_regressions":reg,"per_case_gains":gains,"critical_guardrail_violations":critical,"required_capability_regression":required_regression,"adoption_eligible":eligible}
def markdown(x):return "\n".join(["# FrontierLoop live comparison",f"Adoption eligible: {'Pass' if x['adoption_eligible'] else 'Fail'}",f"Cases: {x['case_count']}",f"Regressions: {len(x['per_case_regressions'])}",f"Gains: {len(x['per_case_gains'])}",f"Critical guardrail violations: {len(x['critical_guardrail_violations'])}"])+"\n"
def synthetic(value,guard=1.0):
    per=[{"id":"a","required_recall":value,"exact_capability_set":value==1,"unnecessary_capability_count":0,"decision_correct":value==1,"guardrail_pass_rate":guard}]
    return {"case_definition_hash":"h","case_ids":["a"],"trials":[{"metrics":{"per_case":per}}],"aggregate":{"required_capability_recall":value,"exact_capability_set_rate":value,"unnecessary_capability_count":0,"decision_accuracy":value,"universal_guardrail_pass_rate":guard}}
def self_test():
    assert compare(synthetic(.5),synthetic(1))["adoption_eligible"]
    assert not compare(synthetic(1),synthetic(.5))["adoption_eligible"]
    assert not compare(synthetic(1),synthetic(1,.8))["adoption_eligible"]
def main():
    p=argparse.ArgumentParser();p.add_argument("--baseline",type=Path);p.add_argument("--candidate",type=Path);p.add_argument("--json-out",type=Path);p.add_argument("--markdown-out",type=Path);p.add_argument("--self-test",action="store_true");a=p.parse_args()
    if a.self_test:self_test();print(json.dumps({"self_test":"Pass"},sort_keys=True));return 0
    if not a.baseline or not a.candidate:raise SystemExit("--baseline and --candidate are required")
    result=compare(load(a.baseline),load(a.candidate));payload=json.dumps(result,indent=2,sort_keys=True)+"\n"
    if a.json_out:a.json_out.parent.mkdir(parents=True,exist_ok=True);a.json_out.write_text(payload,encoding="utf-8")
    else:print(payload,end="")
    if a.markdown_out:a.markdown_out.parent.mkdir(parents=True,exist_ok=True);a.markdown_out.write_text(markdown(result),encoding="utf-8")
    return 0 if result["adoption_eligible"] else 1
if __name__=="__main__":raise SystemExit(main())
