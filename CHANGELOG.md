# Release Notes

Human-readable notes about what changed in each Research OS release.

Research OS uses small version numbers while it is still early:

- `v0.1.x` for small fixes, documentation updates and setup improvements.
- `v0.2.0`, `v0.3.0`, etc. for visible new features.
- `v1.0.0` only when Research OS is stable enough for broader everyday use.

## v0.1.2 - Docker Compose examples

Added clearer Docker Compose examples for people who want to run Research OS
with Docker directly.

What changed:

- Added a local `docker-compose.yml` example that builds Research OS from the
  repository.
- Added a prebuilt-image example for people who later want to use a published
  Docker image.
- Explained why Docker must mount the whole `UX Research` workspace, not only
  the `Research OS` folder.
- Linked the Docker Compose examples from the README.

## v0.1.1 - GitHub install and update instructions

Made it easier for colleagues to install Research OS directly from GitHub.

What changed:

- Added copy-paste `git clone` setup instructions.
- Added simple `git pull` update instructions.
- Added GitHub setup notes to the README, `START_HERE.md` and colleague setup
  guide.
- Clarified that local research projects stay in `UX Research/Projects` and do
  not belong in the public Git repository.

## v0.1.0 - First shareable Research OS release

First tagged release for sharing Research OS with other people.

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
- Added public sharing notes and checks to reduce the risk of publishing local
  company branding, secrets or private research data.

## Before v0.1.0

Early public preparation work:

- Created the initial public Research OS repository.
- Added setup, Docker and colleague-sharing documentation.
- Added public release checklist and license/terms guidance.
