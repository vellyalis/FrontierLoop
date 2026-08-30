#!/usr/bin/env python3
"""Synchronize recorded active Skill hashes with canonical FrontierLoop files."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    args = parser.parse_args()
    root = args.root.resolve()
    source_map_path = root / "references" / "SKILL_SOURCE_MAP.json"
    source_map = json.loads(source_map_path.read_text(encoding="utf-8"))

    changed: list[dict[str, str]] = []
    for row in source_map.get("skills", []):
        name = row.get("active_name")
        if not isinstance(name, str) or not name:
            raise SystemExit("SKILL_SOURCE_MAP row lacks active_name")
        skill_path = root / "skills" / name / "SKILL.md"
        if not skill_path.is_file():
            raise SystemExit(f"Mapped active Skill is missing: {name}")
        actual = sha256(skill_path)
        previous = row.get("active_sha256")
        if previous != actual:
            row["active_sha256"] = actual
            changed.append(
                {"skill": name, "previous": str(previous), "actual": actual}
            )

    source_map_path.write_text(
        json.dumps(source_map, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {"changed_count": len(changed), "changed": changed},
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
