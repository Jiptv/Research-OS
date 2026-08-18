# Research OS File Structure

Research OS keeps the visible folder structure deliberately small. As a
researcher, you should usually only touch input folders, review work in the
dashboard, and share approved output.

## Workspace

```text
UX Research/
├── Research OS/
└── Projects/
```

`Research OS/` contains the app, dashboard, agents and documentation.

`Projects/` contains local research work. It is not meant to be committed to the
shared Research OS repository.

The Docker launcher creates `Projects/` next to `Research OS/` if it does not
exist yet.

## Project Folder

```text
Projects/<project-id>/
├── 00-ai-work-files/
├── 01-input-source-files/
└── 02-rounds/
```

### `00-ai-work-files/`

AI and system work files for the project.

This includes:

- project context and current understanding
- project source representations
- review proposals
- project pipeline run logs

Researchers normally do not edit this folder directly. It exists for
traceability, debugging and reusable context.

### `01-input-source-files/`

Project-level input that should inform the project across multiple rounds.

Use this for:

- stakeholder interviews
- strategy decks
- product documentation
- research archives
- meeting recordings
- durable project background

Do not put round-specific interview transcripts here. Put those in the round's
input folder.

### `02-rounds/`

Research rounds inside the project.

Each round is a bounded study, test, interview batch, evaluation or synthesis
cycle.

## Round Folder

```text
Projects/<project-id>/02-rounds/<date>-<round-name>/
├── 00-ai-work-files/
├── 01-input-source-files/
└── 02-output-deliverables/
```

### `00-ai-work-files/`

AI and system work files for this round.

This includes:

- round overview and research questions
- pipeline settings
- source representations
- evidence observations
- patterns
- insights
- recommendations
- review queue
- method assessments
- pipeline run logs

Researchers normally review this work through the dashboard instead of editing
the files manually.

### `01-input-source-files/`

Original round-specific source material.

Use this for:

- interview transcripts
- research notes
- recordings
- screenshots
- usability test observations
- survey exports
- round setup notes

Keep original source files intact after processing so traceability remains
clean.

### `02-output-deliverables/`

Reviewable and final output for this round.

This includes:

- reviewable Markdown sources
- exported PDFs
- copyable deck prompts
- ready-to-post Slack messages
- Figma/FigJam post-it notes

Deliverables follow a two-step lifecycle:

1. Codex/Cowork drafts or updates a reviewable Markdown source.
2. The researcher reviews it in the dashboard.
3. Codex/Cowork exports or finalizes the approved artefact.

Do not treat generated deliverables as source knowledge. The source of truth is
the accepted knowledge in `00-ai-work-files/`.

## Where Do I Put Things?

Project-wide material:

```text
Projects/<project-id>/01-input-source-files/
```

Round-specific material:

```text
Projects/<project-id>/02-rounds/<round-id>/01-input-source-files/
```

Shareable output:

```text
Projects/<project-id>/02-rounds/<round-id>/02-output-deliverables/
```

AI trace/debug files:

```text
00-ai-work-files/
```

## What Goes To Git?

Commit Research OS itself:

```text
Research OS/
```

Do not commit local project data:

```text
Projects/
```

Also keep local state out of git:

- `.env`
- `.dashboard-settings.json`
- `.backup-status.json`
- `08-looped-learning/feedback-signals.jsonl`
- `08-looped-learning/learning-loop-state.json`
- `08-looped-learning/review-decisions.json`
- `local-branding/`

## Structure Rule

If a folder is mostly for the researcher, it should be one of:

- `01-input-source-files`
- `02-output-deliverables`
- `02-rounds`

If a folder is mostly for AI, pipeline state, review internals, traceability or
debugging, put it under:

```text
00-ai-work-files/
```
