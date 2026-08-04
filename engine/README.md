# Working composition engine

This is the public-safe reference implementation behind the proposal.

It turns an explicit composition world into a renderer-ready brief without artist imitation:

- relationship-grounded rhythm, bass, and temporal-grammar selection;
- harmony, melody, form, sound-source, and instrument roles;
- original lead and supporting voice casts—not named-singer imitation;
- lyric behavior plus explicit controls for filler syllables, random `wop-wop`, unwanted ad-libs, and unintelligible vocals;
- an originality boundary, provenance IDs, and append-only human listening evidence.

Read the [Creator Craft Guide](CREATOR_CRAFT_GUIDE.md) for the full creator path: musical premise -> role-based composition world -> brief -> Suno feature choice -> manual generation -> repair -> reusable learning. It includes prompt language, lyrics, original voice casting, and artifact repair.

`library/semantic-model.json` is the canonical agent contract. It gives every future agent the same music-role vocabulary, combination checks, voice-casting rules, lyric/artifact protocol, and Suno prompt-evidence fields. It is a framework for musical intelligence—not a database of copied melodies, audio, or artist styles.

## Run it

```bash
python engine/propose_composition_worlds.py \
  --catalog engine/library/catalog-v1.5.json \
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

The machine-readable [composition-brief v1.1 schema](library/composition-brief-v1.2.schema.json) retains the selected role map, original voice cast, lyric behavior, arrangement arc, avoid conditions, and artifact-diagnosis fields alongside the final prompt.

The [official Suno capability map](library/suno-capabilities.json) covers creation, original Voices, Custom Models, Suno Sounds, editing, Add Vocals, Hooks, upload/album-art, and stem separation—with the exact run evidence each capability must retain.

Query semantic records directly—for example: `python engine/query_library.py --kind voice --facet register=low --facet energy=contained`.

Run `python engine/validate_library.py` to validate record IDs, archive provenance pointers, semantic facets, and relationship endpoints before publishing a catalog.

Manual Suno runs become reusable evidence through the [trial-record schema](library/suno-trial-record.schema.json) and [trial protocol](library/SUNO_TRIAL_PROTOCOL.md), including lyric, generic-voice, and unwanted-vocal-artifact diagnosis.

Use `python engine/record_suno_trial.py` to append a reviewed Suno result—prompt, model, output reference, artifact time ranges, listening verdict, and the exact next repair delta—without automating or mutating Suno.

Use `python engine/generate_voice_cast.py` to create new semantic original voice roles from register, grain, delivery, distance, and arrangement role—never a named singer.

Use `python engine/generate_sound_source.py` to create an original semantic sound-source role for Suno Sounds or arrangement, from material, gesture, decay, register, and role.

Pass `--brief-dir <folder>` to `propose_composition_worlds.py` to emit a validated canonical brief JSON beside every proposed world.


The [Suno Window Workflows](SUNO_WINDOW_WORKFLOWS.md) map every supported manual workflow to its actual current Suno fields and actions, so future Chrome automation follows the same contract rather than inventing a universal prompt form.
