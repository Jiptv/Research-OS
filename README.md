# Research OS

Research OS is an operating system for research, not a repository for reports.

**Focused on users, automated with AI.**

Research OS was created and is developed with substantial AI assistance. AI helps
shape the code, documentation and research workflows, but it can make mistakes.
Use Research OS as a researcher-controlled system: review AI-generated research
knowledge, check source traceability, and verify code or setup changes before
trusting them in important work.

For a non-technical local installation guide, start with:

```text
START_HERE.md
```

To install directly from GitHub on a Mac:

First check whether Git is installed:

```sh
git --version
```

If a Mac popup asks you to install Apple command line tools, click install and
wait until it finishes. Then run `git --version` again.

If that does not work, install Git from:

```text
https://git-scm.com/download/mac
```

Then install Research OS:

```sh
mkdir -p "$HOME/UX Research"
git clone https://github.com/Jiptv/Research-OS.git "$HOME/UX Research/Research OS"
mkdir -p "$HOME/UX Research/Projects"
cd "$HOME/UX Research/Research OS"
scripts/run-dashboard-docker.sh
```

To update later:

```sh
cd "$HOME/UX Research/Research OS"
git pull
scripts/run-dashboard-docker.sh
```

Docker Compose examples are in `docs/11 Setup.md`.

Change notes are in `CHANGELOG.md`.

For AI assistants opening the whole `UX Research` workspace, keep `AGENTS.md`
at the workspace root. That file tells Claude, Codex or another coding agent to
read the Research OS instructions and work with both `Research OS/` and
`Projects/`.

Use this first prompt with any AI assistant:

```text
Read CLAUDE.md, AGENTS.md and the Research OS instructions. Then inspect the
Projects folder and tell me what projects and rounds exist, what needs review,
and what the next safe Research OS action is. Do not change files yet.
```

It is an AI-first research system designed to continuously transform research evidence into structured, traceable and reusable knowledge.

The primary output of research is **knowledge**. Reports, presentations and summaries are generated from that knowledge rather than being the end product themselves.

---

# License

Research OS is available for noncommercial use under the PolyForm
Noncommercial License 1.0.0. See `LICENSE.md`.

Commercial use requires separate prior written permission from the repository
owner. See `COMMERCIAL_USE.md`.

Research OS is provided as-is. Users are responsible for their own research
data, local backups, AI-provider configuration and review of AI-generated
outputs.

---

# Core Principles

- Knowledge is the primary product of research.
- Every insight must be traceable to evidence.
- AI assists researchers but does not replace human review.
- Reports are generated from knowledge, not the other way around.
- Prefer extending existing concepts over introducing new ones.
- Evidence should preserve research richness before Research OS compresses it into patterns, insights or deliverables.

---

# Documentation

The documentation is the source of truth.

Before making architectural or implementation changes, always read the relevant documentation.

| Document | Purpose |
|----------|---------|
| **00 Vision** | Why Research OS exists and the problems it solves. |
| **01 Research Principles** | The research principles that guide the system. |
| **02 Architecture** | The conceptual architecture and system boundaries. |
| **03 Domain Model** | The core entities and relationships within the system. |
| **04 AI Agents** | How specialized AI agents collaborate with researchers. |
| **05 Knowledge Pipeline** | How research flows through the system from raw input to deliverables. |
| **08 Contribution Principles** | How humans and AI assistants should change the system. |
| **09 Project Handover** | Original project background and handover context for future contributors. |
| **11 Setup** | How to install and update Research OS through GitHub and Docker. |
| **13 License And Terms** | License and commercial-use terms. |
| **FILE_STRUCTURE** | Practical guide to the folders, researcher actions, and AI work files. |

If implementation conflicts with the documentation, update the documentation first.

---

# Repository Structure

```text
UX Research/
├── Research OS/
│   ├── docs/
│   ├── agents/
│   ├── research_os.py
│   ├── research-os
│   └── README.md
└── Projects/
    └── example-project/
        ├── 00-ai-work-files/
        ├── 01-input-source-files/
        └── 02-rounds/
```

The repository is organised around **research projects**.

Each project contains one or more **research rounds**.

