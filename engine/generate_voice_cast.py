"""Create an original, non-imitative voice-cast record from semantic choices."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


CHOICES = {
    "register": ("low", "low_mid", "mid", "high_mid", "high"),
    "grain": ("clear", "dry", "smokeless_dark", "paper", "glass", "warm", "frayed"),
    "delivery": ("speech_song", "held_line", "clipped_phrase", "falling_phrase", "ascending_call"),
    "distance": ("close", "room", "far", "moving"),
    "role": ("lead_voice", "supporting_voice"),
}


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def choose(name: str, value: str) -> str:
    if value not in CHOICES[name]:
        raise ValueError(f"{name} must be one of: {', '.join(CHOICES[name])}")
    return value


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", required=True, help="invented cast name, never a performer name")
    for key in CHOICES:
        parser.add_argument(f"--{key.replace('_', '-')}", required=True, dest=key, choices=CHOICES[key])
    parser.add_argument("--tension", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    values = {key: choose(key, getattr(args, key)) for key in CHOICES}
    identifier = f"voice.{slug(args.name)}"
    title = args.name.strip()
    prompt = ", ".join(value.replace("_", " ") for value in (values["register"], values["grain"], values["delivery"], values["distance"]))
    text = f'''---
id: {identifier}
kind: voice
title: {title} â€” original generated cast
status: draft
evidence_class: inferred
source_ids: []
composition_role: {values["role"]}
register: {values["register"]}
density: open
energy: contained
material: voice
emotional_tension: {args.tension}
interaction: {"answer" if values["role"] == "supporting_voice" else "handoff"}
created_at: <set-on-acceptance>
updated_at: <set-on-acceptance>
---

# {title}

## Cast identity

An original {values["register"]} {values["grain"]} vocal role with {values["delivery"]} delivery, heard at {values["distance"]} distance. Its purpose is {args.tension}; it is not an imitation, clone, accent, language, or regional vocal claim.

## Prompt vocabulary

`{prompt}, original vocal identity, clear diction, controlled phrasing, no named-singer imitation`

## Arrangement behavior

Use this cast as a {values["role"].replace("_", " ")}. Give it one distinct job: carry a line, answer a phrase, interrupt a transition, or leave space. Do not use it as generic decorative harmonies.
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

