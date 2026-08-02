# Working composition engine

This is the public-safe reference implementation behind the proposal.

It turns an explicit composition world into a renderer-ready brief without artist imitation:

- relationship-grounded rhythm, bass, and temporal-grammar selection;
- harmony, melody, form, sound-source, and instrument roles;
- original lead and supporting voice casts—not named-singer imitation;
- lyric behavior plus explicit controls for filler syllables, random `wop-wop`, unwanted ad-libs, and unintelligible vocals;
- an originality boundary, provenance IDs, and append-only human listening evidence.

`library/semantic-model.json` is the canonical agent contract. It gives every future agent the same music-role vocabulary, combination checks, voice-casting rules, lyric/artifact protocol, and Suno prompt-evidence fields. It is a framework for musical intelligence—not a database of copied melodies, audio, or artist styles.

## Run it

```bash
python engine/propose_composition_worlds.py \
  --catalog engine/library/catalog.json \
  --count 5 \
  --output proposed-worlds.md
```

To record a real listening decision:

```bash
python engine/record_listening_trial.py \
  --world proposed-worlds.md \
  --outcome keep \
  --reason "voice-cast-kept" \
  --trials listening-trials.jsonl
```

Then add `--trials listening-trials.jsonl` to the proposer.

The checked-in catalog contains role-level metadata and source pointers only: no private media, account data, raw prompts, credentials, or downloaded cultural archives.
