"""Propose coherent, original composition worlds from the Suno Intelligence library.

This is deliberately a proposer, not an imitation engine. It composes only from
role records and explicit relationship evidence; the returned worlds still need
new melody, text, pitch material, and a listening decision.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

from generate_composition_world import build_brief_payload, build_world, default_catalog_path


ROLE_KINDS = ("grammar", "bass", "rhythm", "sound_source", "harmony", "melody", "form")
DISPLAY_ROLES = (
    ("grammar", "grammar"),
    ("foundation", "bass"),
    ("rhythm", "rhythm"),
    ("sound", "sound source"),
    ("harmony", "harmony"),
    ("melody", "melody"),
    ("form", "form"),
    ("voice", "voice"),
    ("lyric", "lyric behavior"),
)


def index_records(catalog_path: Path) -> tuple[dict[str, dict[str, object]], dict[str, list[dict[str, object]]]]:
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    records = {str(record["id"]): record for record in catalog["records"]}
    by_kind: dict[str, list[dict[str, object]]] = defaultdict(list)
    for record in records.values():
        by_kind[str(record["kind"])].append(record)
    return records, by_kind


def taste_scores(trials_path: Path | None) -> dict[str, int]:
    scores: dict[str, int] = defaultdict(int)
    if not trials_path or not trials_path.is_file():
        return scores
    for line in trials_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        trial = json.loads(line)
        delta = {"keep": 1, "reject": -1}.get(trial.get("outcome"), 0)
        for record_id in trial.get("record_ids", []):
            scores[str(record_id)] += delta
    return scores


def candidates(records: dict[str, dict[str, object]], by_kind: dict[str, list[dict[str, object]]], scores: dict[str, int]) -> list[dict[str, object]]:
    relations = [record for record in records.values() if record["kind"] == "relationship"]
    worlds: list[dict[str, object]] = []
    for relation in relations:
        endpoints = set(relation.get("from_ids", [])) | set(relation.get("to_ids", []))
        ordinal = len(worlds)
        choice = lambda kind: by_kind[kind][ordinal % len(by_kind[kind])]
        endpoint = lambda kind: next((records[item] for item in sorted(endpoints) if records.get(item, {}).get("kind") == kind), None)
        voice_endpoints = [records[item] for item in sorted(endpoints) if records.get(item, {}).get("kind") == "voice"]
        lead_pool = [record for record in by_kind["voice"] if record.get("composition_role") != "supporting_voice"]
        lead_voice = next((record for record in voice_endpoints if record.get("composition_role") != "supporting_voice" and "chorus" not in str(record["title"]).lower() and "group" not in str(record["title"]).lower()), None)
        lead_voice = lead_voice or (voice_endpoints[0] if voice_endpoints else lead_pool[ordinal % len(lead_pool)])
        supporting = [record for record in voice_endpoints if record["id"] != lead_voice["id"]]
        if not supporting:
            support_pool = [
                record for record in by_kind["voice"]
                if record.get("composition_role") == "supporting_voice"
                and record.get("register") != lead_voice.get("register")
            ]
            if support_pool:
                supporting = [support_pool[ordinal % len(support_pool)]]
        world = {
            "relationship": relation,
            "grammar": endpoint("grammar") or choice("grammar"),
            "foundation": endpoint("bass") or choice("bass"),
            "rhythm": endpoint("rhythm") or choice("rhythm"),
            "sound": choice("sound_source"),
            "instruments": [
                by_kind["instrument"][ordinal % len(by_kind["instrument"])],
                by_kind["instrument"][(ordinal + 1) % len(by_kind["instrument"])],
            ],
            "harmony": choice("harmony"),
            "melody": choice("melody"),
            "form": choice("form"),
            "voice": lead_voice,
            "supporting_voices": supporting,
            "lyric": by_kind["lyric"][ordinal % len(by_kind["lyric"])],
        }
        selected = [world["grammar"], world["foundation"], world["rhythm"], world["sound"], world["harmony"], world["melody"], world["form"], *world["instruments"], world["voice"], *world["supporting_voices"], world["lyric"]]
        world["taste_score"] = sum(scores.get(str(record["id"]), 0) for record in selected)
        worlds.append(world)
    return sorted(worlds, key=lambda world: int(world["taste_score"]), reverse=True)


def diverse_selection(worlds: list[dict[str, object]], count: int) -> list[dict[str, object]]:
    """Pick a compact batch that explores different musical materials."""
    remaining = list(worlds)
    selected: list[dict[str, object]] = []
    used_ids: set[str] = set()
    while remaining and len(selected) < count:
        def value(world: dict[str, object]) -> tuple[int, int]:
            record_ids = {
                str(world["grammar"]["id"]), str(world["foundation"]["id"]),
                str(world["rhythm"]["id"]), str(world["sound"]["id"]),
                str(world["harmony"]["id"]), str(world["melody"]["id"]),
                str(world["form"]["id"]), str(world["voice"]["id"]),
                *(str(record["id"]) for record in world["instruments"]),
            }
            overlap = len(record_ids & used_ids)
            return int(world["taste_score"]) - overlap, -overlap
        chosen = max(remaining, key=value)
        selected.append(chosen)
        used_ids.update({
            str(chosen["grammar"]["id"]), str(chosen["foundation"]["id"]),
            str(chosen["rhythm"]["id"]), str(chosen["sound"]["id"]),
            str(chosen["harmony"]["id"]), str(chosen["melody"]["id"]),
            str(chosen["form"]["id"]), str(chosen["voice"]["id"]),
            *(str(record["id"]) for record in chosen["instruments"]),
        })
        remaining.remove(chosen)
    return selected


def make_brief_args(number: int, world: dict[str, object], args: argparse.Namespace) -> argparse.Namespace:
    return argparse.Namespace(
        title=f"{args.title_prefix} {number}",
        tension=args.tension,
        originality=args.originality,
        grammar=world["grammar"]["id"],
        foundation=world["foundation"]["id"],
        rhythm=world["rhythm"]["id"],
        sound=world["sound"]["id"],
        instrument=[record["id"] for record in world["instruments"]],
        harmony=world["harmony"]["id"],
        melody=world["melody"]["id"],
        form=world["form"]["id"],
        voice=world["voice"]["id"],
        supporting_voice=[record["id"] for record in world["supporting_voices"]],
        lyric=world["lyric"]["id"],
        avoid=args.avoid or ["generic choir pad", "wop-wop syllable loops"],
    )


def format_world(number: int, world: dict[str, object], args: argparse.Namespace, records: dict[str, dict[str, object]]) -> tuple[str, dict[str, object]]:
    r = world["relationship"]
    brief_args = make_brief_args(number, world, args)
    rendered = build_world(brief_args, records)
    prompt = rendered.split("## Provider-independent brief\n\n", 1)[1].split("\n\n## Provenance boundary", 1)[0]
    markdown = "\n".join([
        f"## {number}. {r['title']}",
        f"**Why this holds together:** {r.get('relation_type', 'explicit relationship')} between {', '.join(r.get('from_ids', []))} and {', '.join(r.get('to_ids', []))}.",
        "",
        "| Role | Proposed record |",
        "| --- | --- |",
        *[f"| {label} | `{world[key]['id']}` â€” {world[key]['title']} |" for key, label in DISPLAY_ROLES],
        "| instrument roles | " + "; ".join(f"`{record['id']}` â€” {record['title']}" for record in world["instruments"]) + " |",
        *(["| supporting casts | " + "; ".join(f"`{record['id']}` â€” {record['title']}" for record in world["supporting_voices"]) + " |"] if world["supporting_voices"] else []),
        "",
        "**Originality rule:** treat every selected item as a role constraint; write new pitch material, words, vocal phrasing, and form details. Do not claim a living tradition, imitate a named artist, or reproduce repertoire.",
        f"**Listening-evidence score:** {world['taste_score']} (bounded keep/reject evidence; not automatic taste training).",
        "",
        "**Suno-ready brief:** " + prompt,
    ])
    return markdown, build_brief_payload(brief_args, records, rendered)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=default_catalog_path(root))
    parser.add_argument("--count", type=int, default=3)
    parser.add_argument("--title-prefix", default="Untitled world")
    parser.add_argument("--tension", default="An original journey that moves from intimate motion toward a clear, earned horizon")
    parser.add_argument("--originality", default="Write a new melody, lyric behavior, pitch material, and section arc from these role constraints.")
    parser.add_argument("--avoid", action="append", default=[])
    parser.add_argument("--trials", type=Path, help="optional append-only listening-trial JSONL")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--brief-dir", type=Path, help="write one canonical v1.2 brief JSON per proposal")
    args = parser.parse_args()
    records, by_kind = index_records(args.catalog)
    missing = [kind for kind in (*ROLE_KINDS, "voice", "lyric") if not by_kind[kind]]
    if missing:
        raise ValueError(f"cannot propose worlds; library has no records for: {', '.join(missing)}")
    proposed = diverse_selection(candidates(records, by_kind, taste_scores(args.trials)), args.count)
    if not proposed:
        raise ValueError("cannot propose worlds; add an explicit relationship record")
    rendered = [format_world(number, world, args, records) for number, world in enumerate(proposed, 1)]
    result = "# Proposed composition worlds\n\n" + "\n\n".join(markdown for markdown, _ in rendered) + "\n"
    if args.output:
        if args.output.exists():
            raise FileExistsError(f"refusing to overwrite: {args.output}")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result, encoding="utf-8")
        print(args.output)
    else:
        print(result)
    if args.brief_dir:
        args.brief_dir.mkdir(parents=True, exist_ok=True)
        for _, brief in rendered:
            target = args.brief_dir / f"{brief['brief_id']}.json"
            if target.exists():
                raise FileExistsError(f"refusing to overwrite: {target}")
            target.write_text(json.dumps(brief, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(args.brief_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

