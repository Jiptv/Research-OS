# AI Assistant Guide For Research OS

You are working inside a Research OS workspace.

These instructions are for any AI coding assistant, including Codex, Claude,
Claude Code or another tool that can read and change files in a local project
folder.

The workspace root should look like this:

```text
UX Research/
├── Research OS/
└── Projects/
```

Always treat `UX Research/` as the project/workspace root, not only
`UX Research/Research OS/`. Research OS needs both:

- `Research OS/` for the system, scripts, documentation and agent instructions.
- `Projects/` for the user's research projects, rounds, source files and outputs.

## First Things To Read

Before changing files or processing research input, read:

1. `Research OS/AGENTS.md`
2. `Research OS/README.md`
3. `Research OS/FILE_STRUCTURE.md`
4. `Research OS/docs/05 Knowledge Pipeline.md`
5. The relevant agent instructions in `Research OS/agents/`

If the user's request is about setup, installation, Docker or sharing, also read:

- `Research OS/START_HERE.md`
- `Research OS/docs/11 Setup.md`

## Core Rules

- Research OS is a knowledge system, not just a document folder.
- Keep source material, evidence, patterns, insights, recommendations and deliverables separate.
- Evidence must stay traceable to source material.
- The AI can draft, structure, critique and update files, but the researcher decides what becomes accepted knowledge.
- Do not overwrite or delete source files unless the user explicitly asks.
- Do not expose local secrets, private project data or local company branding.
- Keep generated work in the expected project or round folders.

## Common Commands

Run commands from:

```sh
cd "$HOME/UX Research/Research OS"
```

Start the dashboard:

```sh
scripts/run-dashboard-docker.sh
```

Stop the dashboard:

```sh
docker compose down
```

Create a project:

```sh
./research-os project create --name "New Product Area"
```

Create a round:

```sh
./research-os round create --project new-product-area --date 2026-07-29 --name "Concept Test 01"
```

## Where Files Belong

Project files belong under:

```text
Projects/<project-id>/
```

Round files belong under:

```text
Projects/<project-id>/02-rounds/<round-id>/
```

Source material belongs in the relevant input/source folder, not in the system
folder.

System documentation, scripts and templates belong under:

```text
Research OS/
```

## How To Help The User

For normal research work:

1. Identify the relevant project and round.
2. Read existing project context and round state.
3. Check whether there are new source files or pending review decisions.
4. Advance only the next safe stage in the knowledge pipeline.
5. Stop after creating reviewable outputs when researcher review is required.
6. Explain what changed and where.

For setup work:

1. Read `Research OS/START_HERE.md`.
2. Check Docker and folder location assumptions.
3. Keep the active workspace outside Documents, Desktop and iCloud Drive.
4. Use `~/UX Research` as the default location.

## Useful First Prompt

If the user is unsure what to ask, suggest this exact prompt:

```text
Read CLAUDE.md, AGENTS.md and the Research OS instructions. Then inspect the
Projects folder and tell me what projects and rounds exist, what needs review,
and what the next safe Research OS action is. Do not change files yet.
```
