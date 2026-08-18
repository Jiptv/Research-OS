# License And Terms

This page explains the license choice for Research OS.

This is not legal advice. For company, client or employer-owned work, check
with the relevant owner before publishing.

## Why This Matters

If a public repository has no license, other people can read the code, but they
do not automatically get clear permission to use, copy, modify or redistribute
it.

GitHub recommends adding a license so visitors can clearly see how they may use
the project. GitHub also detects common `LICENSE` files and shows the license on
the repository page.

## Current License Choice

Research OS uses:

```text
PolyForm Noncommercial License 1.0.0
```

Commercial use requires separate prior written permission from the repository
owner.

In plain language:

- People may use, study, modify and share Research OS for noncommercial purposes.
- People may not sell it, sell access to it, offer it as a paid service, include
  it in a commercial product, or otherwise use it commercially without written
  permission.
- You can still give commercial permission separately if you want to.

See:

- `LICENSE.md`
- `COMMERCIAL_USE.md`

## Other Common Options Considered

### Option 1 - MIT License

Use this when you want Research OS to be easy for others to use, copy, modify
and adapt.

Typical effect:

- People can use it privately or commercially.
- People can modify and redistribute it.
- People must keep the copyright and license notice.
- There is no warranty.

This is the simplest common open source option.

### Option 2 - Apache License 2.0

Use this when you want a permissive license like MIT, but with more explicit
patent language and a requirement to state meaningful changes.

Typical effect:

- People can use it privately or commercially.
- People can modify and redistribute it.
- People must keep copyright and license notices.
- Contributors provide an explicit patent grant.
- There is no warranty.

This is common for larger or more formal open source projects.

### Option 3 - GPLv3 or AGPLv3

Use this when you want people who distribute modified versions to also share
their source code under the same license.

AGPLv3 is stricter for network/server use.

Typical effect:

- People can use, modify and distribute the project.
- Distributed modified versions must remain open under the same license.
- This can discourage companies that want to embed the project in closed-source
  products.

### Option 4 - Keep It Private Or Unlicensed

Use this when you are not ready for others to reuse it.

Typical effect:

- People can view the public repository if it is public.
- They do not have clear permission to use, modify or redistribute it.
- This is confusing for collaborators and not ideal for open source.

## Why Not GPL For This Goal?

GPL is useful when you want distributed modified versions to remain open source.
It does not prevent commercial use. People can still sell GPL software or use it
commercially, as long as they follow the GPL conditions.

Because the goal for Research OS is "commercial use only with permission",
PolyForm Noncommercial is a better fit.

## Terms Of Use

For a public GitHub repository that people run locally, a license is usually the
main thing you need.

Separate Terms of Use are usually more relevant when:

- you host Research OS as an online service for other people,
- people create accounts,
- you process or store their research data,
- you offer paid access,
- you need privacy, acceptable-use or support terms.

Research OS currently runs locally. The repository should still make clear:

- it is provided as-is,
- users are responsible for their own research data,
- private company branding and project data should not be committed,
- AI outputs should be reviewed by a human researcher.

## README License Text

The README should say:

```markdown
## License

Research OS is available for noncommercial use under the PolyForm
Noncommercial License 1.0.0. See `LICENSE.md`.

Commercial use requires separate prior written permission from the repository
owner. See `COMMERCIAL_USE.md`.

Research OS is provided as-is. Users are responsible for their own research
data, local backups, AI-provider configuration and review of AI-generated
outputs.
```

## How To Add A License On GitHub

1. Keep `LICENSE.md` at the repository root.
2. Keep `COMMERCIAL_USE.md` at the repository root.
3. Commit both files before making the repository public.

Common placeholders to fill:

```text
Copyright 2026 Jip Tervoort
```

or, if owned by an organization:

```text
Copyright 2026 <organization name>
```

## Do Not License These By Accident

These should stay outside the public repository:

- private research project data,
- interview transcripts,
- client or company strategy documents,
- real company logos unless cleared for public use,
- `.env` files and API keys,
- local learning logs or review histories that mention private work.
