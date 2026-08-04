# Suno window workflows

This is the manual-to-Chrome operating contract. A task selects one Suno window; the system returns only that window's fields and preserves a receipt for later automation.

## Custom Create — vocal song

```text
WINDOW: Create > Custom
MODEL: [current model | selected Voice | selected Custom Model]
LYRICS: [final section-labelled lyric]
STYLE OF MUSIC: [arrangement / sound / vocal direction]
ADVANCED: Weirdness [..] | Style Influence [..] | Audio Influence [.. if shown]
TITLE: [working title]
CREATE
```

## Custom Create — instrumental

```text
WINDOW: Create > Custom
MODEL: [current model]
INSTRUMENTAL: ON
STYLE OF MUSIC: [foundation + material + arrangement arc + explicit exclusions]
ADVANCED: Weirdness [..] | Style Influence [..]
TITLE: [working title]
CREATE
```

## ReMi lyric draft

```text
WINDOW: Create > Custom > Lyrics > Write with Suno
LYRIC BRIEF: [speaker + emotional turn + images + section jobs + language]
LYRIC MODEL: ReMi | Classic
WRITE LYRICS
```

Edit the returned words before they become a production lyric.

## Upload Audio

```text
WINDOW: Create > Upload Audio
SOURCE: Record | My Device
FILE / RECORDING: [owned source]
TITLE: [source title]
ALBUM ART: generated prompt | uploaded image (optional)
OWNERSHIP CONFIRMATION: ON
CONTINUE
NEXT ACTION: Extend | Cover | Add Vocals | Studio/stems
```

## Extend

```text
WINDOW: song (...) > Remix/Edit > Extend
SOURCE SONG: [selected song]
EXTEND FROM: [timeline point]
LYRICS: [continuation, if vocal]
STYLE DETAILS: [what changes or preserves]
CREATE
IF KEPT: (...) > Create > Get Whole Song
```

## Song Editor

```text
WINDOW: Song Editor
TARGET: selected clip or highlighted range
ACTION: Replace | Edit Lyrics | Create Section | Quick Replace
REPLACE PROMPT: [one specific musical change]
REPLACE LYRICS: [new text]
SECTION BEATS + LYRICS: [length + text]
PREVIEW ALTERNATIVES > COMMIT selected take
```

## Add Vocals

```text
WINDOW: Library / Workspaces > song (...) > Remix > Add Vocals
LYRICS: [final section-labelled lyric]
STYLE: [existing instrumental + desired vocal role]
ADVANCED: Audio Strength [..]
CREATE
```

## Voices

```text
WINDOW: Create > Add Voice > Create Voice
SOURCE: song in Library | Record now | Upload audio
CLIP: choose up to 2 minutes from a 15 sec–4 min source
VERIFY: read Suno's displayed phrase
PROFILE: voice name | skill level | optional image
RIGHTS CONFIRMATION: ON > SAVE
CREATE WINDOW: select voice + model, Lyrics, Style, Title, high Audio Influence
```

## Custom Models

```text
WINDOW: Create > model dropdown > Create Custom Model
CORPUS: 6+ owned tracks
MODEL INTENT: [what continuity should be retained]
CREATE CUSTOM MODEL > wait until ready > select it in model picker
```

## Sounds

```text
WINDOW: Create > Custom > dropdown > Sounds
PROMPT: [material + gesture + decay + purpose]
TYPE: One Shot | Loop
BPM: [optional]
KEY: [optional]
CREATE
```

## Hooks

```text
WINDOW: Hooks feed > Create a Hook
SONG: Recents | Public | Liked
START POINT: scrub to chosen moment
VIDEO: upload from device library
SHOW LYRICS: on | off
POST
```

## Stem separation

```text
WINDOW: song > stems / separation
MODE: Auto Split | Split from Mix | Advanced Split
TARGET: [single instrument/vocal for Split from Mix]
STEMS: [selected instruments for Advanced Split]
RUN
```

Every run ends with a receipt: exact fields entered, source, output URL/reference, keep/change/reject decision, what worked, and one next change.

Sources: [Custom mode](https://help.suno.com/en/articles/3726721), [Song Editor](https://help.suno.com/en/articles/6141505), [Add Vocals](https://help.suno.com/en/articles/6882817), [Voices](https://help.suno.com/en/articles/11362369), [Custom Models](https://help.suno.com/en/articles/11362497), [Sounds](https://help.suno.com/en/articles/10625537), [Hooks](https://help.suno.com/en/articles/8049409), [Upload Audio](https://help.suno.com/en/articles/6141569), [Advanced Stem Separation](https://help.suno.com/en/articles/12702337).
