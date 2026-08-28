# Change Notes

Human-readable notes about what changed in Research OS.

Research OS uses small version numbers while it is still early:

- `v0.1.x` for small fixes, documentation updates and setup improvements.
- `v0.2.0`, `v0.3.0`, etc. for visible new features.
- `v1.0.0` only when Research OS is stable enough for everyday use.

## v0.1.9 - Synthesis and public wording cleanup

Improved synthesis guidance and removed a company-specific PDF layout reference
from public instructions.

What changed:

- Refined Pattern, Insight and Knowledge Curator agent guidance.
- Updated architecture and knowledge-pipeline notes for safer synthesis flow.
- Improved dashboard support for the updated review/synthesis workflow.
- Replaced a company-specific PDF layout reference with generic public wording.

## v0.1.8 - Review and PDF export polish

Improved review clarity and PDF export handling.

What changed:

- Review analytics now use expanded review items, including saved decisions.
- Changed review items can reset stale decisions so they are reviewed again.
- Review pages explain why an item needs review.
- PDF exports use clear versioned file names and avoid overwriting older PDFs.
- Deliverable actions link to the latest exported PDF when one exists.
- Polished review/export buttons and changed-item styling.

## v0.1.7 - Dashboard signals and settings tabs

Improved the dashboard with clearer round-level signals and a more organized
settings area.

What changed:

- Added round signal cards for checklist progress, recent runs, review status
  and source coverage.
- Added richer research lens descriptions in settings.
- Split settings into General, Backup and Lenses tabs.
- Kept the new dashboard checks local and file-based.

## v0.1.6 - Restart instructions

Made it clearer how to start Research OS again after the first installation.

What changed:

- Added simple steps: open Docker Desktop, start Research OS, open the browser.
- Explained that `scripts/run-dashboard-docker.sh` is safe to run again.
- Added the Docker Desktop Containers screen as an alternative way to start the
  existing `research-os-dashboard` container.

## v0.1.5 - Git install instructions

Made the GitHub setup clearer for people who do not already have Git installed.

What changed:

- Added a `git --version` check to the README and setup docs.
- Explained that macOS may ask to install Apple command line tools.
- Added the official Git for Mac download link as a fallback.

## v0.1.4 - Simpler public setup

Cleaned up the public setup flow so GitHub + Docker is the main way to install
and update Research OS.

What changed:

- Consolidated setup documentation into one clearer setup guide.
- Removed older zip-package and release-image helper files from the public repo.
- Simplified license and public-use explanation.
- Improved wording across the vision, architecture and AI-agent docs.
- Kept the dashboard code aligned with the cleaner setup flow.

## v0.1.3 - Human-readable release notes

Added this changelog so people can see what changed in plain language.

What changed:

- Added human-readable release notes.
- Linked the release notes from the README.
- Documented the basic version-numbering approach.

## v0.1.2 - Docker Compose setup

Added clearer Docker Compose examples for people who want to run Research OS
with Docker directly.

What changed:

- Added a local `docker-compose.yml` example that builds Research OS from the
  repository.
- Explained why Docker must mount the whole `UX Research` workspace, not only
  the `Research OS` folder.
- Linked the Docker Compose examples from the README.

## v0.1.1 - GitHub install and update instructions

Made it easier to install Research OS directly from GitHub.

What changed:

- Added copy-paste `git clone` setup instructions.
- Added simple `git pull` update instructions.
- Added GitHub setup notes to the README, `START_HERE.md` and setup guide.
- Clarified that local research projects stay in `UX Research/Projects` and do
  not belong in the Research OS repository.

## v0.1.0 - First shareable Research OS version

First tagged version for sharing Research OS with other people.

What changed:

- Added the round-level monitoring toggle in the dashboard.
- New research rounds are monitored by default.
- Finished rounds can be switched off so Research OS stops checking them for new
  work.
- Projects stop asking for attention when all rounds are unmonitored, unless
  project context or project sources still need attention.
- Removed the large dashboard hero/header so the app opens closer to the actual
  work.
- Made stage progress bars visually consistent.
- Improved Docker/shared-workspace setup handling.
- Added noncommercial license and commercial-use permission terms.
- Added notes to keep local company branding, secrets and private research data
  out of Git.

## Before v0.1.0

Early preparation work:

- Created the initial Research OS repository.
- Added setup and Docker documentation.
- Added license and terms guidance.
