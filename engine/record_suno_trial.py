"""Append one human-reviewed Suno trial using the library trial-record contract."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path


OUTCOMES = {"keep": "kept", "not-yet": "not_yet", "reject": "rejected", "repair": "repair_selected"}


def artifact(value: str) -> dict[str, str]:
    try:
        label, time_range, correction = value.split("|", 2)
    except ValueError as exc:
        raise ValueError("artifact must be label|time-range|next-correction") from exc
    return {"label": label.strip(), "time_range": time_range.strip(), "correction": correction.strip()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trial-id", required=True)
    parser.add_argument("--brief-id", required=True)
    parser.add_argument("--capability", default="suno.custom_create")
    parser.add_argument("--model", required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--lyrics-mode", choices=("instrumental", "custom_lyrics", "remi", "none"), default="none")
    parser.add_argument("--output-reference", action="append", required=True)
    parser.add_argument("--outcome", choices=OUTCOMES, required=True)
    parser.add_argument("--decision", required=True)
    parser.add_argument("--reason", action="append", default=[])
    parser.add_argument("--artifact", action="append", default=[], help="label|time-range|next-correction; repeatable")
    parser.add_argument("--next-change", required=True)
    parser.add_argument("--trials", type=Path, required=True)
    args = parser.parse_args()
    record = {
        "trial_id": args.trial_id,
        "created_at": datetime.now(UTC).isoformat(),
        "brief_id": args.brief_id,
        "capability_id": args.capability,
        "model_or_mode": args.model,
        "prompt": args.prompt,
        "lyrics_mode": args.lyrics_mode,
        "output_references": args.output_reference,
        "outcome": OUTCOMES[args.outcome],
        "listening_decision": args.decision,
        "reason_tags": [value for value in args.reason if value],
        "artifact_observations": [artifact(value) for value in args.artifact],
        "next_change": args.next_change,
    }
    args.trials.parent.mkdir(parents=True, exist_ok=True)
    with args.trials.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(json.dumps({"trial_id": args.trial_id, "outcome": record["outcome"], "trials": str(args.trials)}))


if __name__ == "__main__":
    raise SystemExit(main())

