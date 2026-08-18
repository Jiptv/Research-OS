# License And Terms

This page explains the practical choices before making Research OS public.

This is not legal advice. For company, client or employer-owned work, check
with the relevant owner before publishing.

## Why This Matters

If a public repository has no license, other people can read the code, but they
do not automatically get clear permission to use, copy, modify or redistribute
it.

GitHub recommends adding a license so visitors can clearly see how they may use
the project. GitHub also detects common `LICENSE` files and shows the license on
the repository page.

## Usual Options

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

## Recommended Choice For Research OS

If the goal is to let colleagues and other researchers easily try, adapt and
build on Research OS, use:

```text
MIT License
```

If you want a slightly more formal permissive license with explicit patent
language, use:

```text
Apache License 2.0
```

For this project, MIT is probably the easiest default unless there is a specific
reason to require Apache-2.0 or copyleft.

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

## Suggested README Text

After choosing a license, add a short README section like:

```markdown
## License

Research OS is released under the MIT License. See `LICENSE`.

Research OS is provided as-is. Users are responsible for their own research
data, local backups, AI-provider configuration and review of AI-generated
outputs.
```

For Apache-2.0, replace `MIT License` with `Apache License 2.0`.

## How To Add A License On GitHub

1. Add a file named `LICENSE` or `LICENSE.md` at the repository root.
2. Use GitHub's license template chooser, or copy the official license text from
   a trusted source.
3. Commit the license before making the repository public.

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
