#!/usr/bin/env python3
"""Build and verify deterministic FrontierLoop release archives."""
from __future__ import annotations
import argparse, datetime, hashlib, json, os, stat, tempfile, zipfile
from pathlib import Path

def is_reparse(path: Path) -> bool:
    try:
        info=path.lstat();return path.is_symlink() or bool(getattr(info,"st_file_attributes",0)&getattr(stat,"FILE_ATTRIBUTE_REPARSE_POINT",0))
    except OSError:return True

def excluded_roots(root: Path, output: Path) -> set[Path]:
    return {(root/".git").resolve(),(root/"provenance").resolve(),(root/"evaluation"/"results").resolve(),output.resolve()}

def excluded(rel: Path, absolute: Path, roots: set[Path], extras: set[Path]) -> bool:
    resolved=absolute.resolve()
    if resolved in roots or resolved in extras:return True
    parts={p.lower() for p in rel.parts}
    name=rel.name.lower()
    return "__pycache__" in parts or name.endswith(".pyc") or name.startswith(".taddkorro-") or name.startswith(".frontier-loop-") or any("backup" in p or p in {"tmp","temp"} for p in parts)

def deterministic_copy(root: Path, output: Path, extra_excluded=()):
    root=root.resolve(); roots=excluded_roots(root,output); extras={Path(x).resolve() for x in extra_excluded}; rows=[]
    for base,dirs,files in os.walk(root,followlinks=False):
        base_path=Path(base)
        dirs[:]=sorted(d for d in dirs if not is_reparse(base_path/d) and not excluded((base_path/d).relative_to(root),base_path/d,roots,extras))
        for name in sorted(files):
            path=base_path/name;rel=path.relative_to(root)
            if is_reparse(path) or excluded(rel,path,roots,extras):continue
            data=path.read_bytes();rows.append((rel.as_posix(),data,hashlib.sha256(data).hexdigest()))
    return sorted(rows,key=lambda x:x[0])

def zip_time(epoch: int):
    dt=datetime.datetime.fromtimestamp(epoch,datetime.timezone.utc)
    if dt.year<1980:dt=datetime.datetime(1980,1,1,tzinfo=datetime.timezone.utc)
    return (dt.year,dt.month,dt.day,dt.hour,dt.minute,dt.second-dt.second%2)

def build(root: Path, output: Path, epoch: int, extra_excluded=()):
    root=root.resolve();output=output.resolve()
    if root==output or output.is_dir():raise ValueError("unsafe output path")
    output.parent.mkdir(parents=True,exist_ok=True)
    rows=deterministic_copy(root,output,extra_excluded)
    manifest_path=root/".codex-plugin"/"plugin.json"
    version=json.loads(manifest_path.read_text(encoding="utf-8"))["version"]
    manifest=json.dumps({"version":version,"files":[{"path":p,"size":len(b),"sha256":h} for p,b,h in rows]},indent=2,sort_keys=True,ensure_ascii=False).encode()+b"\n"
    entries=[(p,b) for p,b,_ in rows]+[("release-manifest.json",manifest)];entries.sort(key=lambda x:x[0])
    with tempfile.NamedTemporaryFile(delete=False,dir=output.parent,prefix=output.name+".tmp-",suffix=".zip") as temporary_file:
        temporary=Path(temporary_file.name)
    try:
        with zipfile.ZipFile(temporary,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
            for name,data in entries:
                info=zipfile.ZipInfo(name,zip_time(epoch));info.compress_type=zipfile.ZIP_DEFLATED;info.create_system=3;info.external_attr=(0o100644<<16)
                archive.writestr(info,data,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
        os.replace(temporary,output)
    finally:
        if temporary.exists():temporary.unlink()
    return {"output":str(output),"files":len(rows),"sha256":hashlib.sha256(output.read_bytes()).hexdigest(),"version":version}

def verify(root: Path, output: Path, epoch: int):
    if not output.is_file():raise ValueError("archive does not exist")
    with tempfile.TemporaryDirectory(prefix="frontier-release-verify-") as td:
        rebuilt=Path(td)/output.name;build(root,rebuilt,epoch,(output,));same=rebuilt.read_bytes()==output.read_bytes()
    if not same:raise ValueError("archive byte verification failed")
    return {"verified":True,"sha256":hashlib.sha256(output.read_bytes()).hexdigest()}

def self_test(test_temp_root: Path | None = None):
    if test_temp_root is not None:test_temp_root.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="frontier-release-test-",dir=test_temp_root) as td:
        root=Path(td)/"root";(root/".codex-plugin").mkdir(parents=True);(root/".codex-plugin"/"plugin.json").write_text('{"version":"test"}',encoding="utf-8");(root/"a.txt").write_bytes(b"a\r\n");(root/"__pycache__").mkdir();(root/"__pycache__"/"x.pyc").write_bytes(b"x");(root/"provenance").mkdir();(root/"provenance"/"source.txt").write_text("developer-only",encoding="utf-8")
        out=root/"release.zip";first=build(root,out,946684800);one=out.read_bytes();second=build(root,out,946684800);two=out.read_bytes();assert one==two
        with zipfile.ZipFile(out) as z:names=z.namelist();assert names==sorted(names) and "release.zip" not in names and not any("__pycache__" in n for n in names) and not any(n.startswith("provenance/") for n in names)
        assert verify(root,out,946684800)["verified"]
    return {"self_test":"Pass"}

def main():
    p=argparse.ArgumentParser();p.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument("--output",type=Path);p.add_argument("--source-date-epoch",type=int,default=946684800);p.add_argument("--verify",action="store_true");p.add_argument("--self-test",action="store_true");p.add_argument("--test-temp-root",type=Path);a=p.parse_args()
    if a.self_test:print(json.dumps(self_test(a.test_temp_root),sort_keys=True));return 0
    if not a.output:p.error("--output is required")
    result=verify(a.root,a.output,a.source_date_epoch) if a.verify else build(a.root,a.output,a.source_date_epoch)
    print(json.dumps(result,sort_keys=True));return 0
if __name__=="__main__":raise SystemExit(main())