Each project may also contain project-level input that informs the enduring
context for the research program, such as stakeholder interviews, product
frameworks, strategy decks, research archives, meeting recordings and product
documentation.

Project-level input is processed as Sources, but it is used to update Program
Context. It must not automatically become round Evidence.

Each round contains:

- `00-ai-work-files/` for AI work, accepted knowledge, review queues and traceability
- `01-input-source-files/` for original round source material
- `02-output-deliverables/` for reviewable and final output

Each round also has a **research lens**. The default is `Neutral research lens`,
which preserves the current Research OS behavior. A round can select a
specialized lens, such as `Consumer product & growth lens`, when synthesis needs
an additional domain-specific interpretation frame. Lenses are additive
instructions on top of common Research OS principles; they must not override
evidence traceability, uncertainty, contradictions or researcher review.

---

# Typical Workflow

```
Create Project
        ↓
Create Research Round
        ↓
Add Source Material
        ↓
Extract Rich Evidence
        ↓
Review Findings & Knowledge
        ↓
Update Knowledge
        ↓
Create Recommendations
        ↓
Generate Deliverables
```

The goal is to continuously grow the knowledge base as new research becomes available.

---

# Running the MVP

## 1. Create a Project

From the `Research OS` folder:

```sh
./research-os project create --name "New Product Area"
```

## 2. Create a Research Round

From the `Research OS` folder:

```sh
./research-os round create --project new-product-area --date 2026-07-29 --name "Concept Test 01"
```

## 3. Add Source Material

Add transcripts, notes, recordings and any supporting documents to the round.

You can also add durable project-level input to the project sources folder when
the material should inform the context across multiple rounds rather than belong
to one specific study.

## 4. Process New Input

Run the processing pipeline to extract evidence and update the project knowledge.

Run the project input pipeline when project-level material should update Program
Context.

## 5. Review

Review AI-generated findings and knowledge before accepting changes.

Research OS intentionally separates rich evidence extraction from review decisions. Evidence can contain many small, traceable observations from an interview. By default, Codex/Cowork should curate normal source-backed Evidence directly and ask the researcher to review only Evidence attention items: low-confidence observations, weakly relevant items, participant backstory, over-compressed observations, contradictions/tensions, narrow support for important claims or Evidence with high downstream impact.

Review cards should be actionable. They should show the actual observation, Pattern, Insight or Recommendation being reviewed, plus the reason it needs attention. Avoid generic proposal text that only references an ID without showing the claim.

Before synthesis moves downstream, Research OS also runs lightweight quality
gates. These gates do not make review decisions. They flag likely gaps such as
missing timestamps, weak support, missing contradicting evidence, missing
assumptions/open questions or unclear `Helps us understand` fields.

Review decisions and notes feed Looped Learning. `Needs changes`, `No`, and
`Yes` with notes can become reviewable Research OS-wide learning suggestions
that future Codex/Cowork runs must read before processing.

Synthesis should be stage-gated. For Evidence, Patterns, Insights and
Recommendations, Research OS should finish and review one stage before advancing
to the next. If Evidence review is still pending, do not generate or update
Patterns. If Pattern review is still pending, do not generate or update Insights.
If Insight review is still pending, do not generate or update Recommendations.
If Recommendation review is still pending, do not update Current Understanding or
generate deliverables.

The normal researcher workflow should use one `continue synthesis` prompt or
dashboard action. That prompt should read the current review state, apply
completed decisions, advance exactly one safe next stage, create reviewable items
for that stage and then stop. Stage-specific prompts are useful as manual repair
or focused rerun tools, but should not be required for ordinary review cycles.

## 6. Recommendations

Recommendations turn accepted or reviewable research knowledge into concrete next
steps for the concept, prototype, product, workflow, experiment strategy,
communication or follow-up research.

Each Recommendation should use a simple two-step structure:

- `What we learned`
- `What we should do`

Recommendations are reviewable. They may be based on accepted Insights, Patterns
or Evidence, including one strong and traceable observation when that observation
is important. They should remain concrete enough to stand alone without forcing
the researcher to infer what was unclear, useful, risky or actionable.

## 7. Open The Dashboard

