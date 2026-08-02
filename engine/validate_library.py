"""Validate Suno Intelligence record, source, relationship, and facet integrity."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from build_library_catalog import build_catalog


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    library = root / "library"
    model = json.loads((library / "semantic-model.json").read_text(encoding="utf-8"))
    archives = {
        json.loads(line)["id"]
        for line in (library / "references" / "archives.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    }
    records = build_catalog(library)
    by_id = {str(record["id"]): record for record in records}
    errors: list[str] = []
    if len(by_id) != len(records):
        errors.append("duplicate record IDs")
    facets = model["facets"]
    for record in records:
        identifier = str(record["id"])
        for source_id in record.get("source_ids", []):
            if source_id not in archives:
                errors.append(f"{identifier}: unknown archive source {source_id}")
        for name, values in facets.items():
            if name in record and str(record[name]) not in values:
                errors.append(f"{identifier}: invalid {name}={record[name]}")
        if record.get("kind") == "relationship":
            for endpoint in [*record.get("from_ids", []), *record.get("to_ids", [])]:
                if endpoint not in by_id:
                    errors.append(f"{identifier}: unknown relationship endpoint {endpoint}")
    if errors:
        print("Library validation failed:\n" + "\n".join(f"- {error}" for error in errors))
        return 1
    print(f"Library valid: {len(records)} records, {len(archives)} archive references")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

