# START HERE - Install Research OS

This guide is for someone who has never used Research OS before.

You do not need to code. You only need to install Docker Desktop, put the folder
in the right place and paste one command into Terminal.

## Quick Overview

In this guide you will:

1. Install Docker Desktop so Research OS can run locally.
2. Check or install Git so your Mac can download Research OS from GitHub.
3. Pull Research OS from GitHub into `~/UX Research/Research OS`.
4. Create the local `~/UX Research/Projects` folder for research work.
5. Start the Research OS dashboard in your browser.
6. Connect Codex, Claude or another AI tool to the full `~/UX Research` folder.
7. Paste the first orientation prompt so the AI tool reads the Research OS
   instructions before changing files.
8. Use the purple AI buttons in the dashboard to copy Research OS prompts, then
   paste those prompts into your AI tool.

## How Research OS Works

Research OS is a local dashboard plus local folders. The AI tool does the
research processing by reading and editing those same folders.

```text
Your Mac
+--------------------------------------------------------------+
| ~/UX Research                                                |
|                                                              |
|  +---------------------+        +-------------------------+  |
|  | Research OS         |        | Projects                |  |
|  | dashboard + scripts |        | sources + reviews      |  |
|  |                     |        | evidence + deliverables |  |
|  +----------+----------+        +-----------^-------------+  |
|             |                               |                |
|             | reads status                  | reads/writes    |
|             v                               |                |
|  +---------------------+   copy prompt   +--+--------------+ |
|  | Browser dashboard   | --------------> | AI tool         | |
|  | review + status UI  | <-------------- | Codex or Claude | |
|  +---------------------+   refresh UI    +-----------------+ |
|                                                              |
+--------------------------------------------------------------+
```

The dashboard does not make AI decisions by itself. It shows status, reviews and
purple AI prompt buttons. You copy those prompts into your AI tool, the AI tool
updates the local files, and the dashboard refreshes to show what changed.

## What You Will Get

After setup, you open Research OS in your browser:

```text
http://127.0.0.1:8765/
```

Your research files stay local on your own computer in:

```text
UX Research/Projects
```

## Step 1 - Install Docker Desktop

Docker is the app that lets Research OS run locally on your computer.

1. Open the official Docker install page:

   ```text
   https://docs.docker.com/desktop/setup/install/mac-install/
   ```

2. Download the right version for your Mac:

   - **Mac with Apple silicon** if your Mac has an M1, M2, M3 or M4 chip.
   - **Mac with Intel chip** if you have an older Intel Mac.

3. Open the downloaded `Docker.dmg` file.
4. Drag Docker into the `Applications` folder.
5. Open Docker from `Applications`.
6. Wait until Docker has fully started.

Docker is ready when you see the Docker icon in the Mac menu bar and Docker
Desktop is no longer showing a startup screen.

## Step 2 - Install From GitHub

Research OS is installed and updated through GitHub.

First make sure Git is available. Git is the small tool that downloads Research
OS from GitHub and pulls updates later.

Paste this into Terminal:

```sh
git --version
```

What can happen:

- If Terminal shows a version number, Git is already installed.
- If a Mac popup asks you to install Apple command line tools, click install and
  wait until it finishes. Then run `git --version` again.
- If that does not work, install Git from:

  ```text
  https://git-scm.com/download/mac
  ```

Then paste this into Terminal:

```sh
mkdir -p "$HOME/UX Research"
git clone https://github.com/Jiptv/Research-OS.git "$HOME/UX Research/Research OS"
mkdir -p "$HOME/UX Research/Projects"
cd "$HOME/UX Research/Research OS"
```

This keeps the active Research OS workspace outside `Documents`, Desktop and
iCloud Drive. That avoids common macOS permission and backup issues. Research OS
can still back up to iCloud from this local workspace if you turn backup on in
Settings. Backup controls are hidden by default for new installs.

The final folder shape should be:

```text
Home folder/
└── UX Research/
    ├── Research OS/
    └── Projects/
```

Important: do not rename `UX Research`, `Research OS` or `Projects`.

To get Research OS updates later:

```sh
cd "$HOME/UX Research/Research OS"
git pull
scripts/run-dashboard-docker.sh
```

## Step 3 - Open Terminal

1. Press `Command + Space` to open Spotlight.
2. Type:

   ```text
   Terminal
   ```

3. Press Enter.

## Step 4 - Go To The Research OS Folder

Paste this into Terminal and press Enter:

```sh
cd "$HOME/UX Research/Research OS"
```

If it works, Terminal usually does not show a special success message. That is
fine.

If you see `No such file or directory`, the `UX Research` folder is probably not
in your home folder, or one of the folder names was changed.

## Step 5 - Start Research OS

Paste this into Terminal and press Enter:

```sh
scripts/run-dashboard-docker.sh
```

The first run can take a few minutes because Docker needs to build the local
Research OS environment.

When it works, you should see:

```text
Research OS dashboard: http://127.0.0.1:8765/
```

## Step 6 - Open Research OS

Open Safari, Chrome, Arc or another browser and go to:

```text
http://127.0.0.1:8765/
```

Keep Docker Desktop open while using Research OS.

## Optional - Add Research OS To Your Dock On Mac

If you use Safari, you can make Research OS feel like a normal Mac app:

1. Open Safari.
2. Go to:

   ```text
   http://127.0.0.1:8765/
   ```

3. In the Mac menu bar, click:

   ```text
   File > Add to Dock...
   ```

4. Name it `Research OS`.
5. Click **Add**.

You can now open Research OS from your Dock. Docker Desktop still needs to be
running in the background.

## Stop Research OS

If you want to stop Research OS:

