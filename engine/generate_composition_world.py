"""Generate a traceable original composition world from canonical library roles.

Example:
  python tools/generate_composition_world.py \
    --title "Glass Under the Tide" \
    --grammar grammar.drum-conducted-density-arc \
    --foundation bass.guembri-rhythmic-melody \
    --rhythm rhythm.frame-drum-jingle-shadow \
    --sound sound_source.bowed-glass-horizon \
    --harmony harmony.pedal-center-deferred-color \
    --melody melody.contour-handoff \
    --form form.reveal-withdraw-return \
    --voice voice.ember-alto-close-grain
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def record_index(catalog_path: Path) -> dict[str, dict[str, object]]:
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    return {str(record["id"]): record for record in catalog["records"]}


def resolve(index: dict[str, dict[str, object]], record_id: str, expected_kind: str) -> dict[str, object]:
    record = index.get(record_id)
    if not record:
        raise ValueError(f"unknown library record: {record_id}")
    if record.get("kind") != expected_kind:
        raise ValueError(f"{record_id} must be kind {expected_kind}, got {record.get('kind')}")
    return record


def hint(record: dict[str, object]) -> str:
    return str(record.get("prompt_hint") or record["title"])


def require_originality(value: str) -> str:
    cleaned = value.strip()
    if len(cleaned) < 24:
        raise ValueError("originality decision must describe a real transformation (at least 24 characters)")
    if re.search(r"\b(in the style of|sound like|imitate|copy)\b", cleaned, re.IGNORECASE):
        raise ValueError("originality decision cannot request imitation or copying")
    return cleaned


def clean_avoidance(value: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError("avoidance must not be empty")
    return cleaned


def build_world(args: argparse.Namespace, index: dict[str, dict[str, object]]) -> str:
    grammar = resolve(index, args.grammar, "grammar")
    foundation = resolve(index, args.foundation, "bass")
    rhythm = resolve(index, args.rhythm, "rhythm")
    sound = resolve(index, args.sound, "sound_source")
    harmony = resolve(index, args.harmony, "harmony")
    melody = resolve(index, args.melody, "melody")
    form = resolve(index, args.form, "form")
    instruments = [resolve(index, record_id, "instrument") for record_id in args.instrument]
    voice = resolve(index, args.voice, "voice") if args.voice else None
    supporting_voices = [resolve(index, record_id, "voice") for record_id in args.supporting_voice]
    lyric = resolve(index, args.lyric, "lyric") if args.lyric else None
    if lyric and not voice:
        raise ValueError("a lyric behavior requires a voice cast")
    ids = [args.grammar, args.foundation, args.rhythm, args.sound, args.harmony, args.melody, args.form] + args.instrument + ([args.voice] if args.voice else []) + args.supporting_voice + ([args.lyric] if args.lyric else [])
    if len(set(ids)) != len(ids):
        raise ValueError("each composition role must use a distinct library record")
    originality = require_originality(args.originality)
    avoidances = [clean_avoidance(value) for value in args.avoid]
    supporting_line = "; ".join(hint(record) for record in supporting_voices)
    instrument_line = "; ".join(hint(record) for record in instruments)
    voice_line = hint(voice) if voice else "instrumental; no lead vocal"
    if supporting_line:
        voice_line += ". Supporting cast roles: " + supporting_line
    source_ids = sorted({sid for record in (grammar, foundation, rhythm, sound, harmony, melody, form, voice, lyric, *instruments, *supporting_voices) if record for sid in record.get("source_ids", [])})
    return f"""# {args.title}

## Original composition world

**Listener promise:** {args.tension}

**Originality decision:** {originality}

## Chosen roles

- **Grammar:** {grammar['id']} â€” {grammar['title']}
- **Foundation:** {foundation['id']} â€” {foundation['title']}
- **Rhythm:** {rhythm['id']} â€” {rhythm['title']}
- **Sound source:** {sound['id']} â€” {sound['title']}
- **Harmony:** {harmony['id']} â€” {harmony['title']}
- **Melody:** {melody['id']} â€” {melody['title']}
- **Form:** {form['id']} â€” {form['title']}
- **Voice cast:** {voice['id'] if voice else 'none'} â€” {voice['title'] if voice else 'instrumental'}
- **Lyric behavior:** {lyric['id'] if lyric else 'none'} â€” {lyric['title'] if lyric else 'instrumental'}
- **Avoid:** {', '.join(avoidances) if avoidances else 'none specified'}

**Instrument roles:** {', '.join(record['id'] + ' â€” ' + record['title'] for record in instruments) if instruments else 'none'}

**Supporting casts:** {', '.join(record['id'] + ' â€” ' + record['title'] for record in supporting_voices) if supporting_voices else 'none'}

## Arrangement arc

1. Establish the foundation with space around the first rhythmic gestures.
2. Let the selected grammar trigger the first density shift; do not add every layer at once.
3. Introduce the sound source as a contrasting horizon or afterimage, not a constant pad.
4. {'Let the lead enter only after the foundation is legible; ' + ('assign each supporting cast one distinct answer, shadow, or late arrival.' if supporting_voices else 'keep its role narrow and distinct.') if voice else 'Keep the middle section non-vocal; let a melodic or textural response carry the lift.'}
5. Resolve by removing a role or changing the time field; do not use a generic fade.

## Provider-independent brief

Create an original composition. Emotional direction: {args.tension}. Foundation: {hint(foundation)}. Rhythm role: {hint(rhythm)}. Arrangement grammar: {hint(grammar)}. Harmony: {hint(harmony)}. Melody: {hint(melody)}. Form: {hint(form)}. Instrument role(s): {instrument_line if instruments else 'none; let the sound source carry the color'}. Distinctive sound source: {hint(sound)}. Voice behavior: {voice_line}. Lyric behavior: {hint(lyric) if lyric else 'no lyrics; preserve a true instrumental.'} {originality} Preserve silence between roles, a full arrangement arc, and an authored ending. {'Avoid: ' + '; '.join(avoidances) + '.' if avoidances else ''} Do not imitate a named artist or reproduce traditional repertoire.

## Provenance boundary

Referenced source IDs: {', '.join(source_ids) if source_ids else 'none; all selected roles are original/inferred'}.

The listed records are role inputs, not material to copy. This world requires a
new melody, new lyric if applicable, new structure, and a dated listening trial.
"""


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title", required=True)
    parser.add_argument("--tension", required=True)
    parser.add_argument("--originality", required=True)
    parser.add_argument("--grammar", required=True)
    parser.add_argument("--foundation", required=True)
    parser.add_argument("--rhythm", required=True)
    parser.add_argument("--sound", required=True)
    parser.add_argument("--harmony", required=True)
    parser.add_argument("--melody", required=True)
    parser.add_argument("--form", required=True)
    parser.add_argument("--instrument", action="append", default=[], help="instrument role from the library; may be repeated")
    parser.add_argument("--voice")
    parser.add_argument("--supporting-voice", action="append", default=[], help="supporting original voice cast; may be repeated")
    parser.add_argument("--lyric")
    parser.add_argument("--avoid", action="append", default=[], help="generation artifact or behavior to avoid; may be repeated")
    parser.add_argument("--catalog", type=Path, default=root / "library" / "catalog.json")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    world = build_world(args, record_index(args.catalog))
    if args.output:
        if args.output.exists():
            raise FileExistsError(f"refusing to overwrite: {args.output}")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(world, encoding="utf-8")
        print(args.output)
    else:
        print(world)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
