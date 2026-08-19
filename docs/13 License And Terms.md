# License And Terms

Research OS uses the PolyForm Noncommercial License 1.0.0.

Commercial use requires separate prior written permission from the repository
owner.

See:

- `LICENSE.md`
- `COMMERCIAL_USE.md`

## What This Means

- Research OS may be used, studied, modified and shared for noncommercial use.
- Research OS may not be sold, offered as a paid service, included in a
  commercial product or otherwise used commercially without written permission.
- Research OS is provided as-is. Users are responsible for their own research
  data, local backups, AI-provider configuration and review of AI-generated
  outputs.

## Keep Local Data Out Of Git

These should stay outside the Research OS repository:

- research project data in `../Projects`,
- interview transcripts,
- client or company strategy documents,
- real company logos or licensed brand assets,
- `.env` files and API keys,
- local learning logs or review histories that mention private work.

Use `.gitignore`, `branding/.gitignore` and the local `Projects` folder to keep
workspace data separate from the Research OS system files.
