# Colleague Setup

This guide is for teammates who want to run Research OS locally.

For the shortest non-technical setup guide, read:

```text
START_HERE.md
```

That guide also explains how to add the `UX Research` folder as a local
project/workspace in Codex or Claude.

Research OS stores research files on the local machine. Docker only runs the dashboard.

Expected local shape:

```text
UX Research/
├── Research OS/
└── Projects/
```

The dashboard launcher creates `Projects/` next to `Research OS/` if it does
not exist yet.

## Option A: Zip Package

Use this when you want to send one simple file.

1. Install Docker Desktop from the official Docker instructions:

   ```text
   https://docs.docker.com/desktop/setup/install/mac-install/
   ```

   Choose **Mac with Apple silicon** for M1/M2/M3/M4 Macs, or **Mac with Intel
   chip** for older Intel Macs.

2. Unzip `research-os-share-YYYYMMDD-HHMMSS.zip`.
3. Move the unzipped `UX Research` folder to your home folder:

   ```text
   ~/UX Research
   ```

   Keep the active workspace outside `Documents`, Desktop and iCloud Drive to
   avoid common macOS permission and backup issues. Research OS can still back
   up to iCloud from this local workspace.

4. Open Terminal and go to the Research OS folder:

   ```sh
   cd ~/UX\ Research/Research\ OS
   ```

5. Start the dashboard:

   ```sh
   scripts/run-dashboard-docker.sh
   ```

   The first run can take a few minutes because Docker builds the local
   Research OS container.

6. Open:

   ```text
   http://127.0.0.1:8765/
   ```

To stop:

```sh
docker compose down
```

The `Projects` folder next to `Research OS` is where local project files live.
Project data stays local by default and is not included in the share package.

Optional company branding can be placed here:

```text
~/UX Research/Research OS/branding/company-logo.png
```

Branding files stay local and are not meant to be committed to the public
Research OS repository.

## Make The Zip

From your own `Research OS` folder:

```sh
scripts/make-share-zip.sh
```

The zip is created in:

```text
../dist/
```

It includes the Research OS app and an empty `Projects` folder. It does not include your project data.

## Option B: Updates Via Git And Docker

Use this when colleagues should be able to pull updates.

Simple GitHub setup:

```sh
mkdir -p "$HOME/UX Research"
git clone https://github.com/Jiptv/Research-OS.git "$HOME/UX Research/Research OS"
mkdir -p "$HOME/UX Research/Projects"
cd "$HOME/UX Research/Research OS"
scripts/run-dashboard-docker.sh
```

Colleague update command:

```sh
cd "$HOME/UX Research/Research OS"
git pull
scripts/run-dashboard-docker.sh
```

Keep the local `UX Research/Projects` folder outside Git. Project data stays
local by default and should not be committed to the public Research OS
repository.

Optional container-registry setup:

- Publish the Docker image to GitHub Container Registry.
- Let colleagues update by pulling the latest image and restarting Docker.

Example image name:

```text
ghcr.io/your-org/research-os-dashboard:latest
```

Container-registry update command:

```sh
cd ~/UX\ Research/Research\ OS
RESEARCH_OS_IMAGE=ghcr.io/your-org/research-os-dashboard:latest docker compose -f docker-compose.release.yml pull
RESEARCH_OS_IMAGE=ghcr.io/your-org/research-os-dashboard:latest docker compose -f docker-compose.release.yml up -d
```

For day-to-day development, keep using:

```sh
docker compose up --build -d
```

## Docker Compose Example

Research OS already includes a working `docker-compose.yml`. Colleagues usually
do not need to create this file themselves.

If someone wants to understand or recreate the local Docker Compose setup, this
is the minimal shape:

```yaml
services:
  dashboard:
    image: research-os-dashboard:local
    build:
      context: .
    container_name: research-os-dashboard
    working_dir: /workspace/Research OS
    command: ["python3", "research_os.py", "dashboard", "--host", "0.0.0.0", "--port", "8765"]
    ports:
      - "127.0.0.1:8765:8765"
    environment:
      TZ: "Europe/Amsterdam"
      RESEARCH_OS_HOST_WORKSPACE_DIR: "${HOME}/UX Research"
      RESEARCH_OS_BACKUP_DIR: "/icloud/UX Research"
    volumes:
      - ..:/workspace
      - "${HOME}/Library/Mobile Documents/com~apple~CloudDocs/iCloud/UX Research:/icloud/UX Research"
    restart: unless-stopped
```

Run it from the `Research OS` folder:

```sh
cd "$HOME/UX Research/Research OS"
docker compose up --build -d
```

Then open:

```text
http://127.0.0.1:8765/
```

For a prebuilt image instead of local build, use `docker-compose.release.yml`
and set `RESEARCH_OS_IMAGE`:

```yaml
services:
  dashboard:
    image: ghcr.io/your-org/research-os-dashboard:latest
    container_name: research-os-dashboard
    working_dir: /workspace/Research OS
    command: ["python3", "research_os.py", "dashboard", "--host", "0.0.0.0", "--port", "8765"]
    ports:
      - "127.0.0.1:8765:8765"
    volumes:
      - ..:/workspace
    restart: unless-stopped
```

The important part is the volume mount:

```yaml
volumes:
  - ..:/workspace
```

That gives Docker access to both:

```text
UX Research/Research OS
UX Research/Projects
```

## Folder Shape

Research OS expects this shape:

```text
UX Research/
├── Research OS/
│   ├── research_os.py
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── scripts/
└── Projects/
```

This matters because Docker mounts the full `UX Research` folder into the container.

Inside each project, the top-level structure is:

```text
Projects/<project-id>/
├── 00-ai-work-files/
├── 01-input-source-files/
└── 02-rounds/
```

Inside each round, the visible structure is:

```text
02-rounds/<round-id>/
├── 00-ai-work-files/
├── 01-input-source-files/
└── 02-output-deliverables/
```

## Troubleshooting

Check that Docker sees the dashboard as healthy:

```sh
docker ps --filter name=research-os-dashboard
```

Check the health endpoint:

```sh
curl -fsS http://127.0.0.1:8765/api/health
```

Restart cleanly:

```sh
docker compose down
scripts/run-dashboard-docker.sh
```
