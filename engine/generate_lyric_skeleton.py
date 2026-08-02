"""Create an original lyric-and-vocal skeleton from a library lyric behavior."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--theme", required=True)
    parser.add_argument("--behavior", required=True)
    parser.add_argument("--voice", required=True)
    parser.add_argument("--catalog", type=Path, default=root / "library" / "catalog.json")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    records = {record["id"]: record for record in json.loads(args.catalog.read_text(encoding="utf-8"))["records"]}
    lyric = records.get(args.behavior)
    voice = records.get(args.voice)
    if not lyric or lyric.get("kind") != "lyric":
        raise ValueError("--behavior must name a lyric record")
    if not voice or voice.get("kind") != "voice":
        raise ValueError("--voice must name a voice record")
    text = f"""# Lyric skeleton â€” {args.theme}

**Lyric behavior:** {lyric['id']} â€” {lyric['title']}
**Voice cast:** {voice['id']} â€” {voice['title']}

1. **Verse 1 â€” concrete image:** one physical scene; 2â€“4 short lines; no thesis statement.
2. **Pre-lift â€” pressure:** one unfinished question or altered image; leave a breath after it.
3. **Hook â€” release:** one repeatable vowel-friendly phrase, changed slightly on the second pass.
4. **Verse 2 â€” consequence:** show what shifted rather than explaining the emotion.
5. **Bridge â€” absence:** reduce language to one fragment or wordless contour; let arrangement speak.
6. **Final hook / exit:** return to the hook with one changed image, then stop on an authored final line.

**Writing direction:** {args.theme}. Use new language and melody. Keep consonants clear,
avoid filler syllables, chant loops, invented pseudo-language, and automatic ad-libs. Match
the cast's arrangement role; do not turn it into a generic choir or a named-singer imitation.
"""
    if args.output:
        if args.output.exists():
            raise FileExistsError(f"refusing to overwrite: {args.output}")
        args.output.write_text(text, encoding="utf-8")
        print(args.output)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
