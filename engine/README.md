# Working composition engine

This is the public-safe reference implementation behind the proposal.

It turns an explicit composition world into a renderer-ready brief without artist imitation:
- relationship-grounded rhythm/bass/grammar selection;
- harmony, melody, form, source and instrument roles;
- a lead voice plus supporting vocal casts;
- lyric behavior and explicit artifact avoidances;
- an originality boundary and provenance IDs;
- append-only human listening evidence that can rank later proposals.

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