Use the local dashboard to see projects, rounds, pending reviews and new or
changed files waiting for processing. Review decisions can be made directly in
the web UI.

Recommended local setup:

```sh
scripts/run-dashboard-docker.sh
```

Then open:

```text
http://127.0.0.1:8765/
```

Docker runs the dashboard in a small local container and mounts the `UX Research`
folder, so Research OS still reads and writes the same local files. This avoids
macOS LaunchAgent and Python permission issues around binding a local web server.

Recommended local location:

```text
~/UX Research/
```

Keep the active workspace outside `Documents`, Desktop and iCloud Drive to avoid
common macOS permission and backup issues. Research OS can still back up to
iCloud from this local workspace.

The launcher creates this local workspace shape if `Projects/` is missing:

```text
UX Research/
├── Research OS/
└── Projects/
```

The easiest setup is: install Docker Desktop, clone `Research OS` into a folder
named `UX Research`, run `scripts/run-dashboard-docker.sh`, then open
`http://127.0.0.1:8765/`.

To start Research OS again later:

1. Open Docker Desktop.
2. Wait until Docker is fully started.
3. Run:

   ```sh
   cd "$HOME/UX Research/Research OS"
   scripts/run-dashboard-docker.sh
   ```

4. Open `http://127.0.0.1:8765/`.

You can also start the existing `research-os-dashboard` container from Docker
Desktop's **Containers** screen.

On Mac, Safari can add the dashboard to the Dock:

1. Open `http://127.0.0.1:8765/` in Safari.
2. Choose `File` -> `Add to Dock...`.
3. Name it `Research OS` and click **Add**.

The Dock item opens Research OS like a small local app. Docker Desktop still
needs to be running in the background.

To stop it:

```sh
docker compose down
```

Manual fallback:

```sh
./research-os dashboard
```

The dashboard writes transparent `status.json` snapshots at project and round
level while it scans the filesystem.

Older macOS service fallback:

```sh
scripts/install-dashboard-service.sh
```

Then open the dashboard in Safari and use `File` -> `Add to Dock...` to make it
a local Dock web app. See `docs/10 Dashboard Service.md` for uninstall and log
locations.

## 8. Generate Deliverables

Generate reports, presentations and other outputs from the approved knowledge.

Deliverables use a two-step lifecycle:

1. Draft or update a reviewable Markdown source file.
2. Review that Markdown source in the dashboard until every active section is `Looks good` with no notes.
3. Export or finalize the approved artefact, such as a PDF, copyable deck prompt, ready-to-post Slack message or Figma/FigJam notes.

Do not treat `Generate deliverable` as PDF export. Markdown generation is the review step; exporting or finalizing is a separate explicit step after approval. Approved, unchanged sections should stay ready/editable in later review iterations instead of being surfaced again as active review work.

For shareable PDF exports, preserve the approved Markdown wording exactly and only change the visual formatting. Use the configured company-branded report style when local branding assets are present: logo/header branding, accent rules, subtle section rules, executive-summary callout, confidential footer and page numbering. Bullets and numbered items should be easy to scan: keep the original bold lead sentence/title slightly stronger than the body, put the explanation directly below it in the same text column, avoid hanging or stepped indents, and leave enough whitespace between items.

---

# AI Providers

By default, Research OS runs in Codex-controlled mode.

Codex-controlled mode allows the workflow to run without paid APIs while avoiding fake local AI analysis. Deterministic file processing still runs locally; interpretation and synthesis should be done through Codex or an API-backed provider.

For higher-quality extraction and synthesis, configure an external provider in `.env`.

Example:

```text
AI_PROVIDER=openai
```

---

# Development Guidelines

When contributing to Research OS:

1. Read the relevant documentation before making changes.
2. Treat the documentation as the source of truth.
3. Prefer extending existing concepts over creating new ones.
4. Keep every insight traceable to its original evidence.
5. Keep components small, composable and easy to understand.
6. Update the documentation whenever architectural decisions change.
7. Favour long-term maintainability over short-term convenience.

The objective is not simply to build software.

The objective is to build an operating system that continuously transforms research into reusable organisational knowledge.
