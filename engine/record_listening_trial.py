"""Record one human listening decision against a generated composition world.

The output is append-only evidence. It does not fine-tune anything, rewrite
library records, or replace Hammad's next creative decision.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import UTC, datetime
from pathlib import Path


RECORD_ID = re.compile(r"\b(?:grammar|bass|rhythm|sound_source|harmony|melody|form|instrument|voice|lyric)\.[a-z0-9-]+")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--world", type=Path, required=True)
    parser.add_argument("--outcome", choices=("keep", "not-yet", "reject"), required=True)
    parser.add_argument("--reason", action="append", default=[], help="short human reason tag; may be repeated")
    parser.add_argument("--note", default="")
    parser.add_argument("--trials", type=Path, required=True, help="append-only JSONL evidence file")
    args = parser.parse_args()
    if not args.world.is_file():
        raise FileNotFoundError(args.world)
    ids = sorted(set(RECORD_ID.findall(args.world.read_text(encoding="utf-8"))))
    if not ids:
        raise ValueError("world has no identifiable library record IDs")
    reasons = [reason.strip() for reason in args.reason if reason.strip()]
    record = {
        "version": "1.0",
        "recorded_at": datetime.now(UTC).isoformat(),
        "world": str(args.world),
        "outcome": args.outcome,
        "record_ids": ids,
        "reason_tags": reasons,
        "note": args.note.strip(),
    }
    args.trials.parent.mkdir(parents=True, exist_ok=True)
    with args.trials.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(json.dumps({"outcome": args.outcome, "record_count": len(ids), "trials": str(args.trials)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
