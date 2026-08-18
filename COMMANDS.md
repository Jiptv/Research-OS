# Research OS Commands

Use these Terminal commands from the `Research OS` folder. Processing and prompting are currently driven from Codex/Cowork through the dashboard. Backend API processing and local stubs are disabled.

## Projects Level

```sh
./research-os project create --name "New Product Area"
```

## Dashboard

Recommended local setup:

```sh
scripts/run-dashboard-docker.sh
```

The launcher creates `../Projects` next to `Research OS` if it is missing.

Manual fallback:

```sh
./research-os dashboard
```

Then open:

```text
http://127.0.0.1:8765/
```

To keep the dashboard running outside Codex after login:

```sh
scripts/install-dashboard-service.sh
```

To remove that background service:

```sh
scripts/uninstall-dashboard-service.sh
```

## Project Level

```sh
./research-os round create --project new-product-area --date 2026-07-23 --name "Concept Test 01"
```

## Round Level

After adding a transcript or other source material, open the dashboard and use the purple prompt icon for the relevant phase. If you run the CLI command below, it only logs and prints a Codex handoff prompt; it does not process sources itself.

```sh
./research-os pipeline run ../Projects/new-product-area/02-rounds/2026-07-23-concept-test-01
```

To draft reviewable Markdown deliverables:

```sh
./research-os deliverable request ../Projects/new-product-area/02-rounds/2026-07-23-concept-test-01 --type research-summary
./research-os deliverable request ../Projects/new-product-area/02-rounds/2026-07-23-concept-test-01 --type stakeholder-slack-message --audience stakeholders
./research-os deliverable request ../Projects/new-product-area/02-rounds/2026-07-23-concept-test-01 --type post-it-notes --audience workshop
./research-os deliverable generate ../Projects/new-product-area/02-rounds/2026-07-23-concept-test-01
```

`deliverable generate` also only logs and prints a Codex handoff prompt. Codex/Cowork should create the actual deliverable file.

Deliverables then follow the review/export lifecycle:

1. Codex/Cowork drafts or updates the Markdown source.
2. The researcher reviews the Markdown sections in the dashboard.
3. Codex/Cowork applies review notes until every active section is `Looks good` with no notes.
4. Codex/Cowork exports or finalizes the approved artefact, such as a PDF for `research-summary.md` or `design-actions-summary.md`.

Do not expect `deliverable generate` to create PDFs or final shareable artefacts directly.

When exporting PDFs, preserve the approved Markdown text exactly. Use only visual formatting changes: configured branding, accent rules, callouts, footer/page numbering and scan-friendly bullets. For bullet and numbered-list items, keep the original bold lead sentence/title and place the explanation directly underneath in the same text column, without a hanging or stepped indent.
