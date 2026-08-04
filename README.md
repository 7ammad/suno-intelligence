# Suno Intelligence

> A creator proposal for taking music generation beyond a prompt box.

Suno already makes it possible to turn a thought into a song. This project asks
what happens when a creator can also build a durable musical memory: a living
library of rhythm, bass, instruments, voices, emotional worlds, arrangements,
original sound ideas, Suno craft knowledge, and the lessons earned from listening.

This is a public, creator-led proposal and working reference implementation. It
is not affiliated with Suno, and it does not reverse engineer or automate
Suno's consumer interface.

## Why this exists

After thousands of private experiments, the hard part is not generating another
track. The hard part is retaining the musical discoveries that made a track feel
alive, then using them to make the next one more surprising and more personal.

The ambition is a **music intelligence system** that helps a creator:

1. Start from an original impulse, a musical world, a genre/tradition question,
   a user-owned seed, or an abstracted reference study.
2. Combine musical roles—rhythm, bass, harmony, melody, form, texture, voice,
   and lyrics—into a specific composition brief rather than a bag of tags.
3. Create distinct original voice casts and sound-source roles instead of
   default generic vocals.
4. Generate manually in Suno today, using the right feature for creation,
   editing, voices, Sounds, hooks, cover art, stems, and release assets.
5. Keep, revise, or reject the candidate with a short reason that improves the
   next brief.
6. Turn the selected track into its visual world, hook/short, release plan,
   community conversation, and measured next idea.

The point is not automated content volume. It is a better creative memory.

## Creator references

Two public Suno experiments that informed this project:

- [Nothing Broke — candidate 1](https://suno.com/song/c7523f12-36c8-4218-8981-a66b7ebcfcfb)
- [Nothing Broke — candidate 2](https://suno.com/song/0de84576-3ea4-494a-8570-8f1afd05e846)

These are not held up as finished releases. They are evidence of the normal
creator loop: make, listen, name what is missing, and try again.

## The system

creative impulse -> music intelligence library -> composition + arrangement +
lyric/voice brief -> Suno generation or manual session -> listening decision:
keep / change / reject -> track record + visual world + hook -> publishing,
community, analytics -> bounded learning for the next brief

The musical library is the heart. It is an agent-usable semantic model with
records for musical worlds, rhythm, bass, harmony, melody, instruments, voice
casts, production texture, original sound sources, arrangement, and the
relationships between them. Cultural/tradition records carry source pointers
and explicit boundaries: they inform new composition choices; they are not
treated as a bag of stereotypes or repertoire to copy.

See [the product proposal](docs/PRODUCT_PROPOSAL.md), [the creator
workflow](docs/CREATOR_WORKFLOW.md), and the working [Creator Craft
Guide](engine/CREATOR_CRAFT_GUIDE.md).

## What we hope Suno enables

An official creator/developer surface could make this workflow much stronger:

- create and monitor generations from a creator-owned tool;
- attach a versioned composition brief and provenance to a generation;
- retrieve creator-authorized tracks, metadata, covers, stems where supported,
  and hook candidates;
- preserve generation lineage, remix/extend relationships, and creator notes;
- publish creator-approved track assets to an owned release workflow; and
- return reliable, permissioned performance data to improve future briefs.

The local system remains useful without this. The official API would remove
manual copying and let a creator's own history become usable creative context.

## Scope and principles

- **Creator-controlled:** the person chooses what to generate, keep, publish,
  and learn from.
- **Originality-oriented:** reference study extracts abstract musical attributes;
  it does not ask for artist imitation or copied recordings.
- **Human listening stays central:** a rating or metric is evidence, never the
  final artistic decision.
- **Manual-first today:** no browser automation, scraping, or unsupported API
  assumptions.
- **Public-safe:** this repository contains no keys, account tokens, private
  media, private prompts, or private track archives.

## Repository map

- docs/PRODUCT_PROPOSAL.md — the product thesis and capability model.
- docs/CREATOR_WORKFLOW.md — the end-to-end creator journey.
- docs/OPEN_QUESTIONS_FOR_SUNO.md — practical questions for the Suno team.
- engine/CREATOR_CRAFT_GUIDE.md — prompt language, lyrics, original voice
  casting, unwanted-vocal repair, feature choice, and the working music loop.
- engine/ — the runnable composition-world generator, semantic catalog,
  brief schema, and append-only trial recorders.

## Working local prototype

A first local creator console is now included at
[prototype/creator-console.html](prototype/creator-console.html). It turns a
creative seed into a composition brief, a manually attached Suno result, a
keep/change/reject decision, content-stage readiness, and portable track/Social
Family draft packages. It is intentionally local-first and carries no
credentials or live-publish action.

## A note to the Suno team

We are not asking for an autonomous music factory. We are asking for the
creative continuity serious music heads naturally build by hand: a way to
remember what we explored, why it worked, how a track evolved, and where to
take the next one.

If you are interested in talking, please open an issue in this repository.
