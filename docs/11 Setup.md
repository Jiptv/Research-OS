# Setup

This guide is for people who want to run Research OS locally.

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

## Option A: GitHub Pull And Docker

Use this as the default setup. Install once from GitHub, then pull updates when
Research OS changes.

1. Install Docker Desktop from the official Docker instructions:

   ```text
   https://docs.docker.com/desktop/setup/install/mac-install/
   ```

   Choose **Mac with Apple silicon** for M1/M2/M3/M4 Macs, or **Mac with Intel
   chip** for older Intel Macs.

2. Check whether Git is installed.

   Git is the tool that downloads Research OS from GitHub and pulls updates
   later.

   Paste this into Terminal:

   ```sh
   git --version
   ```

   What can happen:

   - If Terminal shows a version number, Git is already installed.
   - If a Mac popup asks you to install Apple command line tools, click install
     and wait until it finishes. Then run `git --version` again.
   - If that does not work, install Git from:

     ```text
     https://git-scm.com/download/mac
     ```

3. Open Terminal and install Research OS from GitHub:

   ```sh
   mkdir -p "$HOME/UX Research"
   git clone https://github.com/Jiptv/Research-OS.git "$HOME/UX Research/Research OS"
   mkdir -p "$HOME/UX Research/Projects"
   cd "$HOME/UX Research/Research OS"
   ```

   Keep the active workspace outside `Documents`, Desktop and iCloud Drive to
   avoid common macOS permission and backup issues. Research OS can still back
   up to iCloud from this local workspace if backup is turned on in Settings.
   Backup controls are hidden by default for new installs.

4. Start the dashboard:

   ```sh
   scripts/run-dashboard-docker.sh
   ```

   The first run can take a few minutes because Docker builds the local
   Research OS container.

5. Open:

   ```text
   http://127.0.0.1:8765/
   ```

To stop:

```sh
docker compose down
```

## Start Research OS Again Later

Use these steps after the first installation:

1. Open Docker Desktop from `Applications`.
2. Wait until Docker has fully started.
3. Open Terminal and run:

   ```sh
   cd "$HOME/UX Research/Research OS"
   scripts/run-dashboard-docker.sh
   ```

4. Open:

   ```text
   http://127.0.0.1:8765/
   ```

Alternative: in Docker Desktop, go to **Containers**, find
`research-os-dashboard`, click the start/play button, then open
`http://127.0.0.1:8765/`.

If you are unsure, use the Terminal command. It is safe to run again.

The `Projects` folder next to `Research OS` is where local project files live.
Project data stays local by default and should not be committed to the Research
OS repository.

Update command:

```sh
cd "$HOME/UX Research/Research OS"
git pull
scripts/run-dashboard-docker.sh
```

Optional company branding can be placed here:

```text
~/UX Research/Research OS/branding/company-logo.png
```

Branding files stay local and are not meant to be committed to the Research OS
repository.

For day-to-day use, keep using:

```sh
docker compose up --build -d
```

## Docker Compose Example

Research OS already includes a working `docker-compose.yml`. Most users do not
need to create this file themselves.

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
