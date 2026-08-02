# Creator Console Prototype

Open `creator-console.html` in any modern browser.

It is intentionally local-first:
- your drafts live in browser local storage;
- **Download track package** creates portable Markdown and JSON;
- **Download Social Family drafts** creates draft-only handoffs for kept tracks;
- it contains no Suno credentials, social tokens, UI automation, or live publishing.

The production local workflow also has a small import command that turns an exported record into a canonical `songs/<slug>/` Suno Lab record.