```sh
cd "$HOME/UX Research/Research OS"
docker compose down
```

## Start Research OS Again Later

Use these steps the next time you want to use Research OS.

1. Open Docker Desktop from your `Applications` folder.
2. Wait until Docker has fully started.

   Docker is ready when the Docker icon is visible in the Mac menu bar and
   Docker Desktop is no longer showing a startup screen.

3. Open Terminal and paste:

   ```sh
   cd "$HOME/UX Research/Research OS"
   scripts/run-dashboard-docker.sh
   ```

4. Open Research OS in your browser:

   ```text
   http://127.0.0.1:8765/
   ```

If you already see a `research-os-dashboard` container in Docker Desktop, you
can also start it there:

1. Open Docker Desktop.
2. Go to **Containers**.
3. Find `research-os-dashboard`.
4. Click the start/play button.
5. Open:

   ```text
   http://127.0.0.1:8765/
   ```

If you are unsure, use the Terminal command. It is safe to run again.

## Update Research OS Later

Open Docker Desktop first, then open Terminal and paste:

```sh
cd "$HOME/UX Research/Research OS"
git pull
scripts/run-dashboard-docker.sh
```

Then open Research OS:

```text
http://127.0.0.1:8765/
```

## Where To Put Research Files

Put research projects here:

```text
~/UX Research/Projects/
```

Research OS creates the `Projects` folder automatically if it does not exist
yet.

## Where To Put A Company Logo

Optional local branding files can go here:

```text
~/UX Research/Research OS/branding/company-logo.png
~/UX Research/Research OS/branding/company-footer.png
```

Branding files are local. They are not meant to be committed to the Research OS
repository.

## Using An AI Assistant With Research OS

Research OS is designed so an AI coding assistant can read and change files in
the `UX Research` folder.

This can be Codex, Claude, Claude Code or another AI assistant that can work
with a local project folder.

Use this folder as the project/workspace:

```text
~/UX Research
```

Do not add only the `Research OS` subfolder. The assistant also needs access to
`Projects`, because that is where research project files live.

The shared `UX Research` folder contains `CLAUDE.md` and `AGENTS.md` files for
AI assistants. These tell Claude, Codex or another coding agent how to work with
Research OS when it opens the project.

### The Most Important Rule

When an AI tool asks which folder or project to open, select:

```text
~/UX Research
```

Do not select only:

```text
~/UX Research/Research OS
```

The AI assistant needs both folders:

- `Research OS` contains the system instructions and scripts.
- `Projects` contains the actual research work.

### First Prompt To Use

After opening `~/UX Research` in your AI assistant, paste this:

```text
Read CLAUDE.md, AGENTS.md and the Research OS instructions. Then inspect the
Projects folder and tell me what projects and rounds exist, what needs review,
and what the next safe Research OS action is. Do not change files yet.
```

This helps the assistant orient itself before doing work.

### How Dashboard Prompts Work

Research OS does not run AI work by itself. The dashboard shows purple AI
buttons for work that should be done by Codex, Claude or another AI tool.

Use them like this:

1. Click the purple AI button in the dashboard.
2. The prompt is copied to your clipboard.
3. Paste that prompt into your AI tool.
4. Let the AI tool work in the local `~/UX Research` folder.
5. Return to the dashboard to review changes, check status or copy the next
   prompt.

### Codex / ChatGPT Desktop

1. Open the ChatGPT desktop app.
2. Switch to **Codex**.
3. Choose **Add project** or **Open folder**.
4. Select:

   ```text
   ~/UX Research
   ```

5. Start a task and describe what you want Codex to do.

Example prompt:

```text
Read CLAUDE.md, AGENTS.md and the Research OS instructions. Then create a new
research project for [product area], and create a first research round called
[study name].
```

Codex can help with tasks like creating project folders, processing research
input, updating markdown files, generating review prompts and preparing
deliverables.

### Claude Or Claude Code

Use the same idea in Claude or Claude Code:

1. Open Claude.
2. Add or open a local project/workspace folder.
3. Select:

   ```text
   ~/UX Research
   ```

4. Ask Claude to read the Research OS instructions before changing files.

Example prompt:

```text
Read CLAUDE.md and the Research OS instructions in this folder first. Then help
me add a new research round and prepare the project structure.
```

Another useful first prompt is:

```text
Read CLAUDE.md and the Research OS instructions. Then inspect the Projects
folder and tell me what projects and rounds exist, what needs review, and what
the next safe Research OS action is.
```

### Other AI Assistants

If you use another AI assistant, use the same pattern:

1. Open or add a local project/workspace.
2. Select:

   ```text
   ~/UX Research
   ```

3. Tell it to read:

   ```text
   CLAUDE.md
   AGENTS.md
   Research OS/AI_ASSISTANT_GUIDE.md
   Research OS/README.md
   ```

4. Ask it to explain the current project state before changing files.

If the AI assistant cannot open local folders, connect it to the local
`~/UX Research` workspace or share the relevant files manually. Make sure it
receives both `Research OS` and `Projects` context.

## If Something Does Not Work

### Docker command not found

Docker Desktop is not installed, or Docker is not running.

Open Docker Desktop from `Applications`, wait until it has started, then try:

```sh
scripts/run-dashboard-docker.sh
```

### Cannot connect to Docker

Docker Desktop has not fully started yet.

Open Docker Desktop and wait until it is ready. Then try again.

### Port 8765 is already in use

Research OS may already be running.

Open:

```text
http://127.0.0.1:8765/
```

Or stop it first:

```sh
docker compose down
```

### Start Over Cleanly

```sh
cd "$HOME/UX Research/Research OS"
docker compose down
scripts/run-dashboard-docker.sh
```
