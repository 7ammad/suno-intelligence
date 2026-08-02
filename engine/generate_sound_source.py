"""Create an original semantic sound-source record for Suno Sounds or composition briefs."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


CHOICES = {
    "material": ("air", "glass", "metal", "stone", "water", "wire", "wood", "hybrid"),
    "gesture": ("tick", "scrape", "bow", "fold", "pulse", "rattle", "bloom", "wash"),
    "decay": ("instant", "short", "uneven", "long", "breathing"),
    "role": ("texture", "transition", "timekeeper"),
    "register": ("sub", "low", "mid", "high_mid", "high"),
}


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", required=True, help="invented sound-source name")
    for key, choices in CHOICES.items():
        parser.add_argument(f"--{key}", required=True, choices=choices)
    parser.add_argument("--tension", required=True, choices=("grounded", "longing", "friction", "awe", "tenderness", "defiance", "suspense", "release", "euphoria", "unease"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    identifier = f"sound_source.{slug(args.name)}"
    prompt = f"{args.material} {args.gesture}, {args.decay} decay, {args.register} register, sparse original sound detail"
    text = f'''---
id: {identifier}
kind: sound_source
title: {args.name.strip()} â€” original generated sound source
status: draft
evidence_class: inferred
source_ids: []
composition_role: {args.role}
time_behavior: sparse
pitch_behavior: noise_pitch_blend
register: {args.register}
density: spare
energy: contained
material: {args.material}
emotional_tension: {args.tension}
interaction: answer
created_at: <set-on-acceptance>
updated_at: <set-on-acceptance>
---

# {args.name.strip()}

## Sound identity

An original {args.material} {args.gesture} with {args.decay} decay in the {args.register} register. It creates {args.tension} through placement and silence, not a named instrument, sample pack, or cultural imitation.

## Suno Sounds vocabulary

`{prompt}, no full musical arrangement, no generic synth pad`

## Arrangement behavior

Use it as a {args.role}; let it arrive at structural edges or answer an empty phrase. Do not turn it into a constant loop unless the brief deliberately makes it the timekeeper.
'''
    if args.output:
        if args.output.exists():
            raise FileExistsError(f"refusing to overwrite: {args.output}")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
        print(args.output)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

