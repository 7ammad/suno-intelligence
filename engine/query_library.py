"""Query the Suno Intelligence catalog by kind and semantic facets.

Examples:
  python tools/query_library.py --kind voice --facet register=low --facet energy=contained
  python tools/query_library.py --kind sound_source
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def default_catalog(root: Path) -> Path:
    local = root / "library" / "catalog.json"
    return local if local.exists() else root / "engine" / "library" / "catalog-v1.3.json"


def parse_facets(values: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"facet must use key=value: {value}")
        key, expected = value.split("=", 1)
        if not key or not expected:
            raise ValueError(f"facet must use key=value: {value}")
        result[key] = expected
    return result


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=default_catalog(root))
    parser.add_argument("--kind")
    parser.add_argument("--facet", action="append", default=[], help="repeatable key=value semantic filter")
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()
    if args.limit < 1:
        raise ValueError("limit must be positive")
    facets = parse_facets(args.facet)
    catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
    records = catalog["records"]
    if args.kind:
        records = [record for record in records if record.get("kind") == args.kind]
    for key, expected in facets.items():
        records = [record for record in records if str(record.get(key, "")).lower() == expected.lower()]
    rows = records[:args.limit]
    print(json.dumps({"count": len(records), "returned": rows}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

