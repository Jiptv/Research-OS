# Dashboard Service

The Research OS dashboard can run as a local macOS LaunchAgent.

This keeps the dashboard available outside Codex at:

```text
http://127.0.0.1:8765/
```

## Install

From the Research OS folder:

```sh
scripts/install-dashboard-service.sh
```

The service:

- starts automatically after login
- restarts if it exits
- serves only on `127.0.0.1`
- writes logs to `~/Library/Logs/ResearchOS/`

The installer writes the LaunchAgent into:

```text
~/Library/LaunchAgents/com.research-os.dashboard.plist
```

It bootstraps the job into the current user launchd domain and points it at the
current local Research OS folder.

## macOS Folder Permission

If Research OS lives inside `~/Documents`, Desktop, or iCloud Drive, macOS may
block background services from reading the project folder. When that happens,
the installer removes the broken service and prints the log location.

The installer writes the LaunchAgent with the current absolute Research OS path,
so rerun it after moving the folder.

Fix options:

1. Grant Full Disk Access to the Python executable printed by the installer.
   This may be an Xcode Python path even when the command is `python3`.
2. Move the project outside protected or synced folders. In this setup the
   active local workspace is:

```text
~/UX Research
```

Then rerun the installer:

```sh
scripts/install-dashboard-service.sh
```

## Local Runtime With iCloud Backup

The active local workspace is:

```text
~/UX Research
```

Keep the dashboard runtime local. Use iCloud only as a backup or sync copy.

From the local Research OS folder:

```sh
scripts/backup-to-icloud.sh
```

By default this updates the iCloud backup workspace:

```text
~/Library/Mobile Documents/com~apple~CloudDocs/iCloud/UX Research/
```

The script mirrors:

```text
~/UX Research/Research OS -> iCloud/UX Research/Research OS
~/UX Research/Projects    -> iCloud/UX Research/Projects
```

You can also pass a different backup workspace destination:

```sh
scripts/backup-to-icloud.sh "/path/to/backup/UX Research"
```

The backup script mirrors the local workspace to the backup folder with `rsync`
and does not change the LaunchAgent runtime path.

## Automated iCloud Backup

Do not run the iCloud backup script as a default LaunchAgent unless macOS has
explicitly been allowed to let background shell tools write to iCloud Drive.
Without that permission, launchd may fail with `Operation not permitted` even
though the same script works when run manually from Terminal.

The safest default is:

- keep the dashboard runtime local
- run `scripts/backup-to-icloud.sh` manually when you want to refresh iCloud
- use iCloud as backup/sync only, not as the active dashboard runtime

## Add To Dock

After installing the service:

1. Open Safari.
2. Go to `http://127.0.0.1:8765/`.
3. Choose `File` -> `Add to Dock...`.
4. Name it `Research OS`.
5. Click `Add`.

The Dock item opens the dashboard as a standalone local web app. The LaunchAgent
keeps the local dashboard server running in the background.

## Uninstall

```sh
scripts/uninstall-dashboard-service.sh
```

## Manual Fallback

You can still run the dashboard manually:

```sh
./research-os dashboard
```

If the project folder moves, reinstall the service so the LaunchAgent points to
the new location.

## Reboot Troubleshooting

If the dashboard does not come back after a reboot, reinstall it from the local
runtime folder:

```sh
cd ~/UX\ Research/Research\ OS
scripts/install-dashboard-service.sh
```

Then verify launchd is running the local copy:

```sh
launchctl print gui/$(id -u)/com.research-os.dashboard
```

The output should show:

```text
state = running
working directory = /path/to/UX Research/Research OS
```

If it points to another path, rerun the installer from
your local `UX Research/Research OS` folder.
