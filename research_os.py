#!/usr/bin/env python3
"""Filesystem orchestrator for the Research OS MVP."""

from __future__ import annotations

import argparse
import hashlib
import html
import http.server
import json
import os
import re
import shutil
import socketserver
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parent
WORKSPACE_ROOT = ROOT.parent
AGENTS_DIR = ROOT / "agents"
LENSES_DIR = ROOT / "lenses"
PROJECTS_DIR = WORKSPACE_ROOT / "Projects"
LEGACY_PROJECTS_DIR = ROOT / "research" / "projects"
SHORTCUTS_DIR = ROOT / "Command Shortcuts"
LOOPED_LEARNING_DIR = ROOT / "08-looped-learning"
LOOPED_SIGNALS_FILE = LOOPED_LEARNING_DIR / "feedback-signals.jsonl"
LOOPED_SUGGESTIONS_FILE = LOOPED_LEARNING_DIR / "suggested-learnings.md"
LOOPED_ACTIVE_FILE = LOOPED_LEARNING_DIR / "active-learnings.md"
LOOPED_STATE_FILE = LOOPED_LEARNING_DIR / "learning-loop-state.json"
STATE_FILE = ".pipeline-state.json"
PROJECT_STATE_FILE = ".project-pipeline-state.json"
ROUND_MONITORING_FILE = ".round-monitoring.json"
QUALITY_GATE_WAIVERS_FILE = ".quality-gate-waivers.json"
QUALITY_GATE_CACHE_FILE = ".quality-gates-cache.json"
QUALITY_GATE_RULE_VERSION = "2026-08-19-ai-cleanups-v3"
DEFAULT_RESEARCH_LENS = "neutral"
BACKUP_STATUS_FILE = ROOT / ".backup-status.json"
UPDATE_STATUS_FILE = ROOT / ".update-status.json"
UPDATE_CHECK_INTERVAL = timedelta(hours=12)
GITHUB_CHANGELOG_URL = "https://github.com/Jiptv/Research-OS/blob/main/CHANGELOG.md"
GITHUB_REPO_URL = "https://github.com/Jiptv/Research-OS"
GITHUB_API_REPO_URL = "https://api.github.com/repos/Jiptv/Research-OS"
BACKUP_SCRIPT = ROOT / "scripts" / "backup-to-icloud.sh"
BACKUP_COMMAND = WORKSPACE_ROOT / "00 Sync Research OS to iCloud.command"
SETTINGS_FILE = ROOT / ".dashboard-settings.json"
SUPPORTED_DELIVERABLES = {
    "research-summary",
    "design-actions-summary",
    "powerpoint-preparation-prompt",
    "stakeholder-slack-message",
    "post-it-notes",
}
DELIVERABLE_REVIEW_ORDER = [
    ("research-summary", "Research summary"),
    ("design-actions-summary", "Design brief"),
    ("powerpoint-preparation-prompt", "PowerPoint preparation prompt"),
    ("stakeholder-slack-message", "Slack message"),
    ("post-it-notes", "Post-it notes"),
]
DELIVERABLE_DESCRIPTIONS = {
    "research-summary": "Reviewed research story and recommended next steps.",
    "design-actions-summary": "Design brief with concrete UX actions and user stories.",
    "powerpoint-preparation-prompt": "Reusable prompt for making a research readout deck.",
    "stakeholder-slack-message": "Ready-to-post stakeholder update for Slack.",
    "post-it-notes": "Workshop-ready insight notes for copying into Figma.",
}
DELIVERABLE_BUTTON_LABELS = {
    "research-summary": "Prepare",
    "design-actions-summary": "Prepare",
    "powerpoint-preparation-prompt": "Prepare",
    "stakeholder-slack-message": "Prepare",
    "post-it-notes": "Prepare",
}
DELIVERABLE_COPY_LABELS = {
    "research-summary": "create research summary",
    "design-actions-summary": "create design brief",
    "powerpoint-preparation-prompt": "create deck prompt",
    "stakeholder-slack-message": "create Slack message",
    "post-it-notes": "create post-it notes",
}
NON_REVIEWABLE_DELIVERABLES: set[str] = set()
ROUND_DIRS = {
    "sources": ("01-input-source-files", "01-source-files", "01-source-material", "01-sources", "sources"),
    "representations": ("00-ai-work-files/01-source-representations", "90-ai-work-files/01-source-representations", "90-work-files/02-representations", "02-representations", "representations"),
    "evidence": ("00-ai-work-files/02-evidence-observations", "90-ai-work-files/02-evidence-observations", "02-evidence-observations", "03-evidence", "evidence"),
    "method": ("00-ai-work-files/02-method-assessments", "90-ai-work-files/02-method-assessments", "90-work-files/04-method-assessments", "04-method-assessments"),
    "patterns": ("00-ai-work-files/03-patterns-found-across-evidence", "90-ai-work-files/03-patterns-found-across-evidence", "03-patterns-found-across-evidence", "05-patterns", "patterns"),
    "insights": ("00-ai-work-files/04-insights-from-patterns", "90-ai-work-files/04-insights-from-patterns", "04-insights-from-patterns", "06-insights", "insights"),
    "recommendations": ("00-ai-work-files/05-recommendations", "90-ai-work-files/05-recommendations", "05-recommendations", "07-recommendations", "recommendations"),
    "reviews": ("00-ai-work-files/06-review-queue", "90-ai-work-files/06-review-queue", "06-review-queue", "05-review-queue", "07-reviews", "reviews"),
    "deliverables": ("02-output-deliverables", "02-deliverables", "07-deliverables", "06-deliverables", "08-deliverables", "deliverables"),
    "pipeline_runs": ("00-ai-work-files/09-pipeline-runs", "90-ai-work-files/09-pipeline-runs", "90-work-files/09-pipeline-runs", "09-pipeline-runs", "pipeline-runs"),
    "work_files": ("00-ai-work-files", "90-ai-work-files", "90-work-files"),
}
PROJECT_DIRS = {
    "sources": ("01-input-source-files", "01-source-files", "01-project-context-sources", "00-project-sources", "project-sources"),
    "representations": ("00-ai-work-files/01-project-source-representations", "90-ai-work-files/01-project-source-representations", "90-work-files/01-project-representations", "01-project-representations", "project-representations"),
    "reviews": ("00-ai-work-files/02-review-project-context-proposals", "90-ai-work-files/02-review-project-context-proposals", "02-review-project-context-proposals", "02-project-reviews", "project-reviews"),
    "pipeline_runs": ("00-ai-work-files/03-project-pipeline-runs", "90-ai-work-files/03-project-pipeline-runs", "90-work-files/03-project-pipeline-runs", "03-project-pipeline-runs", "project-pipeline-runs"),
    "rounds": ("02-rounds", "03-research-rounds", "04-rounds", "rounds"),
    "work_files": ("00-ai-work-files", "90-ai-work-files", "90-work-files"),
}
ROUND_FILES = {
    "overview": ("00-ai-work-files/00-round-overview.md", "90-ai-work-files/00-round-overview.md", "00-round-overview.md", "round.md"),
    "questions": ("00-ai-work-files/01-research-questions.md", "90-ai-work-files/01-research-questions.md", "01-research-questions.md", "research-questions.md"),
    "pipeline": ("00-ai-work-files/90-pipeline-settings.yaml", "00-ai-work-files/90-pipeline-settings.yaml", "90-pipeline-settings.yaml", "pipeline.yaml"),
}
PROJECT_FILES = {
    "overview": ("00-ai-work-files/00-project-overview.md", "90-ai-work-files/00-project-overview.md", "00-project-overview.md", "project.md"),
    "context": ("00-ai-work-files/01-project-context.md", "90-ai-work-files/01-project-context.md", "01-project-context.md", "program-context.md"),
    "understanding": ("00-ai-work-files/02-current-understanding.md", "90-ai-work-files/02-current-understanding.md", "02-current-understanding.md", "current-understanding.md"),
    "opportunities": ("00-ai-work-files/03-opportunities.md", "90-ai-work-files/03-opportunities.md", "03-opportunities.md", "opportunities.md"),
    "decisions": ("00-ai-work-files/04-decisions.md", "90-ai-work-files/04-decisions.md", "04-decisions.md", "decisions.md"),
}


@dataclass
class StageResult:
    key: str
    name: str
    status: str
    input_files: list[Path]
    output_files: list[Path]
    started: datetime
    completed: datetime
    warnings: list[str]
    errors: list[str]
    review_required: bool = False


STAGES = [
    ("source_intake", "source-intake", "Source Intake Agent", "source-intake-agent.md"),
    ("source_processing", "source-processing", "Source Processing Agent", "source-processing-agent.md"),
    ("evidence_extraction", "evidence-extraction", "Evidence Extractor Agent", "evidence-extractor-agent.md"),
    ("method_assessment", "method-assessment", "Method Specialist Agent", "method-specialist-agent.md"),
    ("pattern_detection", "pattern-detection", "Pattern Detector Agent", "pattern-detector-agent.md"),
    ("insight_synthesis", "insight-synthesis", "Insight Synthesizer Agent", "insight-synthesizer-agent.md"),
    ("recommendation_synthesis", "recommendation-synthesis", "Recommendation Synthesizer Agent", "recommendation-synthesizer-agent.md"),
    ("quality_critique", "quality-critique", "Quality Critic Agent", "quality-critic-agent.md"),
    ("knowledge_curation", "knowledge-curation", "Knowledge Curator Agent", "knowledge-curator-agent.md"),
]


def now() -> datetime:
    return datetime.now().replace(microsecond=0)


def rel(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(ROOT).as_posix()
    except ValueError:
        return os.path.relpath(resolved, ROOT).replace(os.sep, "/")


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def resolve_research_path(path: Path) -> Path:
    if path.is_absolute():
        return path.resolve()
    root_candidate = (ROOT / path).resolve()
    if root_candidate.exists():
        return root_candidate
    workspace_candidate = (WORKSPACE_ROOT / path).resolve()
    if workspace_candidate.exists():
        return workspace_candidate
    projects_candidate = (projects_dir() / path).resolve()
    if projects_candidate.exists():
        return projects_candidate
    return root_candidate


def default_backup_dir() -> Path:
    return Path(os.environ.get("RESEARCH_OS_BACKUP_DIR", str(WORKSPACE_ROOT / "iCloud backup"))).expanduser()


def host_workspace_dir() -> Path | None:
    value = str(os.environ.get("RESEARCH_OS_HOST_WORKSPACE_DIR", "")).strip()
    if not value:
        return None
    return Path(value).expanduser()


def host_display_path(path: str | Path) -> str:
    host_root = host_workspace_dir()
    raw = str(path)
    if not host_root:
        return raw
    try:
        resolved = Path(raw)
        relative = resolved.relative_to(WORKSPACE_ROOT)
    except ValueError:
        return raw
    return str(host_root / relative)


def container_path_from_display(path: str | Path) -> str:
    host_root = host_workspace_dir()
    raw = str(path).strip()
    if not host_root or not raw:
        return raw
    expanded = Path(raw).expanduser()
    try:
        relative = expanded.relative_to(host_root)
    except ValueError:
        return raw
    return str(WORKSPACE_ROOT / relative)


def default_research_lens() -> str:
    return lens_key(load_dashboard_settings().get("default_research_lens", DEFAULT_RESEARCH_LENS))


def dashboard_refresh_seconds() -> int:
    try:
        value = int(load_dashboard_settings().get("refresh_seconds", DASHBOARD_REFRESH_SECONDS))
    except (TypeError, ValueError):
        value = DASHBOARD_REFRESH_SECONDS
    return max(30, min(3600, value))


def load_dashboard_settings() -> dict:
    defaults = {
        "research_os_dir": str(ROOT),
        "workspace_dir": str(WORKSPACE_ROOT),
        "projects_dir": str(PROJECTS_DIR if PROJECTS_DIR.exists() or not LEGACY_PROJECTS_DIR.exists() else LEGACY_PROJECTS_DIR),
        "backup_dir": str(default_backup_dir()),
        "backup_enabled": False,
        "refresh_seconds": DASHBOARD_REFRESH_SECONDS,
        "default_research_lens": DEFAULT_RESEARCH_LENS,
    }
    if not SETTINGS_FILE.exists():
        return defaults
    try:
        data = json.loads(read_text(SETTINGS_FILE))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return defaults
    if not isinstance(data, dict):
        return defaults
    settings = {**defaults}
    for key in ("projects_dir", "backup_dir"):
        value = str(data.get(key, "")).strip()
        if value:
            settings[key] = value
    try:
        settings["refresh_seconds"] = max(30, min(3600, int(data.get("refresh_seconds", defaults["refresh_seconds"]))))
    except (TypeError, ValueError):
        settings["refresh_seconds"] = defaults["refresh_seconds"]
    settings["backup_enabled"] = data.get("backup_enabled") is True
    lens = lens_key(str(data.get("default_research_lens", defaults["default_research_lens"])))
    known_lenses = {item["key"] for item in available_research_lenses()}
    settings["default_research_lens"] = lens if lens in known_lenses else DEFAULT_RESEARCH_LENS
    return settings


def save_dashboard_settings(data: dict) -> dict:
    current = load_dashboard_settings()
    next_settings = dict(current)
    for key in ("projects_dir", "backup_dir"):
        value = str(data.get(key, "")).strip()
        if value:
            next_settings[key] = str(Path(container_path_from_display(value)).expanduser())
    if "refresh_seconds" in data:
        try:
            next_settings["refresh_seconds"] = max(30, min(3600, int(data.get("refresh_seconds"))))
        except (TypeError, ValueError):
            raise ValueError("Refresh interval must be a number of seconds.")
    if "backup_enabled" in data:
        next_settings["backup_enabled"] = data.get("backup_enabled") is True
    if "default_research_lens" in data:
        lens = lens_key(str(data.get("default_research_lens", "")))
        known_lenses = {item["key"] for item in available_research_lenses()}
        if lens not in known_lenses:
            raise ValueError(f"Unknown research lens: {data.get('default_research_lens')}")
        next_settings["default_research_lens"] = lens
    write_text(
        SETTINGS_FILE,
        json.dumps(
            {
                "projects_dir": next_settings["projects_dir"],
                "backup_dir": next_settings["backup_dir"],
                "backup_enabled": next_settings["backup_enabled"],
                "refresh_seconds": next_settings["refresh_seconds"],
                "default_research_lens": next_settings["default_research_lens"],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
    )
    return next_settings


def run_git(args: list[str], timeout: float = 4.0) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=timeout,
        check=True,
    )
    return result.stdout.strip()


def git_value(args: list[str], fallback: str = "", timeout: float = 4.0) -> str:
    try:
        return run_git(args, timeout=timeout).strip()
    except Exception:
        return fallback


def version_sort_key(tag: str) -> tuple[int, int, int, str]:
    match = re.match(r"^v?(\d+)\.(\d+)\.(\d+)(.*)$", tag.strip())
    if not match:
        return (0, 0, 0, tag)
    major, minor, patch, suffix = match.groups()
    return (int(major), int(minor), int(patch), suffix)


def latest_semver_tag(tags: Iterable[str]) -> str:
    clean = [tag for tag in tags if re.match(r"^v?\d+\.\d+\.\d+", tag)]
    if not clean:
        return ""
    return sorted(clean, key=version_sort_key)[-1]


def changelog_latest_version() -> str:
    changelog = ROOT / "CHANGELOG.md"
    if not changelog.exists():
        return ""
    match = re.search(r"^##\s+(v?\d+\.\d+\.\d+)\b", read_text(changelog), flags=re.MULTILINE)
    return match.group(1) if match else ""


def local_update_identity() -> dict:
    current_sha = git_value(["rev-parse", "HEAD"])
    changelog_version = changelog_latest_version()
    current_version = git_value(["describe", "--tags", "--always", "--dirty"], current_sha[:7] if current_sha else changelog_version or "unknown")
    branch = git_value(["branch", "--show-current"], "unknown")
    return {
        "current_sha": current_sha,
        "current_short_sha": current_sha[:7] if current_sha else "",
        "current_version": current_version,
        "current_release_version": changelog_version or current_version,
        "branch": branch,
    }


def load_update_cache() -> dict:
    if not UPDATE_STATUS_FILE.exists():
        return {}
    try:
        data = json.loads(read_text(UPDATE_STATUS_FILE))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def save_update_cache(data: dict) -> None:
    write_text(UPDATE_STATUS_FILE, json.dumps(data, indent=2, sort_keys=True) + "\n")


def update_cache_is_fresh(cache: dict) -> bool:
    checked_at = str(cache.get("checked_at", ""))
    if not checked_at:
        return False
    try:
        checked = datetime.fromisoformat(checked_at)
    except ValueError:
        return False
    interval = UPDATE_CHECK_INTERVAL if cache.get("status") == "ok" else timedelta(hours=1)
    return now() - checked < interval


def github_json(path: str) -> object:
    request = urllib.request.Request(
        f"{GITHUB_API_REPO_URL}{path}",
        headers={"User-Agent": "Research-OS-dashboard", "Accept": "application/vnd.github+json"},
    )
    with urllib.request.urlopen(request, timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def remote_update_info() -> dict:
    main = github_json("/commits/main")
    remote_main_sha = str(main.get("sha", "")) if isinstance(main, dict) else ""
    tag_payload = github_json("/tags?per_page=100")
    tags = [str(item.get("name", "")) for item in tag_payload if isinstance(item, dict)] if isinstance(tag_payload, list) else []
    latest_tag = latest_semver_tag(tags)
    return {
        "remote_main_sha": remote_main_sha,
        "remote_short_sha": remote_main_sha[:7] if remote_main_sha else "",
        "latest_tag": latest_tag,
    }


def update_status(force: bool = False) -> dict:
    local = local_update_identity()
    cache = load_update_cache()
    if force or not update_cache_is_fresh(cache):
        try:
            remote = remote_update_info()
            cache = {
                "status": "ok",
                "checked_at": now().isoformat(),
                **remote,
                "error": "",
            }
        except Exception as exc:
            cache = {
                **cache,
                "status": "error",
                "checked_at": now().isoformat(),
                "error": str(exc),
            }
        save_update_cache(cache)
    remote_sha = str(cache.get("remote_main_sha", ""))
    latest_tag = str(cache.get("latest_tag", ""))
    sha_update_available = bool(remote_sha and local.get("current_sha") and remote_sha != local.get("current_sha"))
    version_update_available = bool(latest_tag and version_sort_key(latest_tag) > version_sort_key(str(local.get("current_release_version", ""))))
    update_available = sha_update_available or version_update_available
    latest_version = latest_tag or (remote_sha[:7] if remote_sha else "")
    if update_available and latest_tag and remote_sha:
        latest_version = f"{latest_tag} ({remote_sha[:7]})"
    command_path = host_display_path(ROOT)
    update_command = f'cd "{command_path}"\ngit pull\nscripts/run-dashboard-docker.sh'
    return {
        **local,
        "status": cache.get("status", "unknown") if cache else "unknown",
        "checked_at": cache.get("checked_at", ""),
        "error": cache.get("error", ""),
        "remote_main_sha": remote_sha,
        "remote_short_sha": remote_sha[:7] if remote_sha else "",
        "latest_tag": latest_tag,
        "latest_version": latest_version or "unknown",
        "update_available": update_available,
        "check_interval_hours": round(UPDATE_CHECK_INTERVAL.total_seconds() / 3600),
        "release_notes_url": GITHUB_CHANGELOG_URL,
        "repo_url": GITHUB_REPO_URL,
        "update_command": update_command,
    }


def dashboard_settings_payload() -> dict:
    settings = load_dashboard_settings()
    return {
        **settings,
        "research_os_display_dir": host_display_path(settings["research_os_dir"]),
        "workspace_display_dir": host_display_path(settings["workspace_dir"]),
        "projects_display_dir": host_display_path(settings["projects_dir"]),
        "settings_display_file": host_display_path(SETTINGS_FILE),
        "settings_file": str(SETTINGS_FILE),
        "research_os_exists": Path(settings["research_os_dir"]).exists(),
        "projects_exists": Path(settings["projects_dir"]).exists(),
        "backup_exists": Path(settings["backup_dir"]).exists(),
        "research_lenses": available_research_lenses(),
        "update_status": update_status(),
    }


def projects_dir() -> Path:
    return Path(load_dashboard_settings()["projects_dir"]).expanduser()


def slug(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return cleaned or "source"


def title_from_slug(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("-", " ")).strip().title()


def normalize_date(value: str) -> str:
    match = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", value)
    if match:
        return value
    match = re.fullmatch(r"(\d{2})-(\d{2})-(\d{4})", value)
    if match:
        day, month, year = match.groups()
        return f"{year}-{month}-{day}"
    raise SystemExit("Date must be YYYY-MM-DD, for example 2026-07-23.")


def checksum(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def lens_key(value: str) -> str:
    return slug(value.replace("_", "-")).replace("-", "_") or DEFAULT_RESEARCH_LENS


def lens_file_key(path: Path) -> str:
    return lens_key(path.stem)


def lens_title(text: str, fallback: str) -> str:
    match = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
    if match:
        return match.group(1).strip()
    return title_from_slug(fallback.replace("_", "-"))


def available_research_lenses() -> list[dict]:
    lenses: list[dict] = []
    if LENSES_DIR.exists():
        for path in sorted(LENSES_DIR.glob("*.md")):
            try:
                text = read_text(path)
            except UnicodeDecodeError:
                continue
            key = lens_file_key(path)
            lenses.append(
                {
                    "key": key,
                    "label": lens_title(text, key),
                    "path": rel(path),
                    "is_default": key == DEFAULT_RESEARCH_LENS,
                }
            )
    if not any(item["key"] == DEFAULT_RESEARCH_LENS for item in lenses):
        lenses.insert(
            0,
            {
                "key": DEFAULT_RESEARCH_LENS,
                "label": "Neutral research lens",
                "path": rel(LENSES_DIR / "neutral.md"),
                "is_default": True,
            },
        )
    return lenses


def research_lens_file(key: str) -> Path | None:
    normalized = lens_key(key)
    if not LENSES_DIR.exists():
        return None
    for path in sorted(LENSES_DIR.glob("*.md")):
        if lens_file_key(path) == normalized:
            return path
    return None


def simple_yaml_value(text: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.+?)\s*$", text, flags=re.MULTILINE)
    if not match:
        return ""
    return match.group(1).strip().strip('"').strip("'")


def selected_research_lens(round_dir: Path) -> dict:
    pipeline = round_file(round_dir, "pipeline")
    key = DEFAULT_RESEARCH_LENS
    if pipeline.exists():
        key = lens_key(simple_yaml_value(read_text(pipeline), "research_lens") or DEFAULT_RESEARCH_LENS)
    available = available_research_lenses()
    known = {item["key"]: item for item in available}
    if key not in known:
        key = DEFAULT_RESEARCH_LENS
    info = dict(known.get(key, known[DEFAULT_RESEARCH_LENS]))
    info["is_special"] = key != DEFAULT_RESEARCH_LENS
    return info


def set_round_research_lens(round_dir: Path, key: str) -> dict:
    normalized = lens_key(key)
    known = {item["key"] for item in available_research_lenses()}
    if normalized not in known:
        raise ValueError(f"Unknown research lens: {key}")
    pipeline = round_file(round_dir, "pipeline")
    text = read_text(pipeline) if pipeline.exists() else ""
    if re.search(r"^research_lens:\s*.*$", text, flags=re.MULTILINE):
        text = re.sub(r"^research_lens:\s*.*$", f"research_lens: {normalized}", text, flags=re.MULTILINE)
    elif text:
        text = re.sub(r"^(status:\s*.+)$", rf"\1\nresearch_lens: {normalized}", text, count=1, flags=re.MULTILINE)
        if "research_lens:" not in text:
            text = f"research_lens: {normalized}\n{text}"
    else:
        text = f"research_lens: {normalized}\n"
    write_text(pipeline, text if text.endswith("\n") else text + "\n")
    return selected_research_lens(round_dir)


def round_monitoring_path(round_dir: Path) -> Path:
    return round_dir / ROUND_MONITORING_FILE


def load_round_monitoring(round_dir: Path) -> dict:
    path = round_monitoring_path(round_dir)
    defaults = {"monitored": True}
    if not path.exists():
        return defaults
    try:
        data = json.loads(read_text(path))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return defaults
    if not isinstance(data, dict):
        return defaults
    return {"monitored": data.get("monitored") is not False}


def round_is_monitored(round_dir: Path) -> bool:
    return bool(load_round_monitoring(round_dir).get("monitored", True))


def set_round_monitoring(round_dir: Path, monitored: bool) -> dict:
    payload = {"monitored": bool(monitored), "updated_at": now().isoformat()}
    write_json_if_changed(round_monitoring_path(round_dir), payload)
    return load_round_monitoring(round_dir)


def research_lens_prompt_block(round_dir: Path, include_content: bool = False) -> str:
    lens = selected_research_lens(round_dir)
    lines = [
        f"Selected research lens: {lens['label']} (`{lens['key']}`).",
        f"Lens file: `{lens['path']}`.",
        "Apply this lens as additional instructions on top of the common Research OS principles and stage-specific agent instructions.",
        "Do not let the lens override evidence traceability, uncertainty, contradictions or researcher review.",
        "Evidence extraction remains source-faithful; apply lens-specific interpretation mainly to Patterns, Insights, Recommendations and Deliverables.",
    ]
    if include_content:
        path = research_lens_file(lens["key"])
        if path and path.exists():
            lines.extend(["", read_text(path).strip()])
    return "\n".join(lines)


def load_env() -> dict[str, str]:
    env = dict(os.environ)
    env_path = ROOT / ".env"
    if env_path.exists():
        for raw_line in read_text(env_path).splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            env.setdefault(key.strip(), value.strip().strip('"').strip("'"))
    return env


def openai_model() -> str:
    return load_env().get("OPENAI_MODEL", "gpt-4.1-mini")


def openai_api_key() -> str | None:
    return load_env().get("OPENAI_API_KEY")


def ai_provider() -> str:
    return load_env().get("AI_PROVIDER", "local").strip().lower()


def round_path(round_dir: Path, logical_name: str) -> Path:
    for folder_name in ROUND_DIRS[logical_name]:
        candidate = round_dir / folder_name
        if candidate.exists():
            return candidate
    return round_dir / ROUND_DIRS[logical_name][0]


def project_path(project_dir: Path, logical_name: str) -> Path:
    for folder_name in PROJECT_DIRS[logical_name]:
        candidate = project_dir / folder_name
        if candidate.exists():
            return candidate
    return project_dir / PROJECT_DIRS[logical_name][0]


def round_file(round_dir: Path, logical_name: str) -> Path:
    for filename in ROUND_FILES[logical_name]:
        candidate = round_dir / filename
        if candidate.exists():
            return candidate
    return round_dir / ROUND_FILES[logical_name][0]


def project_file(project_dir: Path, logical_name: str) -> Path:
    for filename in PROJECT_FILES[logical_name]:
        candidate = project_dir / filename
        if candidate.exists():
            return candidate
    return project_dir / PROJECT_FILES[logical_name][0]


def load_state(round_dir: Path) -> dict:
    state_path = round_dir / STATE_FILE
    if not state_path.exists():
        return {"sources": {}, "runs": []}
    return json.loads(read_text(state_path))


def save_state(round_dir: Path, state: dict) -> None:
    write_text(round_dir / STATE_FILE, json.dumps(state, indent=2, sort_keys=True) + "\n")


def load_project_state(project_dir: Path) -> dict:
    state_path = project_dir / PROJECT_STATE_FILE
    if not state_path.exists():
        return {"sources": {}, "runs": []}
    return json.loads(read_text(state_path))


def save_project_state(project_dir: Path, state: dict) -> None:
    write_text(project_dir / PROJECT_STATE_FILE, json.dumps(state, indent=2, sort_keys=True) + "\n")


def assert_project(project_dir: Path) -> Path:
    resolved = resolve_research_path(project_dir)
    missing = []
    if not project_file(resolved, "overview").exists():
        missing.append(PROJECT_FILES["overview"][0])
    if not project_path(resolved, "rounds").exists():
        missing.append(PROJECT_DIRS["rounds"][0])
    if missing:
        raise SystemExit(f"Not a Research Program or missing files: {', '.join(missing)}")
    return resolved


def assert_round(round_dir: Path) -> Path:
    resolved = resolve_research_path(round_dir)
    required_files = ["overview", "questions", "pipeline"]
    missing = [ROUND_FILES[key][0] for key in required_files if not round_file(resolved, key).exists()]
    if not round_path(resolved, "sources").exists():
        missing.append(ROUND_DIRS["sources"][0])
    if missing:
        raise SystemExit(f"Not a Research Round or missing files: {', '.join(missing)}")
    return resolved


def source_files(round_dir: Path) -> list[Path]:
    ignored = {"README.md", ".DS_Store"}
    sources_dir = round_path(round_dir, "sources")
    return sorted(
        path
        for path in sources_dir.iterdir()
        if path.is_file() and path.name not in ignored
    )


def project_source_files(project_dir: Path) -> list[Path]:
    ignored = {"README.md", ".DS_Store"}
    sources_dir = project_path(project_dir, "sources")
    if not sources_dir.exists():
        return []
    return sorted(
        path
        for path in sources_dir.iterdir()
        if path.is_file() and path.name not in ignored
    )


def classify_source(path: Path) -> str:
    name = path.name.lower()
    try:
        text = read_text(path).lower()[:6000]
    except UnicodeDecodeError:
        text = ""
    if re.search(r"(?m)^\d{1,2}:\d{2}\s*$", text):
        return "interview-transcript"
    if "concept test" in name and path.suffix.lower() in {".txt", ".md"}:
        return "interview-transcript"
    setup_markers = [
        "research setup",
        "onderzoeksopzet",
        "onderzoeksdoel",
        "research goal",
        "research questions",
        "onderzoeksvragen",
        "methode",
        "method",
        "scope",
        "deelnemers",
        "participants",
    ]
    interview_markers = [
        "interview",
        "participant",
        "deelnemer",
        "moderator",
        "respondent",
        "transcript",
    ]
    if any(marker in name for marker in ["setup", "opzet", "context", "research-plan", "onderzoeksplan"]):
        return "research-setup"
    if sum(marker in text for marker in setup_markers) >= 2:
        return "research-setup"
    if any(marker in name for marker in ["interview", "transcript", "participant", "deelnemer"]):
        return "interview-transcript"
    if any(marker in text for marker in interview_markers):
        return "interview-transcript"
    return "source-material"


def classify_project_source(path: Path) -> str:
    name = path.name.lower()
    try:
        text = read_text(path).lower()[:6000]
    except UnicodeDecodeError:
        text = ""
    if any(marker in name for marker in ["stakeholder", "meeting", "workshop", "standup"]):
        return "stakeholder-context"
    if any(marker in name for marker in ["framework", "principles", "model", "canvas"]):
        return "framework-context"
    if any(marker in name for marker in ["research", "report", "insight", "findings"]):
        return "prior-research-context"
    if any(marker in name for marker in ["strategy", "roadmap", "vision", "okr", "brief"]):
        return "strategy-context"
    if any(marker in name for marker in ["product", "requirements", "spec", "documentation", "manual"]):
        return "product-context"
    if sum(marker in text for marker in ["stakeholder", "context", "constraint", "framework", "roadmap", "research"]) >= 2:
        return "project-context"
    return "project-context"


def changed_sources(round_dir: Path, force: bool) -> list[dict]:
    state = load_state(round_dir)
    sources = []
    for path in source_files(round_dir):
        digest = checksum(path)
        previous = state["sources"].get(path.name)
        if force or not previous or previous.get("checksum") != digest:
            sources.append(
                {
                    "id": f"SRC-{slug(path.stem)}",
                    "path": path,
                    "checksum": digest,
                    "size": path.stat().st_size,
                    "status": "changed" if previous else "new",
                    "type": classify_source(path),
                }
            )
    return sources


def changed_project_sources(project_dir: Path, force: bool) -> list[dict]:
    state = load_project_state(project_dir)
    sources = []
    for path in project_source_files(project_dir):
        digest = checksum(path)
        previous = state["sources"].get(path.name)
        if force or not previous or previous.get("checksum") != digest:
            sources.append(
                {
                    "id": f"PSRC-{slug(path.stem)}",
                    "path": path,
                    "checksum": digest,
                    "size": path.stat().st_size,
                    "status": "changed" if previous else "new",
                    "type": classify_project_source(path),
                }
            )
    return sources


def sources_by_type(sources: list[dict], source_type: str) -> list[dict]:
    return [source for source in sources if source.get("type") == source_type]


def placeholder_file(path: Path) -> bool:
    if not path.exists():
        return True
    text = read_text(path)
    placeholders = ["To be added.", "1. To be added.", "No accepted", "No Review Items are pending."]
    return any(placeholder in text for placeholder in placeholders)


def extract_json(text: str) -> dict:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped)
        stripped = re.sub(r"\s*```$", "", stripped)
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", stripped, flags=re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise


def load_context(round_dir: Path, files: Iterable[Path]) -> dict[str, str]:
    context = {}
    for path in files:
        if path.exists() and path.is_file():
            context[rel(path)] = read_text(path)
    return context


def run_agent(agent_name: str, instructions: str, context: dict[str, str], output_path: Path) -> None:
    """Disabled backend AI adapter.

    Research OS is currently operated through Codex/Cowork. Backend API calls
    and local stub generation are intentionally disabled so the dashboard never
    pretends that automated synthesis happened.
    """
    prompt = "\n\n".join(
        [
            "You are executing one Research OS agent. Follow the agent instructions exactly.",
            "Do not include hidden reasoning. Store only concise decisions, validation results, references and summaries.",
            "Context files:",
            *[f"\n--- {name} ---\n{content}" for name, content in sorted(context.items())],
        ]
    )
    output = call_ai(agent_name, instructions, prompt)
    write_text(output_path, output)


def call_ai(agent_name: str, instructions: str, prompt: str) -> str:
    raise RuntimeError(
        f"{agent_name} cannot run in the Research OS backend right now. "
        "Use Codex or Cowork from the dashboard prompt instead. "
        "Backend API calls and local stub generation are disabled."
    )


def context_sections(prompt: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    matches = list(re.finditer(r"\n--- (.*?) ---\n", prompt))
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(prompt)
        sections[match.group(1)] = prompt[start:end].strip()
    return sections


def first_section_value(text: str, labels: list[str]) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        clean = line.strip().strip("#").strip()
        for label in labels:
            if clean.lower().startswith(label.lower()):
                if ":" in clean:
                    value = clean.split(":", 1)[1].strip()
                    if value:
                        return value
                collected = []
                for next_line in lines[index + 1 :]:
                    stripped = next_line.strip()
                    if stripped.startswith("#") or re.match(r"^[A-Za-z ].*:$", stripped):
                        break
                    if stripped:
                        collected.append(stripped.strip("- "))
                    if len(collected) >= 3:
                        break
                if collected:
                    return " ".join(collected)
    return "To be added."


def extract_questions(text: str) -> list[str]:
    questions = []
    in_questions = False
    for line in text.splitlines():
        stripped = line.strip()
        lower = stripped.lower()
        if any(marker in lower for marker in ["onderzoeksvragen", "research questions"]):
            in_questions = True
            continue
        if in_questions and stripped.startswith("#"):
            break
        if in_questions:
            match = re.match(r"^(?:[-*]|\d+[.)])\s*(.+)", stripped)
            if match:
                question = match.group(1).strip()
                if question:
                    questions.append(question)
    return questions


def markdown_list(paths: Iterable[Path]) -> str:
    items = list(paths)
    if not items:
        return "- None"
    return "\n".join(f"- {rel(path)}" for path in items)


def write_stage_log(run_dir: Path, result: StageResult) -> None:
    content = f"""# {result.name}

- Status: {result.status}
- Started time: {result.started.isoformat()}
- Completed time: {result.completed.isoformat()}
- Researcher review required: {"Yes" if result.review_required else "No"}

## Input files
{markdown_list(result.input_files)}

## Output files
{markdown_list(result.output_files)}

## Warnings
{chr(10).join(f"- {warning}" for warning in result.warnings) if result.warnings else "- None"}

## Errors
{chr(10).join(f"- {error}" for error in result.errors) if result.errors else "- None"}
"""
    write_text(run_dir / f"{result.name}.md", content)


def append_section(path: Path, section: str) -> None:
    existing = read_text(path) if path.exists() else ""
    if existing and not existing.endswith("\n"):
        existing += "\n"
    write_text(path, existing + "\n" + section.lstrip())


def command_shortcut(path: Path, body: str) -> None:
    write_text(path, body)
    path.chmod(0o755)


def round_command_shortcuts(round_dir: Path, project_id: str) -> None:
    shortcuts_dir = SHORTCUTS_DIR / "Rounds" / project_id / round_dir.name
    round_rel = rel(round_dir)
    command_shortcut(
        shortcuts_dir / "01 Process New Input.command",
        f"""#!/bin/sh
set -e
cd "$(dirname "$0")/../../../.."
./research-os pipeline run {round_rel}
printf '\\nDone. You can close this window.\\n'
""",
    )
    command_shortcut(
        shortcuts_dir / "02 Make Deliverables.command",
        f"""#!/bin/sh
set -e
cd "$(dirname "$0")/../../../.."
printf 'Deliverable type [research-summary]: '
read -r DELIVERABLE_TYPE
if [ -z "$DELIVERABLE_TYPE" ]; then
  DELIVERABLE_TYPE="research-summary"
fi
./research-os deliverable request {round_rel} --type "$DELIVERABLE_TYPE"
./research-os deliverable generate {round_rel}
printf '\\nDone. You can close this window.\\n'
""",
    )
    write_text(
        shortcuts_dir / "README.md",
        f"# Round Shortcuts\n\nThese shortcuts are parked in Research OS while Codex/Cowork drives processing.\n\nOriginal round: `{round_rel}`\n\nUse the dashboard prompt after adding transcripts or other sources. The command shortcut only prints/logs a Codex handoff prompt; it does not process through a backend API.\n",
    )


def project_command_shortcuts(project_dir: Path) -> None:
    shortcuts_dir = SHORTCUTS_DIR / "Projects" / project_dir.name
    project_id = project_dir.name
    project_rel = rel(project_dir)
    command_shortcut(
        shortcuts_dir / "00 Process Project Input.command",
        f"""#!/bin/sh
set -e
cd "$(dirname "$0")/../.."
./research-os project process-input {project_rel}
printf '\\nDone. You can close this window.\\n'
""",
    )
    command_shortcut(
        shortcuts_dir / "01 Make New Round.command",
        f"""#!/bin/sh
set -e
cd "$(dirname "$0")/../.."
printf 'Round date, YYYY-MM-DD: '
read -r ROUND_DATE
printf 'Round name: '
read -r ROUND_NAME
if [ -z "$ROUND_DATE" ] || [ -z "$ROUND_NAME" ]; then
  printf 'Round date and name are required. Nothing created.\\n'
  exit 1
fi
./research-os round create --project {project_id} --date "$ROUND_DATE" --name "$ROUND_NAME"
printf '\\nDone. You can close this window.\\n'
""",
    )
    write_text(
        shortcuts_dir / "README.md",
        f"# Project Shortcuts\n\nThese shortcuts are parked in Research OS while Codex/Cowork drives processing.\n\nOriginal project: `{project_rel}`\n\nUse the dashboard prompt after adding project-level context sources. The command shortcut only prints/logs a Codex handoff prompt; it does not process through a backend API. Use `01 Make New Round.command` to make a new round inside this project.\n",
    )


def projects_command_shortcuts() -> None:
    shortcuts_dir = SHORTCUTS_DIR / "Projects Level"
    command_shortcut(
        shortcuts_dir / "01 Make New Project.command",
        """#!/bin/sh
set -e
cd "$(dirname "$0")/../.."
printf 'Project name: '
read -r PROJECT_NAME
if [ -z "$PROJECT_NAME" ]; then
  printf 'No project name entered. Nothing created.\n'
  exit 1
fi
./research-os project create --name "$PROJECT_NAME"
printf '\nDone. You can close this window.\n'
""",
    )
    write_text(shortcuts_dir / "README.md", "# Projects Shortcuts\n\nUse this shortcut to make a new project.\n")


def create_round_files(round_dir: Path, project_id: str, round_id: str, title: str, date: str, method: str) -> None:
    for logical_name in ROUND_DIRS:
        round_path(round_dir, logical_name).mkdir(parents=True, exist_ok=True)

    write_text(
        round_file(round_dir, "overview"),
        f"""# {title}

## Research Project
{title_from_slug(project_id)}

## Date
{date}

## Status
Planned

## Goal
To be added.

## Method
{method}

## Scope
To be added.

## Participants
To be added.

## Researcher Notes
To be added.
""",
    )
    write_text(round_file(round_dir, "questions"), "# Research Questions\n\n1. To be added.\n")
    write_text(
        round_file(round_dir, "pipeline"),
f"""project: {project_id}
round: {round_id}
status: planned
research_lens: {default_research_lens()}
sources:
  directory: 01-input-source-files
stages:
  source_intake:
    enabled: true
    automatic: true
  source_processing:
    enabled: true
    automatic: true
  evidence_extraction:
    enabled: true
    automatic: true
  method_assessment:
    enabled: true
    automatic: true
  pattern_detection:
    enabled: true
    automatic: true
  insight_synthesis:
    enabled: true
    automatic: true
  recommendation_synthesis:
    enabled: true
    automatic: true
  quality_critique:
    enabled: true
    automatic: true
  knowledge_curation:
    enabled: true
    automatic: false
    requires_review: true
  deliverable_generation:
    enabled: true
    automatic: false
    requires_explicit_request: true
deliverables:
  requested: []
""",
    )
    write_text(round_path(round_dir, "sources") / "README.md", "# Sources\n\nPlace original research material for this Research Round in this folder.\n")
    write_text(round_path(round_dir, "representations") / ".gitkeep", "")
    write_text(round_path(round_dir, "evidence") / ".gitkeep", "")
    write_text(round_path(round_dir, "method") / ".gitkeep", "")
    write_text(round_path(round_dir, "patterns") / "patterns.md", "# Patterns\n\nNo accepted or proposed Patterns have been recorded yet.\n")
    write_text(round_path(round_dir, "insights") / "insights.md", "# Insights\n\nNo accepted or proposed Insights have been recorded yet.\n")
    write_text(round_path(round_dir, "recommendations") / "recommendations.md", "# Recommendations\n\nNo accepted or proposed Recommendations have been recorded yet.\n")
    write_text(
        round_path(round_dir, "reviews") / "review-queue.md",
        """# Review Queue

No Review Items are pending.

## Review Item
- ID:
- Type:
- Status: Pending
- Proposed by:
- Triggered by:
- Affected knowledge:
- Proposed change:
- Helps us understand:
- Supporting Evidence:
- Contradicting Evidence:
- Available decisions:
  - Approve
  - Reject
  - Revise

## Researcher Decision
- Decision:
- Researcher:
- Date:
- Notes:
""",
    )
    write_text(round_path(round_dir, "deliverables") / "README.md", "# Deliverables\n\nDeliverables are not generated automatically. Request them explicitly.\n")
    write_text(round_path(round_dir, "pipeline_runs") / ".gitkeep", "")
    write_text(
        round_path(round_dir, "work_files") / "README.md",
        "# AI Work Files\n\nThis folder contains AI and pipeline work files for this Research Round, including source representations, evidence, patterns, insights, recommendations, review queues, method assessments, settings and run logs. Researchers normally add input in `01-input-source-files/` and collect final output in `02-output-deliverables/`.\n",
    )
    set_round_monitoring(round_dir, True)
    round_command_shortcuts(round_dir, project_id)


def create_project_files(project_dir: Path, project_name: str, force: bool = False) -> None:
    if project_dir.exists() and not force:
        raise SystemExit(f"Project already exists: {rel(project_dir)}. Use --force to fill missing files.")

    project_dir.mkdir(parents=True, exist_ok=True)
    for logical_name in PROJECT_DIRS:
        project_path(project_dir, logical_name).mkdir(parents=True, exist_ok=True)

    files = {
        project_file(project_dir, "overview"): f"""# {project_name}

## Purpose
To be added.

## Status
Active

## Current Focus
To be added.
""",
        project_file(project_dir, "context"): f"""# Project Context

## Purpose
Durable context for {project_name} that can inform multiple Research Rounds.

## Context Statements
No accepted Project Context has been recorded yet.

## Assumptions
No enduring assumptions have been recorded yet.

## Open Questions
No enduring open questions have been recorded yet.

## Source References
No project-level Sources have been accepted into Project Context yet.
""",
        project_file(project_dir, "understanding"): "# Current Understanding\n\nNo accepted Current Understanding has been recorded yet.\n",
        project_file(project_dir, "opportunities"): "# Opportunities\n\nNo Opportunities have been recorded yet.\n",
        project_file(project_dir, "decisions"): "# Decisions\n\nNo Decisions have been recorded yet.\n",
        project_path(project_dir, "work_files") / "COMMANDS.md": f"""# {project_name} Commands

From the Research OS folder:

```sh
cd "{ROOT}"
```

## Make A New Round

```sh
./research-os round create --project {project_dir.name} --date 2026-07-29 --name "Concept Test 01"
```

## Process Project-Level Input

Place durable context material in `01-input-source-files/`, then use the Research OS dashboard prompt to process it in Codex/Cowork.

## Parked Shortcuts

Clickable `.command` shortcuts are stored under `Research OS/Command Shortcuts/Projects/{project_dir.name}/` as Codex handoff helpers. Backend API processing is disabled.
""",
    }
    for path, content in files.items():
        if force or not path.exists():
            write_text(path, content)
    project_readmes = {
        project_path(project_dir, "sources") / "README.md": "# Project Context Sources\n\nPlace project-level input here when it should inform Project Context across rounds. Examples: stakeholder interviews, meeting recordings, slide decks, frameworks, research documents, product documentation and strategy material.\n\nThese Sources are contextual by default. They do not automatically become Round Evidence.\n",
        project_path(project_dir, "representations") / ".gitkeep": "",
        project_path(project_dir, "reviews") / "project-context-proposals.md": "# Project Context Proposals\n\nNo Project Context proposals are pending.\n",
        project_path(project_dir, "pipeline_runs") / ".gitkeep": "",
        project_path(project_dir, "work_files") / "README.md": "# AI Work Files\n\nThis folder contains AI and pipeline work files for the project, including project context, current understanding, opportunities, decisions, review proposals, source representations and run logs. Researchers normally add input in `01-input-source-files/` and keep research rounds in `02-rounds/`.\n",
    }
    for path, content in project_readmes.items():
        if force or not path.exists():
            write_text(path, content)
    project_command_shortcuts(project_dir)
    projects_command_shortcuts()


def ensure_project_input_scaffold(project_dir: Path) -> None:
    for logical_name in PROJECT_DIRS:
        project_path(project_dir, logical_name).mkdir(parents=True, exist_ok=True)
    if not (project_file(project_dir, "context")).exists():
        project_name = title_from_slug(project_dir.name)
        write_text(
            project_file(project_dir, "context"),
            f"""# Project Context

## Purpose
Durable context for {project_name} that can inform multiple Research Rounds.

## Context Statements
No accepted Project Context has been recorded yet.

## Assumptions
No enduring assumptions have been recorded yet.

## Open Questions
No enduring open questions have been recorded yet.

## Source References
No project-level Sources have been accepted into Project Context yet.
""",
        )
    readme = project_path(project_dir, "sources") / "README.md"
    if not readme.exists():
        write_text(readme, "# Project Context Sources\n\nPlace project-level input here when it should inform Project Context across rounds. These Sources are contextual by default and do not automatically become Round Evidence.\n")
    proposals = project_path(project_dir, "reviews") / "project-context-proposals.md"
    if not proposals.exists():
        write_text(proposals, "# Project Context Proposals\n\nNo Project Context proposals are pending.\n")
    gitkeep_targets = [
        project_path(project_dir, "representations") / ".gitkeep",
        project_path(project_dir, "pipeline_runs") / ".gitkeep",
    ]
    for path in gitkeep_targets:
        if not path.exists():
            write_text(path, "")
    work_readme = project_path(project_dir, "work_files") / "README.md"
    if not work_readme.exists():
        write_text(work_readme, "# Work Files\n\nThis folder contains AI and pipeline work files for the project. Researchers normally do not edit these files directly.\n")
    project_command_shortcuts(project_dir)


def write_project_source_metadata(project_dir: Path, sources: list[dict]) -> list[Path]:
    outputs = []
    representations_dir = project_path(project_dir, "representations")
    for source in sources:
        output = representations_dir / f"{source['id']}-metadata.md"
        content = f"""# Project Source Metadata

## Source
- Source ID: {source['id']}
- Scope: Research Program
- Original file: {rel(source['path'])}
- Checksum: {source['checksum']}
- Size bytes: {source['size']}
- Intake status: {source['status']}
- Source type: {source.get('type', 'project-context')}
- Evidentiary role: Context by default
- Processing plan: Create a normalized representation and propose Project Context updates for researcher review.
- Review required: Yes
"""
        write_text(output, content)
        outputs.append(output)
    return outputs


def write_project_representations(project_dir: Path, sources: list[dict]) -> list[Path]:
    outputs = []
    representations_dir = project_path(project_dir, "representations")
    for source in sources:
        output = representations_dir / f"{source['id']}-representation.md"
        try:
            body = read_text(source["path"])
            warning = ""
        except UnicodeDecodeError:
            body = ""
            warning = "Source is not UTF-8 text-readable. Add a transcript, notes or normalized representation manually before using it for Project Context."
        content = f"""# Project Source Representation

- Source ID: {source['id']}
- Source file: {rel(source['path'])}
- Scope: Research Program
- Representation type: {"normalized-text" if body else "manual-required"}
- Created by: Source Processing Agent MVP adapter

## Segments
### Segment
- Segment ID: {source['id']}-SEG-001
- Source reference: {rel(source['path'])}
- Content:

```text
{body.strip() if body else warning}
```

## Context Use Rules
- May inform Project Context after researcher review.
- Must not be cited as Round Evidence unless linked to underlying Evidence from its original study.
"""
        write_text(output, content)
        outputs.append(output)
    return outputs


def project_context_summary(source: dict) -> list[str]:
    try:
        text = read_text(source["path"])
    except UnicodeDecodeError:
        return ["Manual representation required before context can be proposed."]
    lines = []
    for raw_line in text.splitlines():
        line = raw_line.strip().strip("-* ")
        if not line or line.startswith("#"):
            continue
        if len(line) < 18:
            continue
        lines.append(line)
        if len(lines) >= 5:
            break
    return lines or ["Review this Source for durable context, assumptions, terminology or constraints."]


def append_program_context_proposals(project_dir: Path, run_id: str, sources: list[dict]) -> Path:
    output = project_path(project_dir, "reviews") / "project-context-proposals.md"
    sections = [f"\n<!-- Generated by {run_id} -->"]
    for source in sources:
        proposal_id = f"PCI-{source['id'].replace('PSRC-', '')}"
        summaries = project_context_summary(source)
        sections.extend(
            [
                "",
                "## Project Context Proposal",
                f"- ID: {proposal_id}",
                "- Status: Pending",
                "- Proposed by: Project Source Processing MVP adapter",
                f"- Triggered by: {source['id']}",
                f"- Source type: {source.get('type', 'project-context')}",
                "- Affected knowledge: Project Context",
                f"- Proposed change: Should Research OS use `{source['path'].name}` as reusable project context for future research rounds?",
                "- Evidentiary role: Context by default; not Round Evidence",
                f"- Source reference: {rel(source['path'])}",
                "- Candidate context statements:",
                *[f"  - {line}" for line in summaries],
                "- Available decisions:",
                "  - Approve",
                "  - Reject",
                "  - Revise",
                "",
                "## Researcher Decision",
                "- Decision:",
                "- Researcher:",
                "- Date:",
                "- Notes:",
            ]
        )
    append_section(output, "\n".join(sections) + "\n")
    return output


def write_source_metadata(round_dir: Path, sources: list[dict]) -> list[Path]:
    outputs = []
    representations_dir = round_path(round_dir, "representations")
    for source in sources:
        output = representations_dir / f"{source['id']}-metadata.md"
        content = f"""# Source Metadata

## Source
- Source ID: {source['id']}
- Original file: {rel(source['path'])}
- Checksum: {source['checksum']}
- Size bytes: {source['size']}
- Intake status: {source['status']}
- Source type: {source.get('type', 'source-material')}
- Processing plan: Create a normalized text representation if the Source is text-readable; otherwise mark for manual representation.
- Review required: No
"""
        write_text(output, content)
        outputs.append(output)
    return outputs


def write_representations(round_dir: Path, sources: list[dict]) -> list[Path]:
    outputs = []
    representations_dir = round_path(round_dir, "representations")
    for source in sources:
        output = representations_dir / f"{source['id']}-representation.md"
        try:
            body = read_text(source["path"])
            warning = ""
        except UnicodeDecodeError:
            body = ""
            warning = "Source is not UTF-8 text-readable. Add a transcript or normalized representation manually."
        content = f"""# Source Representation

- Source ID: {source['id']}
- Source file: {rel(source['path'])}
- Representation type: {"normalized-text" if body else "manual-required"}
- Created by: Source Processing Agent MVP adapter

## Segments
### Segment
- Segment ID: {source['id']}-SEG-001
- Source reference: {rel(source['path'])}
- Content:

```text
{body.strip() if body else warning}
```
"""
        write_text(output, content)
        outputs.append(output)
    return outputs


def process_round_setup(round_dir: Path, setup_sources: list[dict], run_dir: Path) -> list[Path]:
    if not setup_sources:
        return []
    context = {
        rel(round_file(round_dir, "overview")): read_text(round_file(round_dir, "overview")),
        rel(round_file(round_dir, "questions")): read_text(round_file(round_dir, "questions")),
    }
    for source in setup_sources:
        try:
            context[rel(source["path"])] = read_text(source["path"])
        except UnicodeDecodeError:
            context[rel(source["path"])] = "[Binary or non-text setup source. Add a text setup file to auto-fill round context.]"

    instructions = read_text(AGENTS_DIR / "round-setup-agent.md")
    prompt = "\n\n".join(
        [
            "Extract the Research Round setup from the source material.",
            "Return only JSON with keys: round_md, research_questions_md, summary, uncertainties.",
            "Do not invent findings. Do not create Evidence.",
            *[f"\n--- {name} ---\n{content}" for name, content in sorted(context.items())],
        ]
    )
    raw_output = call_ai("Round Setup Agent", instructions, prompt)
    write_text(run_dir / "round-setup-agent-output.md", raw_output)

    outputs = [run_dir / "round-setup-agent-output.md"]
    try:
        data = extract_json(raw_output)
    except json.JSONDecodeError:
        proposal_path = round_path(round_dir, "reviews") / "round-setup-proposal.md"
        write_text(proposal_path, "# Round Setup Proposal\n\nThe agent returned non-JSON output. Review manually.\n\n" + raw_output)
        outputs.append(proposal_path)
        return outputs

    overview_file = round_file(round_dir, "overview")
    questions_file = round_file(round_dir, "questions")
    can_apply = placeholder_file(overview_file) and placeholder_file(questions_file)
    if can_apply:
        write_text(overview_file, data.get("round_md", read_text(overview_file)).strip() + "\n")
        write_text(questions_file, data.get("research_questions_md", read_text(questions_file)).strip() + "\n")
        outputs.extend([overview_file, questions_file])
    else:
        proposal_path = round_path(round_dir, "reviews") / "round-setup-proposal.md"
        content = f"""# Round Setup Proposal

Status: Pending

## Summary
{data.get("summary", "No summary provided.")}

## Proposed round.md
{data.get("round_md", "").strip()}

## Proposed research-questions.md
{data.get("research_questions_md", "").strip()}

## Uncertainties
{chr(10).join(f"- {item}" for item in data.get("uncertainties", [])) if data.get("uncertainties") else "- None"}
"""
        write_text(proposal_path, content)
        outputs.append(proposal_path)
    return outputs


def write_empty_evidence(round_dir: Path, sources: list[dict]) -> Path:
    output = round_path(round_dir, "evidence") / "evidence.md"
    sections = [
        "# Evidence",
        "",
        "No Evidence has been accepted yet.",
        "",
        "The MVP adapter does not infer Evidence without an AI provider. Source Representations created in this run are ready for extraction.",
    ]
    if sources:
        sections.extend(["", "## Sources Awaiting Evidence Extraction"])
        sections.extend(f"- {source['id']}: {rel(source['path'])}" for source in sources)
    write_text(output, "\n".join(sections) + "\n")
    return output


def write_evidence(round_dir: Path, sources: list[dict], run_dir: Path) -> Path:
    output = round_path(round_dir, "evidence") / "evidence.md"
    transcript_sources = sources_by_type(sources, "interview-transcript")
    if not transcript_sources:
        return write_empty_evidence(round_dir, sources)

    representation_paths = [
        round_path(round_dir, "representations") / f"{source['id']}-representation.md"
        for source in transcript_sources
    ]
    context = load_context(round_dir, [round_file(round_dir, "questions"), *representation_paths])
    instructions = read_text(AGENTS_DIR / "evidence-extractor-agent.md")
    prompt = "\n\n".join(
        [
            "Extract proposed atomic Evidence from interview transcript representations.",
            "Preserve research richness: do not collapse a whole interview into one observation per screen or research question.",
            "Capture separate reactions, confusions, expectations, suggestions, workflow comparisons and changes in understanding as separate Evidence items.",
            "For a rich 45-minute interview, prefer high-recall extraction with many concrete Evidence items when the transcript supports it.",
            "Write Markdown only. Do not explain why behavior occurred.",
            "Every Evidence item must include Evidence ID, Source, source reference, observation, quote, related research question, uncertainty and salience.",
            *[f"\n--- {name} ---\n{content}" for name, content in sorted(context.items())],
        ]
    )
    content = call_ai("Evidence Extractor Agent", instructions, prompt)
    write_text(run_dir / "evidence-extraction-agent-output.md", content)
    write_text(output, content)
    return output


def evidence_available(round_dir: Path) -> bool:
    evidence_path = round_path(round_dir, "evidence") / "evidence.md"
    if not evidence_path.exists():
        return False
    text = read_text(evidence_path)
    return "Evidence ID" in text or "Observation:" in text


def write_method_assessment(round_dir: Path, run_dir: Path) -> Path:
    output = round_path(round_dir, "method") / "method-assessments.md"
    if not evidence_available(round_dir):
        write_text(output, "# Method Assessments\n\nNo Method Assessments were generated because no Evidence exists yet.\n")
        return output
    context = load_context(round_dir, [round_file(round_dir, "overview"), round_path(round_dir, "evidence") / "evidence.md"])
    instructions = read_text(AGENTS_DIR / "method-specialist-agent.md")
    prompt = "\n\n".join(
        [
            "Assess method, prototype, sample and moderation limitations that affect interpretation.",
            "Do not reject Evidence solely because limitations exist.",
            *[f"\n--- {name} ---\n{content}" for name, content in sorted(context.items())],
        ]
    )
    content = call_ai("Method Specialist Agent", instructions, prompt)
    write_text(run_dir / "method-assessment-agent-output.md", content)
    write_text(output, content)
    return output


def write_patterns(round_dir: Path, run_dir: Path) -> Path:
    output = round_path(round_dir, "patterns") / "patterns.md"
    if not evidence_available(round_dir):
        write_text(output, "# Patterns\n\nNo Patterns were generated because no Evidence exists yet.\n")
        return output
    context = load_context(round_dir, [round_path(round_dir, "evidence") / "evidence.md", output])
    instructions = read_text(AGENTS_DIR / "pattern-detector-agent.md")
    prompt = "\n\n".join(
        [
            "Detect proposed Patterns from the Evidence. Group observations without explaining causes.",
            "Include supporting and contradicting Evidence IDs.",
            research_lens_prompt_block(round_dir, include_content=True),
            *[f"\n--- {name} ---\n{content}" for name, content in sorted(context.items())],
        ]
    )
    content = call_ai("Pattern Detector Agent", instructions, prompt)
    write_text(run_dir / "pattern-detection-agent-output.md", content)
    write_text(output, content)
    return output


def write_insights(round_dir: Path, run_dir: Path) -> Path:
    output = round_path(round_dir, "insights") / "insights.md"
    if not evidence_available(round_dir):
        write_text(output, "# Insights\n\nNo Insights were generated because no Evidence exists yet.\n")
        return output
    project_dir = round_dir.parents[1]
    context = load_context(
        round_dir,
        [
            round_file(round_dir, "questions"),
            project_file(project_dir, "context"),
            project_file(project_dir, "understanding"),
            round_path(round_dir, "evidence") / "evidence.md",
            round_path(round_dir, "method") / "method-assessments.md",
            round_path(round_dir, "patterns") / "patterns.md",
            output,
        ],
    )
    instructions = read_text(AGENTS_DIR / "insight-synthesizer-agent.md")
    prompt = "\n\n".join(
        [
            "Synthesize proposed Insights from Patterns, Evidence and Method Assessments.",
            "Do not prescribe solutions. Preserve confidence, assumptions, contradictions and open questions.",
            research_lens_prompt_block(round_dir, include_content=True),
            *[f"\n--- {name} ---\n{content}" for name, content in sorted(context.items())],
        ]
    )
    content = call_ai("Insight Synthesizer Agent", instructions, prompt)
    write_text(run_dir / "insight-synthesis-agent-output.md", content)
    write_text(output, content)
    return output


def write_recommendations(round_dir: Path, run_dir: Path) -> Path:
    output = round_path(round_dir, "recommendations") / "recommendations.md"
    if not evidence_available(round_dir):
        write_text(output, "# Recommendations\n\nNo Recommendations were generated because no Evidence exists yet.\n")
        return output
    project_dir = round_dir.parents[1]
    context = load_context(
        round_dir,
        [
            round_file(round_dir, "questions"),
            project_file(project_dir, "context"),
            round_path(round_dir, "evidence") / "evidence.md",
            round_path(round_dir, "patterns") / "patterns.md",
            round_path(round_dir, "insights") / "insights.md",
            output,
        ],
    )
    instructions = read_text(AGENTS_DIR / "recommendation-synthesizer-agent.md")
    prompt = "\n\n".join(
        [
            "Create or update proposed Recommendations from Evidence, Patterns and Insights.",
            "Use the two-step structure: What we learned, then What we should do.",
            "Keep every Recommendation independently understandable, concrete, traceable and reviewable.",
            "Do not create stakeholder-facing deliverables.",
            research_lens_prompt_block(round_dir, include_content=True),
            *[f"\n--- {name} ---\n{content}" for name, content in sorted(context.items())],
        ]
    )
    content = call_ai("Recommendation Synthesizer Agent", instructions, prompt)
    write_text(run_dir / "recommendation-synthesis-agent-output.md", content)
    write_text(output, content)
    return output


def write_quality_critique(round_dir: Path, run_dir: Path) -> Path:
    output = run_dir / "quality-critique-proposals.md"
    if not evidence_available(round_dir):
        write_text(output, "# Quality Critique\n\nNo critique was generated because no Evidence exists yet.\n")
        return output
    context = load_context(
        round_dir,
        [
            round_path(round_dir, "insights") / "insights.md",
            round_path(round_dir, "recommendations") / "recommendations.md",
            round_path(round_dir, "evidence") / "evidence.md",
            round_path(round_dir, "method") / "method-assessments.md",
        ],
    )
    instructions = read_text(AGENTS_DIR / "quality-critic-agent.md")
    prompt = "\n\n".join(
        [
            "Critique proposed Insights for unsupported claims, scope problems, weak traceability and missing contradictions.",
            "Do not silently edit accepted knowledge.",
            research_lens_prompt_block(round_dir, include_content=True),
            *[f"\n--- {name} ---\n{content}" for name, content in sorted(context.items())],
        ]
    )
    content = call_ai("Quality Critic Agent", instructions, prompt)
    write_text(output, content)
    return output


def write_review_queue(round_dir: Path, run_id: str, run_dir: Path) -> Path:
    output = round_path(round_dir, "reviews") / "review-queue.md"
    if not evidence_available(round_dir):
        append_section(output, f"\n<!-- Generated by {run_id} -->\n\nNo knowledge Review Items were generated because no Evidence exists yet.\n")
        return output
    context = load_context(
        round_dir,
        [
            round_path(round_dir, "insights") / "insights.md",
            round_path(round_dir, "recommendations") / "recommendations.md",
            run_dir / "quality-critique-proposals.md",
            output,
        ],
    )
    instructions = read_text(AGENTS_DIR / "knowledge-curator-agent.md")
    prompt = "\n\n".join(
        [
            "Create human-facing Review Items for proposed knowledge changes.",
            "Every Review Item must include ID, Type, Status: Pending, Proposed by, Triggered by, Affected knowledge, Proposed change, Helps us understand, Supporting Evidence, Contradicting Evidence and Available decisions.",
            "Create review items for important proposed Recommendations too. Recommendation review proposals should include `What we learned` and `What we should do` in the Proposed change field.",
            "Write `Helps us understand` as one plain-language sentence that completes this UI prompt: 'What this helps us understand'. Do not write a vague justification for why review is needed.",
            "Do not update Current Understanding directly.",
            research_lens_prompt_block(round_dir, include_content=True),
            *[f"\n--- {name} ---\n{content}" for name, content in sorted(context.items())],
        ]
    )
    content = call_ai("Knowledge Curator Agent", instructions, prompt)
    append_section(output, f"\n<!-- Generated by {run_id} -->\n\n{content}")
    return output


def append_review_stub(round_dir: Path, run_id: str, source_count: int) -> Path:
    path = round_path(round_dir, "reviews") / "review-queue.md"
    if source_count == 0:
        return path
    item_id = f"RI-{run_id}"
    section = f"""## Review Item
- ID: {item_id}
- Type: Pipeline Processing
- Status: Pending
- Proposed by: Knowledge Curator Agent MVP adapter
- Triggered by: {source_count} new or changed Source file(s)
- Affected knowledge: None
- Proposed change: Review generated Source metadata and representations before connecting an AI provider for Evidence extraction.
- Helps us understand: This helps us understand that Research OS prepared traceable inputs, but no evidence or findings have been inferred yet.
- Supporting Evidence: None
- Contradicting Evidence: None
- Available decisions:
  - Approve
  - Reject
  - Revise

## Researcher Decision
- Decision:
- Researcher:
- Date:
- Notes:
"""
    append_section(path, section)
    return path


def stage_inputs(round_dir: Path, key: str, sources: list[dict]) -> list[Path]:
    source_paths = [source["path"] for source in sources]
    representations_dir = round_path(round_dir, "representations")
    evidence_dir = round_path(round_dir, "evidence")
    patterns_dir = round_path(round_dir, "patterns")
    insights_dir = round_path(round_dir, "insights")
    recommendations_dir = round_path(round_dir, "recommendations")
    reviews_dir = round_path(round_dir, "reviews")
    if key == "source_intake":
        return [round_file(round_dir, "overview"), round_file(round_dir, "questions"), *source_paths]
    if key == "source_processing":
        return [*source_paths, *sorted(representations_dir.glob("*-metadata.md"))]
    if key == "evidence_extraction":
        return [round_file(round_dir, "questions"), *sorted(representations_dir.glob("*-representation.md"))]
    if key == "method_assessment":
        return [round_file(round_dir, "overview"), evidence_dir / "evidence.md"]
    if key == "pattern_detection":
        return [evidence_dir / "evidence.md", patterns_dir / "patterns.md"]
    if key == "insight_synthesis":
        return [patterns_dir / "patterns.md", insights_dir / "insights.md"]
    if key == "recommendation_synthesis":
        return [evidence_dir / "evidence.md", patterns_dir / "patterns.md", insights_dir / "insights.md", recommendations_dir / "recommendations.md"]
    if key == "quality_critique":
        return [insights_dir / "insights.md", recommendations_dir / "recommendations.md"]
    if key == "knowledge_curation":
        return [insights_dir / "insights.md", recommendations_dir / "recommendations.md", reviews_dir / "review-queue.md"]
    return []


def execute_stage(round_dir: Path, run_dir: Path, run_id: str, stage: tuple, sources: list[dict]) -> StageResult:
    key, log_name, agent_name, instruction_file = stage
    started = now()
    warnings = []
    errors = []
    outputs: list[Path] = []
    inputs = [path for path in stage_inputs(round_dir, key, sources) if path.exists()]

    try:
        if key == "source_intake":
            outputs = write_source_metadata(round_dir, sources)
            outputs.extend(process_round_setup(round_dir, sources_by_type(sources, "research-setup"), run_dir))
        elif key == "source_processing":
            outputs = write_representations(round_dir, sources)
        elif key == "evidence_extraction":
            outputs = [write_evidence(round_dir, sources, run_dir)]
        elif key == "method_assessment":
            outputs = [write_method_assessment(round_dir, run_dir)]
        elif key == "pattern_detection":
            outputs = [write_patterns(round_dir, run_dir)]
        elif key == "insight_synthesis":
            outputs = [write_insights(round_dir, run_dir)]
        elif key == "recommendation_synthesis":
            outputs = [write_recommendations(round_dir, run_dir)]
        elif key == "quality_critique":
            outputs = [write_quality_critique(round_dir, run_dir)]
        elif key == "knowledge_curation":
            outputs = [write_review_queue(round_dir, run_id, run_dir)]
        if not outputs:
            warnings.append("Stage produced no domain output files.")
        status = "success"
    except Exception as exc:
        errors.append(str(exc))
        status = "failed"

    result = StageResult(
        key=key,
        name=log_name,
        status=status,
        input_files=inputs,
        output_files=outputs,
        started=started,
        completed=now(),
        warnings=warnings,
        errors=errors,
        review_required=key == "knowledge_curation" and bool(sources),
    )
    write_stage_log(run_dir, result)
    return result


def pipeline_run(args: argparse.Namespace) -> None:
    round_dir = assert_round(Path(args.round_dir))
    sources = changed_sources(round_dir, args.force)
    run_id = "run-" + datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = round_path(round_dir, "pipeline_runs") / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    results = []
    if not sources:
        warning = "No new or changed Sources detected. Use --force to reprocess unchanged Sources."
        write_text(run_dir / "run.md", f"# Pipeline Run {run_id}\n\n- Status: no-op\n- Warning: {warning}\n")
        print(warning)
        return

    state = load_state(round_dir)
    status = "codex-required"
    state["runs"].append({"id": run_id, "created_at": now().isoformat(), "status": status})
    save_state(round_dir, state)

    prompt = round_codex_processing_prompt(round_dir, sources)
    summary = [
        f"# Pipeline Run {run_id}",
        "",
        f"- Status: {status}",
        "- Mode: Codex/Cowork handoff",
        f"- Sources waiting for Codex processing: {len(sources)}",
        f"- Started: {now().isoformat()}",
        f"- Completed: {now().isoformat()}",
        "",
        "## Sources",
        *[f"- {source['id']}: {rel(source['path'])}" for source in sources],
        "",
        "## Codex Prompt",
        "```text",
        prompt.strip(),
        "```",
    ]
    write_text(run_dir / "run.md", "\n".join(summary) + "\n")
    print("Backend pipeline execution is disabled. Use this Codex/Cowork prompt instead:")
    print()
    print(prompt.strip())
    print()
    print(f"Handoff logged: {rel(run_dir)}")


def pipeline_status(args: argparse.Namespace) -> None:
    round_dir = assert_round(Path(args.round_dir))
    state = load_state(round_dir)
    pending = changed_sources(round_dir, False)
    print(f"Round: {rel(round_dir)}")
    print(f"Processed sources: {len(state.get('sources', {}))}")
    print(f"New or changed sources: {len(pending)}")
    if state.get("runs"):
        latest = state["runs"][-1]
        print(f"Latest run: {latest['id']} ({latest['status']})")
    else:
        print("Latest run: none")


def pipeline_review(args: argparse.Namespace) -> None:
    round_dir = assert_round(Path(args.round_dir))
    queue = round_path(round_dir, "reviews") / "review-queue.md"
    pending = pending_markdown_items(queue)
    print(f"Review queue: {rel(queue)}")
    print(f"Pending items: {pending}")


def apply_reviews(args: argparse.Namespace) -> None:
    round_dir = assert_round(Path(args.round_dir))
    reviews_path = round_path(round_dir, "reviews") / "review-queue.md"
    queue = read_text(reviews_path)
    approved = re.findall(r"- Decision:\s*Approve\b", queue, flags=re.IGNORECASE)
    if not approved:
        print("No approved Change Proposals found. Current Understanding was not changed.")
        return
    target = project_file(round_dir.parents[1], "understanding")
    append_section(
        target,
        f"""## Approved Review Application
- Applied at: {now().isoformat()}
- Source: {rel(reviews_path)}
- Note: MVP recorded approval presence only. Connect the Knowledge Curator adapter before applying substantive knowledge changes.
""",
    )
    print(f"Applied approval marker to {rel(target)}")


DASHBOARD_REFRESH_SECONDS = 900
DASHBOARD_CACHE_SECONDS = 20
IGNORED_DASHBOARD_FILES = {"README.md", ".DS_Store", ".gitkeep", "status.json"}
DASHBOARD_PAYLOAD_CACHE: dict[str, object] = {"payload": None, "created_at": 0.0}


def parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value).replace(tzinfo=None)
    except ValueError:
        return None


def status_rank(status: str) -> int:
    return {"gray": 0, "green": 1, "blue": 2, "yellow": 3, "red": 4}.get(status, 0)


def worst_status(statuses: Iterable[str]) -> str:
    items = list(statuses)
    if not items:
        return "gray"
    return max(items, key=status_rank)


def source_inventory(source_dir: Path) -> list[dict]:
    if not source_dir.exists():
        return []
    items = []
    for path in sorted(source_dir.rglob("*")):
        if not path.is_file() or path.name in IGNORED_DASHBOARD_FILES:
            continue
        try:
            stat = path.stat()
        except OSError:
            continue
        items.append(
            {
                "path": rel(path),
                "name": path.name,
                "top_level": path.relative_to(source_dir).parts[0],
                "checksum": "",
                "size": stat.st_size,
                "modified_at": datetime.fromtimestamp(stat.st_mtime).replace(microsecond=0).isoformat(),
            }
        )
    return items


def latest_run(state: dict) -> dict | None:
    runs = state.get("runs", [])
    return runs[-1] if runs else None


def waiting_sources(source_dir: Path, state: dict, inventory: list[dict] | None = None) -> list[dict]:
    waiting = []
    processed = state.get("sources", {})
    items = inventory if inventory is not None else source_inventory(source_dir)
    for item in items:
        record = processed.get(item["name"]) or processed.get(item["top_level"])
        if not record:
            waiting.append(item)
            continue
        if not isinstance(record, dict):
            waiting.append(item)
            continue
        record_checksum = str(record.get("checksum", ""))
        if record_checksum in {"manifest", "corpus-manifest"}:
            continue
        processed_at = parse_time(record.get("last_processed_at")) if isinstance(record, dict) else None
        modified_at = parse_time(item.get("modified_at")) if item.get("modified_at") else None
        modified_after_processing = bool(processed_at and modified_at and modified_at > processed_at)
        if not modified_after_processing:
            continue
        if record_checksum:
            try:
                current_checksum = checksum(resolve_research_path(Path(item["path"])))
            except OSError:
                current_checksum = ""
            if current_checksum and current_checksum == record_checksum:
                continue
        if modified_after_processing:
            waiting.append(item)
    return waiting


def non_empty_files(path: Path) -> list[Path]:
    if not path.exists():
        return []
    if path.is_file():
        return [] if path.name in IGNORED_DASHBOARD_FILES else [path]
    def visible_file(item: Path) -> bool:
        if not item.is_file() or item.name in IGNORED_DASHBOARD_FILES:
            return False
        try:
            relative_parts = item.relative_to(path).parts
        except ValueError:
            relative_parts = item.parts
        return not any(part.startswith(".") for part in relative_parts)
    return sorted(
        item
        for item in path.rglob("*")
        if visible_file(item)
    )


def markdown_field(block: str, *names: str) -> str:
    for name in names:
        match = re.search(rf"^-[ \t]*{re.escape(name)}:[ \t]*(.*)$", block, flags=re.IGNORECASE | re.MULTILINE)
        if match:
            return match.group(1).strip()
    return ""


def parse_markdown_review_items(path: Path) -> list[dict]:
    if not path.exists():
        return []
    items = []
    for file_path in non_empty_files(path):
        try:
            text = read_text(file_path)
        except UnicodeDecodeError:
            continue
        blocks = re.split(r"\n(?=##\s+)", text)
        for block in blocks:
            item_id = markdown_field(block, "ID", "Evidence ID", "Pattern ID", "Insight ID", "Critique ID")
            status = markdown_field(block, "Status")
            if not item_id or not status:
                continue
            decision = markdown_field(block, "Decision")
            items.append(
                {
                    "id": item_id,
                    "type": markdown_field(block, "Type") or block.splitlines()[0].strip("# ").strip(),
                    "status": status,
                    "decision": decision,
                    "researcher": markdown_field(block, "Researcher"),
                    "date": markdown_field(block, "Date"),
                    "notes": markdown_field(block, "Notes"),
                    "proposed_change": markdown_field(block, "Proposed change", "Statement", "Observation", "Summary"),
                    "example": markdown_field(block, "Example"),
                    "future_analysis_change": markdown_field(block, "What will change for future analysis"),
                    "reason": markdown_field(block, "Helps us understand", "Reason"),
                    "affected_knowledge": markdown_field(block, "Affected knowledge"),
                    "source_reference": markdown_field(block, "Source reference"),
                    "supporting_evidence": markdown_field(block, "Supporting Evidence"),
                    "contradicting_evidence": markdown_field(block, "Contradicting Evidence"),
                    "source": rel(file_path),
                    "file_path": file_path,
                }
            )
    return items


def review_decisions_path(review_path: Path) -> Path:
    target = review_path if review_path.is_file() else review_path / "review-queue.md"
    return target.parent / "review-decisions.json"


def load_review_decisions(review_path: Path) -> dict:
    path = review_decisions_path(review_path)
    if not path.exists():
        return {}
    try:
        return json.loads(read_text(path))
    except json.JSONDecodeError:
        return {}


def save_review_decisions(review_path: Path, decisions: dict) -> None:
    write_text(review_decisions_path(review_path), json.dumps(decisions, indent=2, sort_keys=True) + "\n")


REVIEW_SNAPSHOTS_KEY = "_reviewed_snapshots"


def review_snapshot(item: dict, target: Path) -> dict:
    return {
        "captured_at": now().isoformat(),
        "proposal": review_summary_text(item, target),
        "reason": review_reason_text(item),
    }


def attach_review_change_metadata(items: list[dict], review_path: Path, decisions: dict) -> list[dict]:
    snapshots = decisions.get(REVIEW_SNAPSHOTS_KEY, {})
    if not isinstance(snapshots, dict):
        return items
    for item in items:
        snapshot = snapshots.get(item.get("id", ""))
        if not isinstance(snapshot, dict):
            continue
        proposal_lines = changed_line_numbers(snapshot.get("proposal", ""), review_summary_text(item, review_path))
        reason_lines = changed_line_numbers(snapshot.get("reason", ""), review_reason_text(item))
        changed_fields = {}
        if proposal_lines:
            changed_fields["proposal"] = proposal_lines
        if reason_lines:
            changed_fields["reason"] = reason_lines
        if changed_fields:
            item["reviewed_snapshot"] = snapshot
            item["changed_fields"] = changed_fields
    return items


LEARNING_CATEGORIES = {
    "scope_abstractness": {
        "label": "Scope / abstraction level",
        "keywords": [
            "abstract",
            "concreet",
            "concrete",
            "scope",
            "breed",
            "breder",
            "smal",
            "narrow",
            "broad",
            "generaliseer",
            "generalize",
            "te groot",
            "te klein",
            "te vroeg",
        ],
        "rule": "Keep research items at the right abstraction level: specific enough to be grounded, but not so narrow that synthesis becomes fragmented.",
    },
    "interpretation_quality": {
        "label": "Interpretation quality",
        "keywords": [
            "interpret",
            "duiding",
            "conclusie",
            "oorzaak",
            "causal",
            "cause",
            "betekent",
            "nuance",
            "verwart",
            "claim",
            "overinterpre",
            "aanname",
        ],
        "rule": "Separate observation from interpretation and preserve uncertainty, nuance and alternative explanations.",
    },
    "evidence_quality": {
        "label": "Evidence quality",
        "keywords": [
            "evidence",
            "bewijs",
            "bron",
            "source",
            "quote",
            "onderbouw",
            "support",
            "trace",
            "traceer",
            "contradict",
            "tegenbewijs",
            "niet ondersteunt",
            "missing",
            "mist",
            "ontbreekt",
        ],
        "rule": "Make every claim traceable to source-backed evidence and note weak support or missing contradictions.",
    },
    "quality_gates": {
        "label": "Quality gates",
        "keywords": [
            "quality gate",
            "gate",
            "check",
            "controle",
            "traceability",
            "timestamp",
            "assumption",
            "assumptions",
            "open question",
            "open questions",
        ],
        "rule": "Run lightweight quality gates before downstream synthesis: check traceability, support strength, contradictions, assumptions, open questions and review clarity.",
    },
}


def ensure_looped_learning_files() -> None:
    LOOPED_LEARNING_DIR.mkdir(parents=True, exist_ok=True)
    if not LOOPED_SUGGESTIONS_FILE.exists():
        write_text(
            LOOPED_SUGGESTIONS_FILE,
            "# Looped Learning Suggestions\n\nSuggested Research OS-wide learnings inferred from your review decisions and notes.\n",
        )
    if not LOOPED_ACTIVE_FILE.exists():
        write_text(
            LOOPED_ACTIVE_FILE,
            "# Active Looped Learnings\n\nApproved Research OS-wide learnings that should inform future Codex/Cowork analysis prompts.\n",
        )
    if not LOOPED_SIGNALS_FILE.exists():
        write_text(LOOPED_SIGNALS_FILE, "")
    if not LOOPED_STATE_FILE.exists():
        write_text(LOOPED_STATE_FILE, json.dumps({"runs": []}, indent=2) + "\n")


def load_looped_learning_state() -> dict:
    ensure_looped_learning_files()
    try:
        return json.loads(read_text(LOOPED_STATE_FILE))
    except json.JSONDecodeError:
        return {"runs": []}


def save_looped_learning_state(state: dict) -> None:
    ensure_looped_learning_files()
    write_text(LOOPED_STATE_FILE, json.dumps(state, indent=2, sort_keys=True) + "\n")


def looped_learning_prompt(signals: list[dict] | None = None) -> str:
    signals = signals if signals is not None else load_learning_signals()
    pending_count = len(signals)
    return f"""Process the Research OS Looped Learning feedback in Codex/Cowork.

Rules:
- Do not call APIs.
- Do not run local stubs.
- Do not make review decisions for me.
- Read `{rel(LOOPED_SIGNALS_FILE)}` for review feedback signals.
- Read `{rel(LOOPED_SUGGESTIONS_FILE)}` for existing suggested learnings.
- Read `{rel(LOOPED_ACTIVE_FILE)}` for approved active learnings.
- Infer Research OS-wide learning suggestions from Yes-with-notes, Needs changes and No decisions.
- Pay special attention to feedback about scope/abstractieniveau, interpretation quality, evidence quality and quality gates.
- Keep suggestions reviewable in `{rel(LOOPED_SUGGESTIONS_FILE)}`.
- Do not activate suggestions yourself; I review them in the web UI.
- After processing, update `{rel(LOOPED_STATE_FILE)}` with a run entry, including status `codex-complete`, processed signal count and timestamp.
- Report what changed and what still needs review.

Current feedback signals: {pending_count}
"""


def learning_item_id(category: str, stage: str) -> str:
    return f"LL-{slug(category)}-{slug(stage or 'general')}"


def infer_learning_categories(notes: str, decision: str) -> list[str]:
    text = notes.lower()
    matches = []
    for key, config in LEARNING_CATEGORIES.items():
        if any(keyword in text for keyword in config["keywords"]):
            matches.append(key)
    if matches:
        return matches
    if decision == "Revise" and notes.strip():
        return ["interpretation_quality"]
    if decision == "Reject" and notes.strip():
        return ["evidence_quality"]
    return []


def append_learning_signal(review_path: Path, item: dict, decision: str, researcher: str, notes: str) -> None:
    notes = notes.strip()
    if not notes and decision == "Approve":
        return
    ensure_looped_learning_files()
    stage = review_pipeline_stage(item)
    categories = infer_learning_categories(notes, decision)
    if not categories and decision == "Revise":
        categories = ["interpretation_quality"]
    if not categories and decision == "Reject":
        categories = ["evidence_quality"]
    signal = {
        "id": f"signal-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
        "created_at": now().isoformat(),
        "review_path": rel(review_path),
        "review_item_id": item.get("id", ""),
        "review_type": item.get("type", ""),
        "stage": stage,
        "decision": decision,
        "researcher": researcher or "Researcher",
        "notes": notes or f"{decision} without notes",
        "summary": review_summary_text(item, review_path),
        "categories": categories,
    }
    append_section(LOOPED_SIGNALS_FILE, json.dumps(signal, ensure_ascii=False) + "\n")
    for category in categories:
        ensure_learning_suggestion(category, stage, signal)


def learning_signal_count(category: str, stage: str) -> int:
    count = 0
    for signal in load_learning_signals():
        if category in signal.get("categories", []) and signal.get("stage") == stage:
            count += 1
    return count


def ensure_learning_suggestion(category: str, stage: str, signal: dict) -> None:
    ensure_looped_learning_files()
    item_id = learning_item_id(category, stage)
    existing = read_text(LOOPED_SUGGESTIONS_FILE)
    if re.search(rf"^-\s+ID:\s+{re.escape(item_id)}\s*$", existing, flags=re.MULTILINE):
        return
    config = LEARNING_CATEGORIES[category]
    stage_label = dict(REVIEW_PIPELINE_STAGES).get(stage, title_from_slug(stage))
    section = f"""## Review Item
- ID: {item_id}
- Type: Looped Learning
- Status: Pending
- Proposed by: Looped Learning
- Triggered by: Review feedback on {stage_label}
- Affected knowledge: Research OS-wide analysis instructions
- Proposed change: {config["rule"]}
- Helps us understand: This helps us understand that your review feedback points to a reusable improvement in {config["label"].lower()} for future {stage_label} items.
- Supporting Evidence: {rel(LOOPED_SIGNALS_FILE)}
- Contradicting Evidence: Not assessed yet.
- Available decisions:
  - Approve
  - Reject
  - Revise

## Researcher Decision
- Decision:
- Researcher:
- Date:
- Notes:
"""
    append_section(LOOPED_SUGGESTIONS_FILE, "\n" + section)


def is_looped_learning_path(path: Path) -> bool:
    return path.resolve() == LOOPED_SUGGESTIONS_FILE.resolve()


def activate_looped_learning(item_id: str, decision: str, notes: str) -> None:
    if decision != "Approve":
        return
    ensure_looped_learning_files()
    items = {item["id"]: item for item in parse_markdown_review_items(LOOPED_SUGGESTIONS_FILE)}
    item = items.get(item_id)
    if not item:
        return
    existing = read_text(LOOPED_ACTIVE_FILE)
    if re.search(rf"^###\s+{re.escape(item_id)}\s*$", existing, flags=re.MULTILINE):
        return
    section = f"""### {item_id}
- Category: {item.get("reason", "").split(" improve ", 1)[-1] if " improve " in item.get("reason", "") else item.get("type", "Looped Learning")}
- Stage: {review_pipeline_stage(item)}
- Rule: {item.get("proposed_change", "")}
- Approved: {now().date().isoformat()}
- Notes: {notes or item.get("notes", "")}
"""
    append_section(LOOPED_ACTIVE_FILE, "\n" + section)


def load_learning_signals() -> list[dict]:
    ensure_looped_learning_files()
    signals = []
    for line in read_text(LOOPED_SIGNALS_FILE).splitlines():
        if not line.strip():
            continue
        try:
            signals.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return signals


def active_learning_items(limit: int | None = None) -> list[dict]:
    ensure_looped_learning_files()
    text = read_text(LOOPED_ACTIVE_FILE)
    items = []
    for match in re.finditer(r"^###\s+(LL-[^\n]+)\n(.*?)(?=^###\s+LL-|\Z)", text, flags=re.MULTILINE | re.DOTALL):
        block = match.group(2)
        items.append(
            {
                "id": match.group(1).strip(),
                "category": markdown_field(block, "Category"),
                "stage": markdown_field(block, "Stage"),
                "rule": markdown_field(block, "Rule"),
                "approved": markdown_field(block, "Approved"),
                "notes": markdown_field(block, "Notes"),
            }
        )
    if limit is None:
        return items
    return list(reversed(items[-limit:]))


def learning_context_key(signal: dict) -> str:
    path = signal.get("review_path", "")
    match = re.search(r"Projects/([^/]+)/(?:02-rounds|03-research-rounds)/([^/]+)/", path)
    if match:
        project, round_id = match.groups()
        return f"{project} / {round_id}"
    return "Research OS"


def learning_quality_summary(signals: list[dict]) -> dict:
    total = len(signals)
    good = sum(1 for signal in signals if signal.get("decision") == "Approve")
    iterated = sum(1 for signal in signals if signal.get("decision") in {"Revise", "Reject"})
    return {
        "total": total,
        "good": good,
        "iterated": iterated,
        "good_rate": round((good / total) * 100) if total else 0,
        "iteration_rate": round((iterated / total) * 100) if total else 0,
    }


def learning_trend(signals: list[dict]) -> dict:
    contexts: dict[str, list[dict]] = {}
    for signal in signals:
        contexts.setdefault(learning_context_key(signal), []).append(signal)
    ordered = sorted(
        contexts.items(),
        key=lambda item: min((signal.get("created_at", "") for signal in item[1]), default=""),
    )
    points = [
        {
            "label": label,
            **learning_quality_summary(items),
        }
        for label, items in ordered
    ]
    if len(points) < 2:
        direction = "unknown"
        label = "Need more rounds/projects"
        delta = 0
    else:
        delta = points[-1]["good_rate"] - points[0]["good_rate"]
        if delta >= 5:
            direction = "up"
            label = f"+{delta} pts vs first"
        elif delta <= -5:
            direction = "down"
            label = f"{delta} pts vs first"
        else:
            direction = "flat"
            label = "stable"
    return {"points": points, "direction": direction, "label": label, "delta": delta}


def learning_quality_by(signals: list[dict], field: str, defaults: Iterable[str] = ()) -> dict:
    grouped: dict[str, list[dict]] = {key: [] for key in defaults}
    for signal in signals:
        keys = signal.get(field, [])
        if isinstance(keys, str):
            keys = [keys]
        if not keys:
            keys = ["uncategorized"]
        for key in keys:
            grouped.setdefault(str(key), []).append(signal)
    result = {}
    for key, items in grouped.items():
        if not items:
            continue
        result[key] = {
            **learning_quality_summary(items),
            "trend": learning_trend(items),
        }
    return result


def top_learning_bucket(values: dict) -> tuple[str, dict] | None:
    populated = [(key, value) for key, value in values.items() if value.get("total")]
    if not populated:
        return None
    return max(populated, key=lambda item: (item[1].get("iterated", 0), item[1].get("total", 0)))


def learning_interpretation(signals: list[dict], quality_by_stage: dict, quality_by_theme: dict) -> dict:
    total = len(signals)
    if not total:
        return {
            "headline": "No looped-learning feedback has been captured yet.",
            "details": [
                "Once review notes are saved, this card will explain what Research OS is learning from them.",
            ],
            "trend": "Not enough history yet.",
        }
    quality = learning_quality_summary(signals)
    stage = top_learning_bucket(quality_by_stage)
    theme = top_learning_bucket(quality_by_theme)
    details = [
        f"{quality['iterated']} of {total} captured signals asked for some iteration. That does not mean those whole items were wrong; small wording notes and larger changes both count once.",
    ]
    if stage:
        details.append(
            f"Most iteration feedback is currently attached to {dict(REVIEW_PIPELINE_STAGES).get(stage[0], title_from_slug(stage[0])).lower()}."
        )
    if theme:
        theme_label = LEARNING_CATEGORIES.get(theme[0], {}).get("label", title_from_slug(theme[0]))
        details.append(f"The strongest recurring theme is {theme_label.lower()}.")
    trend = learning_trend(signals)
    points = trend.get("points", [])
    if len(points) < 2:
        trend_text = "No clear trend yet because there is not enough comparable history."
    else:
        first = points[0].get("iteration_rate", 0)
        latest = points[-1].get("iteration_rate", 0)
        delta = latest - first
        if abs(delta) < 5:
            trend_text = "No strong trend yet; the amount of iteration feedback is similar across captured contexts."
        elif delta > 0:
            trend_text = "Iteration feedback is higher in the latest captured context, so this is a good moment to look at the active learnings before the next synthesis pass."
        else:
            trend_text = "Iteration feedback is lower in the latest captured context, but the history is still small, so treat this as directional rather than a score."
    return {
        "headline": "The loop is mostly teaching Research OS how to make analysis more concrete, readable and reviewable.",
        "details": details,
        "trend": trend_text,
    }


def looped_learning_metrics() -> dict:
    ensure_looped_learning_files()
    signals = load_learning_signals()
    state = load_looped_learning_state()
    latest_run = state.get("runs", [])[-1] if state.get("runs") else {}
    latest_processed = int(latest_run.get("processed_signal_count", 0) or 0)
    signals_waiting = max(len(signals) - latest_processed, 0)
    suggestions = expanded_review_items(LOOPED_SUGGESTIONS_FILE)
    active_count = len(re.findall(r"^###\s+LL-", read_text(LOOPED_ACTIVE_FILE), flags=re.MULTILINE))
    category_counts = {key: 0 for key in LEARNING_CATEGORIES}
    stage_counts: dict[str, int] = {}
    decision_counts: dict[str, int] = {}
    for signal in signals:
        stage = signal.get("stage", "reviews")
        stage_counts[stage] = stage_counts.get(stage, 0) + 1
        decision = signal.get("decision", "")
        decision_counts[decision] = decision_counts.get(decision, 0) + 1
        for category in signal.get("categories", []):
            category_counts[category] = category_counts.get(category, 0) + 1
    pending_suggestions = sum(1 for item in suggestions if item["status"].lower() in {"pending", "proposed", "open"} and not item["decision"])
    decided_suggestions = len(suggestions) - pending_suggestions
    quality_overall = learning_quality_summary(signals)
    quality_by_stage = learning_quality_by(signals, "stage", ["evidence", "patterns", "insights", "recommendations", "deliverables"])
    quality_by_theme = learning_quality_by(signals, "categories", LEARNING_CATEGORIES.keys())
    if pending_suggestions:
        status_label = f"{pending_suggestions} suggestion{'s' if pending_suggestions != 1 else ''} to review"
    elif signals_waiting:
        status_label = f"{signals_waiting} signal{'s' if signals_waiting != 1 else ''} to process"
    else:
        status_label = "up to date"
    return {
        "signals": len(signals),
        "signals_waiting": signals_waiting,
        "signals_with_notes": len([signal for signal in signals if signal.get("notes", "").strip()]),
        "suggestions_total": len(suggestions),
        "suggestions_pending": pending_suggestions,
        "suggestions_decided": decided_suggestions,
        "active_learnings": active_count,
        "status": "yellow" if pending_suggestions or signals_waiting else "green",
        "status_label": status_label,
        "latest_run": latest_run,
        "prompt": looped_learning_prompt(signals),
        "category_counts": category_counts,
        "stage_counts": stage_counts,
        "decision_counts": decision_counts,
        "quality_overall": {
            **quality_overall,
            "trend": learning_trend(signals),
        },
        "quality_by_stage": quality_by_stage,
        "quality_by_theme": quality_by_theme,
        "learning_interpretation": learning_interpretation(signals, quality_by_stage, quality_by_theme),
        "recent_active_learnings": active_learning_items(limit=5),
        "active_learnings_href": dashboard_file_link(LOOPED_ACTIVE_FILE),
        "suggestions_href": dashboard_file_link(LOOPED_SUGGESTIONS_FILE) + "&mode=focus",
    }


def evidence_detail(evidence_path: Path, item_id: str) -> dict | None:
    try:
        text = read_text(evidence_path)
    except UnicodeDecodeError:
        return None
    match = re.search(rf"^###\s+{re.escape(item_id)}\s*\n(.*?)(?=\n###\s+|\Z)", text, flags=re.DOTALL | re.MULTILINE)
    if not match:
        return None
    block = match.group(1)
    return {
        "evidence_id": item_id,
        "source": markdown_field(block, "Source"),
        "source_reference": markdown_field(block, "Source reference"),
        "research_question": markdown_field(block, "Research Question"),
        "observation": markdown_field(block, "Observation"),
        "quote": markdown_field(block, "Quote"),
        "uncertainty": markdown_field(block, "Uncertainty"),
        "salience": markdown_field(block, "Salience"),
        "interpretation_note": markdown_field(block, "Helps us understand", "Interpretation note"),
    }


def markdown_item_detail(path: Path, item_id: str, field_name: str) -> dict | None:
    try:
        text = read_text(path)
    except UnicodeDecodeError:
        return None
    match = re.search(rf"^###\s+{re.escape(item_id)}\s*\n(.*?)(?=\n###\s+|\Z)", text, flags=re.DOTALL | re.MULTILINE)
    if not match:
        return None
    block = match.group(1)
    return {
        "id": item_id,
        "status": markdown_field(block, "Status"),
        "statement": markdown_field(block, field_name),
        "what_we_learned": markdown_field(block, "What we learned", "Learned"),
        "what_we_should_do": markdown_field(block, "What we should do", "Recommendation"),
        "options": markdown_field(block, "Options"),
        "tradeoff": markdown_field(block, "Tradeoff", "Trade-off"),
        "based_on": markdown_field(block, "Based on", "Supporting Evidence", "Based on Patterns", "Based on Insights"),
        "type_label": markdown_field(block, "Type", "Labels"),
        "evidence": markdown_field(block, "Evidence"),
        "supporting_evidence": markdown_field(block, "Supporting Evidence"),
        "patterns": markdown_field(block, "Based on Patterns"),
        "insights": markdown_field(block, "Based on Insights"),
        "confidence": markdown_field(block, "Confidence"),
        "helps_us_understand": markdown_field(block, "Helps us understand"),
    }


def artifact_ids_from_text(text: str, prefix: str, fallback_path: Path | None = None) -> list[str]:
    found: list[str] = []
    for start, end in re.findall(rf"\b{prefix}-(\d{{3}})\s+through\s+(?:{prefix}-)?(\d{{3}})\b", text, flags=re.IGNORECASE):
        for number in range(int(start), int(end) + 1):
            found.append(f"{prefix.upper()}-{number:03d}")
    for item_id in re.findall(rf"\b{prefix}-\d{{3}}\b", text, flags=re.IGNORECASE):
        found.append(item_id.upper())
    fallback_terms = {
        "PAT": r"\bpatterns?\b",
        "INS": r"\binsights?\b",
        "REC": r"\brecommendations?\b",
    }
    if not found and fallback_path and re.search(fallback_terms.get(prefix.upper(), rf"\b{prefix}\b"), text, flags=re.IGNORECASE):
        for file_path in non_empty_files(fallback_path):
            if file_path.suffix.lower() != ".md":
                continue
            try:
                file_text = read_text(file_path)
            except UnicodeDecodeError:
                continue
            found.extend(match.upper() for match in re.findall(rf"\b{prefix}-\d{{3}}\b", file_text, flags=re.IGNORECASE))
    deduped = []
    for item_id in found:
        if item_id not in deduped:
            deduped.append(item_id)
    return deduped


def round_dir_for_review_path(path: Path) -> Path | None:
    target = path if path.is_file() else path / "review-queue.md"
    if target.name != "review-queue.md" or len(target.parents) < 2:
        return None
    return target.parents[1]


def expanded_review_items(path: Path) -> list[dict]:
    decisions = load_review_decisions(path)
    expanded = []
    seen_round_artifacts: set[str] = set()
    round_dir = round_dir_for_review_path(path)
    pattern_path = (round_path(round_dir, "patterns") / "patterns.md") if round_dir else None
    insight_path = (round_path(round_dir, "insights") / "insights.md") if round_dir else None
    recommendation_path = (round_path(round_dir, "recommendations") / "recommendations.md") if round_dir else None
    quality_gates = {}
    if round_dir:
        source_total = len(source_inventory(round_path(round_dir, "sources")))
        evidence_total = markdown_heading_count(round_path(round_dir, "evidence"), r"^###\s+EV-[A-Z]+-\d{3}\b")
        quality_gates = round_quality_gates(round_dir, source_total=source_total, evidence_total=evidence_total)

    def item_gate_issues(stage: str, *ids: str) -> list[dict]:
        wanted = {item_id for item_id in ids if item_id}
        if not wanted:
            return []
        return [issue for issue in quality_gates.get(stage, []) if issue.get("id") in wanted]

    for item in parse_markdown_review_items(path):
        review_text = " ".join([item.get("proposed_change", ""), item.get("reason", ""), item.get("affected_knowledge", "")])
        ids = evidence_ids_from_text(review_text)
        evidence_path = resolve_review_reference(item.get("supporting_evidence", ""), item["file_path"])
        details = []
        if evidence_path and evidence_path.suffix.lower() == ".md":
            for evidence_id in ids:
                detail = evidence_detail(evidence_path, evidence_id)
                if detail:
                    details.append(detail)
        if details:
            for detail in details:
                child_id = f"{item['id']}::{detail['evidence_id']}"
                stored = decisions.get(child_id, {})
                gates = item_gate_issues("evidence", detail["evidence_id"])
                expanded.append(
                    {
                        **item,
                        "id": child_id,
                        "parent_id": item["id"],
                        "type": "Evidence",
                        "evidence_id": detail["evidence_id"],
                        "research_question": detail["research_question"],
                        "source_detail": detail["source"],
                        "source_reference": detail["source_reference"],
                        "quote": detail["quote"],
                        "uncertainty": detail["uncertainty"],
                        "salience": detail["salience"],
                        "proposed_change": detail["observation"],
                        "reason": detail["interpretation_note"] or item.get("reason", ""),
                        "decision": stored.get("decision", ""),
                        "researcher": stored.get("researcher", ""),
                        "date": stored.get("date", ""),
                        "notes": stored.get("notes", ""),
                        "is_virtual": True,
                        "gate_issues": gates,
                        "gate_count": len(gates),
                    }
                )
        if pattern_path and pattern_path.exists():
            for pattern_id in artifact_ids_from_text(review_text, "PAT", pattern_path):
                detail = markdown_item_detail(pattern_path, pattern_id, "Pattern")
                child_id = f"ROUND-PATTERNS::{pattern_id}"
                if not detail or child_id in seen_round_artifacts:
                    continue
                seen_round_artifacts.add(child_id)
                stored = decisions.get(child_id, {})
                gates = item_gate_issues("patterns", pattern_id)
                expanded.append(
                    {
                        **item,
                        "id": child_id,
                        "parent_id": item["id"],
                        "type": "Pattern",
                        "pattern_id": pattern_id,
                        "supporting_evidence": os.path.relpath(pattern_path, item["file_path"].parent),
                        "source_reference": f"Evidence: {detail['evidence']}",
                        "evidence_links": detail["evidence"],
                        "proposed_change": detail["statement"],
                        "reason": detail["helps_us_understand"] or detail["confidence"] or item.get("reason", ""),
                        "decision": stored.get("decision", ""),
                        "researcher": stored.get("researcher", ""),
                        "date": stored.get("date", ""),
                        "notes": stored.get("notes", ""),
                        "is_virtual": True,
                        "gate_issues": gates,
                        "gate_count": len(gates),
                    }
                )
        if insight_path and insight_path.exists():
            for insight_id in artifact_ids_from_text(review_text, "INS", insight_path):
                detail = markdown_item_detail(insight_path, insight_id, "Insight")
                child_id = f"ROUND-INSIGHTS::{insight_id}"
                if not detail or child_id in seen_round_artifacts:
                    continue
                seen_round_artifacts.add(child_id)
                stored = decisions.get(child_id, {})
                gates = item_gate_issues("insights", insight_id)
                expanded.append(
                    {
                        **item,
                        "id": child_id,
                        "parent_id": item["id"],
                        "type": "Insight",
                        "insight_id": insight_id,
                        "supporting_evidence": os.path.relpath(insight_path, item["file_path"].parent),
                        "source_reference": f"Patterns: {detail['patterns']}",
                        "evidence_links": detail["supporting_evidence"],
                        "proposed_change": detail["statement"],
                        "reason": detail["helps_us_understand"] or detail["confidence"] or item.get("reason", ""),
                        "decision": stored.get("decision", ""),
                        "researcher": stored.get("researcher", ""),
                        "date": stored.get("date", ""),
                        "notes": stored.get("notes", ""),
                        "is_virtual": True,
                        "gate_issues": gates,
                        "gate_count": len(gates),
                    }
                )
        if recommendation_path and recommendation_path.exists():
            for recommendation_id in artifact_ids_from_text(review_text, "REC", recommendation_path):
                detail = markdown_item_detail(recommendation_path, recommendation_id, "What we should do")
                child_id = f"ROUND-RECOMMENDATIONS::{recommendation_id}"
                if not detail or child_id in seen_round_artifacts:
                    continue
                seen_round_artifacts.add(child_id)
                stored = decisions.get(child_id, {})
                gates = item_gate_issues("recommendations", recommendation_id)
                learned = detail.get("what_we_learned") or detail.get("helps_us_understand") or "No learning summary found."
                should_do = detail.get("what_we_should_do") or detail.get("statement") or "No recommendation found."
                proposal = f"What we learned: {learned}\n\nWhat we should do: {should_do}"
                if detail.get("options"):
                    proposal += f"\n\nOptions: {detail['options']}"
                if detail.get("tradeoff"):
                    proposal += f"\n\nTradeoff: {detail['tradeoff']}"
                expanded.append(
                    {
                        **item,
                        "id": child_id,
                        "parent_id": item["id"],
                        "type": "Recommendation",
                        "recommendation_id": recommendation_id,
                        "supporting_evidence": os.path.relpath(recommendation_path, item["file_path"].parent),
                        "source_reference": f"Based on: {detail['based_on']}",
                        "evidence_links": detail["based_on"],
                        "proposed_change": proposal,
                        "reason": learned,
                        "decision": stored.get("decision", ""),
                        "researcher": stored.get("researcher", ""),
                        "date": stored.get("date", ""),
                        "notes": stored.get("notes", ""),
                        "is_virtual": True,
                        "gate_issues": gates,
                        "gate_count": len(gates),
                    }
                )
        if not details and not any(item.get("id") == existing.get("parent_id") for existing in expanded):
            stored = decisions.get(item["id"], {})
            if stored:
                item = {**item, **stored}
            stage = review_pipeline_stage(item)
            item["gate_issues"] = item_gate_issues(stage, item.get("id", ""))
            item["gate_count"] = len(item["gate_issues"])
            expanded.append(item)
    stage_order = {
        "context": 0,
        "sources": 1,
        "evidence": 2,
        "patterns": 3,
        "insights": 4,
        "recommendations": 5,
        "reviews": 6,
        "learning": 7,
        "deliverables": 8,
    }
    return attach_review_change_metadata([
        item
        for _index, item in sorted(
            enumerate(expanded),
            key=lambda pair: (stage_order.get(review_pipeline_stage(pair[1]), 9), -int(pair[1].get("gate_count", 0)), pair[0]),
        )
    ], path, decisions)


def pending_markdown_items(path: Path) -> int:
    return sum(
        1
        for item in expanded_review_items(path)
        if item["status"].lower() in {"pending", "proposed", "open"} and not item["decision"]
    )


def update_review_decision(review_path: Path, item_id: str, decision: str, researcher: str, notes: str) -> None:
    if decision not in {"Approve", "Reject", "Revise"}:
        raise ValueError("Decision must be Approve, Reject or Revise.")
    review_items = {item["id"]: item for item in expanded_review_items(review_path)}
    signal_item = review_items.get(item_id)
    decisions = load_review_decisions(review_path)
    if signal_item:
        decisions.setdefault(REVIEW_SNAPSHOTS_KEY, {})[item_id] = review_snapshot(signal_item, review_path)
    if "::" in item_id:
        decisions[item_id] = {
            "decision": decision,
            "researcher": researcher or "Researcher",
            "date": now().date().isoformat(),
            "notes": notes,
        }
        save_review_decisions(review_path, decisions)
        if signal_item and not is_looped_learning_path(review_path):
            append_learning_signal(review_path, signal_item, decision, researcher, notes)
        return
    text = read_text(review_path)
    blocks = re.split(r"(\n(?=##\s+))", text)
    changed = False
    updated_blocks = []
    for index in range(0, len(blocks), 2):
        block = blocks[index]
        separator = blocks[index + 1] if index + 1 < len(blocks) else ""
        block_id = markdown_field(block, "ID", "Evidence ID", "Pattern ID", "Insight ID", "Critique ID")
        if block_id == item_id:
            replacements = {
                "Decision": decision,
                "Researcher": researcher or "Researcher",
                "Date": now().date().isoformat(),
                "Notes": notes,
            }
            for field, value in replacements.items():
                pattern = rf"^-[ \t]*{field}:[ \t]*.*$"
                replacement = f"- {field}: {value}"
                if re.search(pattern, block, flags=re.IGNORECASE | re.MULTILINE):
                    block = re.sub(pattern, replacement, block, count=1, flags=re.IGNORECASE | re.MULTILINE)
                else:
                    block += f"\n{replacement}"
            changed = True
        updated_blocks.append(block + separator)
    if not changed:
        raise ValueError(f"Review item not found: {item_id}")
    write_text(review_path, "".join(updated_blocks))
    save_review_decisions(review_path, decisions)
    if is_looped_learning_path(review_path):
        activate_looped_learning(item_id, decision, notes)
    elif signal_item:
        append_learning_signal(review_path, signal_item, decision, researcher, notes)


def update_artifact_item(path: Path, item_id: str, block: str) -> None:
    if path.suffix.lower() != ".md":
        raise ValueError("Only Markdown artifact files can be edited here.")
    text = read_text(path)
    item_id = item_id.strip().upper()
    if not re.match(r"^(EV-[A-Z]+-\d{3}|PAT-\d{3}|INS-\d{3}|REC-\d{3})$", item_id):
        raise ValueError("Unsupported artifact item ID.")
    clean_block = block.strip()
    if not clean_block:
        raise ValueError("Edited block cannot be empty.")
    if not re.match(rf"^###\s+{re.escape(item_id)}\s*$", clean_block, flags=re.MULTILINE | re.IGNORECASE):
        clean_block = f"### {item_id}\n{clean_block}"
    pattern = rf"^###\s+{re.escape(item_id)}\s*\n.*?(?=\n###\s+(?:EV-[A-Z]+-\d{{3}}|PAT-\d{{3}}|INS-\d{{3}}|REC-\d{{3}})\s*$|\Z)"
    if not re.search(pattern, text, flags=re.DOTALL | re.MULTILINE | re.IGNORECASE):
        raise ValueError(f"Artifact item not found: {item_id}")
    updated = re.sub(pattern, clean_block.rstrip() + "\n", text, count=1, flags=re.DOTALL | re.MULTILINE | re.IGNORECASE)
    write_text(path, updated)


def review_reference_link(reference: str, base_file: Path) -> str:
    clean = reference.strip().strip("`")
    if not clean or clean.lower() in {"none", "not assessed yet"}:
        return html.escape(reference or "-")
    candidate = (base_file.parent / clean).resolve()
    if not candidate.exists():
        candidate = (base_file.parents[1] / clean).resolve() if len(base_file.parents) > 1 else candidate
    if not candidate.exists():
        candidate = (base_file.parents[2] / clean).resolve() if len(base_file.parents) > 2 else candidate
    label = html.escape(review_reference_label(clean, candidate if candidate.exists() else None))
    path_hint = html.escape(clean)
    if candidate.exists():
        return f'<a class="doc-reference" href="{dashboard_file_link(candidate)}"><strong>{label}</strong><span>{path_hint}</span></a>'
    return f'<span class="doc-reference"><strong>{label}</strong><span>{path_hint}</span></span>'


def review_reference_label(reference: str, candidate: Path | None) -> str:
    path = candidate or Path(reference)
    name = path.name or reference
    stem = Path(name).stem if Path(name).suffix else name
    return title_from_slug(stem)


def review_document_name(item: dict, base_file: Path) -> str:
    reference = item.get("supporting_evidence") or item.get("source_reference", "")
    clean = reference.strip().strip("`")
    if not clean:
        return ""
    return review_reference_label(clean, resolve_review_reference(clean, base_file))


def review_summary_text(item: dict, base_file: Path) -> str:
    summary = item.get("proposed_change") or ""
    if "Review this Source for durable context" in summary:
        document = review_document_name(item, base_file)
        if document:
            return f"Should Research OS use '{document}' as reusable project context for future research rounds?"
        return "Should Research OS use this document as reusable project context for future research rounds?"
    return summary or "No proposal summary available."


SOURCE_SNIPPET_STOPWORDS = {
    "about",
    "after",
    "also",
    "before",
    "being",
    "concept",
    "could",
    "experiment",
    "finds",
    "found",
    "from",
    "have",
    "more",
    "need",
    "needs",
    "should",
    "than",
    "that",
    "their",
    "there",
    "this",
    "with",
    "without",
    "would",
}


def resolve_review_reference(reference: str, base_file: Path) -> Path | None:
    clean = reference.strip().strip("`")
    if not clean or clean.lower() in {"none", "not assessed yet"}:
        return None
    if len(clean) > 180 or re.search(r"\b(EV-[A-Z]+-\d{3}|PAT-\d{3}|INS-\d{3}|REC-\d{3})\b", clean, flags=re.IGNORECASE):
        return None
    if clean.lower().startswith(("based on:", "evidence:", "patterns:", "insights:", "source reference:")):
        return None
    if not any(marker in clean for marker in ["/", "\\", ".md", ".txt", ".pdf"]):
        return None
    candidates = [
        (base_file.parent / clean).resolve(),
        (base_file.parents[1] / clean).resolve() if len(base_file.parents) > 1 else (base_file.parent / clean).resolve(),
        (base_file.parents[2] / clean).resolve() if len(base_file.parents) > 2 else (base_file.parent / clean).resolve(),
    ]
    for candidate in candidates:
        try:
            if candidate.exists():
                return candidate
        except OSError:
            continue
    return None


def source_representation_path(source_id: str, base_file: Path) -> Path | None:
    clean = source_id.strip().strip("`")
    if not clean:
        return None
    for parent in base_file.parents:
        representation_dir = parent / "00-ai-work-files" / "01-source-representations"
        if representation_dir.exists():
            direct = representation_dir / f"{clean}-representation.md"
            if direct.exists():
                return direct
            matches = sorted(representation_dir.glob(f"{clean}*representation.md"))
            if matches:
                return matches[0]
    return None


def source_segments(path: Path) -> list[dict]:
    try:
        text = read_text(path)
    except UnicodeDecodeError:
        return []
    segments = []
    for block in re.split(r"\n(?=###\s+Segment\b)", text):
        if not block.lstrip().startswith("### Segment"):
            continue
        content_match = re.search(
            r"^-[ \t]*Content:[ \t]*(.*?)(?=\n-[ \t]*[A-Z][^:\n]+:|\n###\s+|\n##\s+|\Z)",
            block,
            flags=re.DOTALL | re.MULTILINE,
        )
        content = content_match.group(1).strip() if content_match else ""
        if content.startswith("```"):
            content = re.sub(r"^```[a-zA-Z0-9_-]*\n?", "", content)
            content = re.sub(r"\n?```$", "", content).strip()
        segments.append(
            {
                "id": markdown_field(block, "Segment ID"),
                "reference": markdown_field(block, "Source reference"),
                "content": content,
            }
        )
    return segments


def review_tokens(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-zA-Z][a-zA-Z-]{3,}", text.lower())
        if token not in SOURCE_SNIPPET_STOPWORDS
    }


def source_excerpt(text: str, limit: int = 560) -> str:
    clean = re.sub(r"\s+", " ", text).strip()
    if len(clean) <= limit:
        return clean
    return clean[:limit].rsplit(" ", 1)[0].rstrip(".,;:") + "..."


def timecode_seconds(value: str) -> int | None:
    parts = value.strip().split(":")
    if len(parts) == 2:
        minutes, seconds = parts
        return int(minutes) * 60 + int(seconds)
    if len(parts) == 3:
        hours, minutes, seconds = parts
        return int(hours) * 3600 + int(minutes) * 60 + int(seconds)
    return None


def timestamp_range(reference: str) -> tuple[int, int] | None:
    times = re.findall(r"\b\d{1,2}:\d{2}(?::\d{2})?\b", reference or "")
    if len(times) < 2:
        return None
    start = timecode_seconds(times[-2])
    end = timecode_seconds(times[-1])
    if start is None or end is None:
        return None
    return (min(start, end), max(start, end))


def timestamp_label(seconds: int) -> str:
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def transcript_turns(path: Path) -> list[dict]:
    try:
        text = read_text(path)
    except UnicodeDecodeError:
        return []
    lines = text.splitlines()
    turns = []
    current_time: int | None = None
    current_lines: list[str] = []
    for line in lines:
        stripped = line.strip()
        if re.fullmatch(r"\d{1,2}:\d{2}(?::\d{2})?", stripped):
            if current_time is not None and current_lines:
                turns.append({"time": current_time, "text": " ".join(current_lines).strip()})
            current_time = timecode_seconds(stripped)
            current_lines = []
        elif current_time is not None and stripped:
            current_lines.append(stripped)
    if current_time is not None and current_lines:
        turns.append({"time": current_time, "text": " ".join(current_lines).strip()})
    return turns


def source_file_from_representation(source_id: str, base_file: Path) -> Path | None:
    representation = source_representation_path(source_id, base_file)
    if not representation:
        return None
    try:
        text = read_text(representation)
    except UnicodeDecodeError:
        return None
    source_file = markdown_field(text, "Source file", "Original file")
    if not source_file:
        metadata = representation.with_name(representation.name.replace("-representation.md", "-metadata.md"))
        if metadata.exists():
            source_file = markdown_field(read_text(metadata), "Original file", "Source file")
    return resolve_research_path(Path(source_file)) if source_file else None


def source_file_from_item(item: dict, base_file: Path) -> Path | None:
    reference = item.get("source_reference", "")
    match = re.search(r"`([^`]+)`", reference)
    if match:
        candidate = resolve_research_path(Path(match.group(1)))
        if candidate.exists():
            return candidate
    source_detail = item.get("source_detail", "")
    candidate = source_file_from_representation(source_detail, base_file)
    if candidate and candidate.exists():
        return candidate
    reference_path = resolve_review_reference(reference, base_file)
    if reference_path and reference_path.exists() and reference_path.suffix.lower() in {".txt", ".md"}:
        return reference_path
    return None


def transcript_excerpt(item: dict, base_file: Path) -> dict | None:
    source_file = source_file_from_item(item, base_file)
    if not source_file or source_file.suffix.lower() not in {".txt", ".md"}:
        return None
    range_value = timestamp_range(item.get("source_reference", ""))
    if not range_value:
        return None
    turns = transcript_turns(source_file)
    if not turns:
        return None
    start, end = range_value
    selected = [
        turn for turn in turns
        if start <= int(turn["time"]) <= end
    ]
    if not selected:
        selected = [
            turn for turn in turns
            if abs(int(turn["time"]) - start) <= 30
        ][:4]
    if not selected:
        return None
    return {
        "reference": f"{review_reference_label(source_file.name, source_file)} · {timestamp_label(start)}-{timestamp_label(end)}",
        "turns": selected[:10],
    }


def transcript_snippet_html(snippet: dict) -> str:
    rows = "".join(
        f"""<div class="transcript-line"><time>{html.escape(timestamp_label(int(turn["time"])))}</time><p>{html.escape(turn["text"])}</p></div>"""
        for turn in snippet.get("turns", [])
    )
    return f"""<section class="source-snippet transcript-snippet">
      <h3>Source snippet</h3>
      <p class="source-meta">{html.escape(snippet.get("reference", "Transcript"))}</p>
      <div class="transcript-lines">{rows}</div>
    </section>"""


def best_source_segment(item: dict, base_file: Path) -> dict | None:
    representation = source_representation_path(item.get("source_detail", ""), base_file)
    if not representation:
        return None
    segments = source_segments(representation)
    if not segments:
        return None
    source_reference = item.get("source_reference", "").strip().strip("`")
    if source_reference:
        for segment in segments:
            if source_reference and source_reference in segment.get("reference", ""):
                return segment
    target_tokens = review_tokens(
        " ".join(
            [
                item.get("research_question", ""),
                item.get("proposed_change", ""),
                item.get("reason", ""),
            ]
        )
    )
    if not target_tokens:
        return segments[0]
    scored = []
    for segment in segments:
        segment_tokens = review_tokens(segment.get("content", ""))
        scored.append((len(target_tokens & segment_tokens), segment))
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return scored[0][1] if scored and scored[0][0] else None


def source_document_preview(path: Path) -> dict | None:
    segments = source_segments(path)
    for segment in segments:
        content = segment.get("content", "").strip()
        if content:
            return segment
    try:
        text = read_text(path)
    except UnicodeDecodeError:
        return None
    paragraphs = [line.strip() for line in text.splitlines() if line.strip() and not line.startswith("#")]
    if not paragraphs:
        return None
    return {"id": "", "reference": review_reference_label(path.name, path), "content": " ".join(paragraphs[:4])}


def source_snippet_html(item: dict, base_file: Path) -> str:
    transcript = transcript_excerpt(item, base_file)
    if transcript:
        return transcript_snippet_html(transcript)
    quote = item.get("quote", "").strip()
    if quote:
        reference = item.get("source_reference") or item.get("source_detail") or "Source"
        return f"""<section class="source-snippet">
          <h3>Source snippet</h3>
          <p class="source-meta">{html.escape(reference)}</p>
          <blockquote>{html.escape(source_excerpt(quote))}</blockquote>
        </section>"""
    if (item.get("pattern_id") or item.get("insight_id")) and item.get("source_reference"):
        return f"""<section class="source-snippet">
          <h3>Based on</h3>
          <blockquote>{html.escape(source_excerpt(item['source_reference']))}</blockquote>
        </section>"""
    segment = best_source_segment(item, base_file) if item.get("is_virtual") else None
    if not segment:
        reference_path = resolve_review_reference(item.get("supporting_evidence") or item.get("source_reference", ""), base_file)
        if reference_path and reference_path.suffix.lower() == ".md":
            segment = source_document_preview(reference_path)
    if not segment or not segment.get("content"):
        return ""
    reference = segment.get("reference") or segment.get("id") or "Source"
    return f"""<section class="source-snippet">
      <h3>Source snippet</h3>
      <p class="source-meta">{html.escape(reference)}</p>
      <blockquote>{html.escape(source_excerpt(segment['content']))}</blockquote>
    </section>"""


def evidence_ids_from_text(text: str) -> list[str]:
    found: list[str] = []
    for prefix, start, end in re.findall(r"\b(EV-[A-Z]+-)(\d{3})\s+through\s+(?:EV-[A-Z]+-)?(\d{3})\b", text, flags=re.IGNORECASE):
        for number in range(int(start), int(end) + 1):
            found.append(f"{prefix.upper()}{number:03d}")
    for item_id in re.findall(r"\bEV-[A-Z]+-\d{3}\b", text, flags=re.IGNORECASE):
        found.append(item_id.upper())
    deduped = []
    for item_id in found:
        if item_id not in deduped:
            deduped.append(item_id)
    return deduped


def evidence_preview_html(item: dict, base_file: Path) -> str:
    round_dir = round_dir_for_review_path(base_file)
    if review_pipeline_stage(item) in {"patterns", "insights"} and round_dir:
        evidence_path = round_path(round_dir, "evidence") / "evidence.md"
    else:
        evidence_path = resolve_review_reference(item.get("supporting_evidence", ""), base_file)
    if not evidence_path or not evidence_path.exists() or evidence_path.suffix.lower() != ".md":
        return ""
    ids = evidence_ids_from_text(
        " ".join(
            [
                item.get("proposed_change", ""),
                item.get("reason", ""),
                item.get("source_reference", ""),
                item.get("evidence_links", ""),
            ]
        )
    )
    if not ids:
        return ""
    try:
        text = read_text(evidence_path)
    except UnicodeDecodeError:
        return ""
    previews = []
    for item_id in ids:
        match = re.search(rf"^###\s+{re.escape(item_id)}\s*\n(.*?)(?=\n###\s+|\Z)", text, flags=re.DOTALL | re.MULTILINE)
        if not match:
            continue
        block = match.group(1)
        observation = markdown_field(block, "Observation")
        question = markdown_field(block, "Research Question")
        note = markdown_field(block, "Helps us understand", "Interpretation note")
        source = markdown_field(block, "Source")
        moment = markdown_field(block, "Source reference")
        previews.append(
            f"""<li>
              <div><strong>{html.escape(item_id)}</strong><span>{html.escape(question)}</span></div>
              <p>{html.escape(observation)}</p>
              <small>{html.escape(" · ".join(part for part in [source, moment] if part))}</small>
              <em>{html.escape(note)}</em>
            </li>"""
        )
    if not previews:
        return ""
    return f"""<details class="evidence-preview" open>
      <summary>What this is based on ({len(previews)} items)</summary>
      <ul>{"".join(previews)}</ul>
    </details>"""


def review_question(item: dict) -> str:
    stage = review_pipeline_stage(item)
    if stage == "learning":
        return "Should Research OS learn this for future analysis?"
    if stage == "evidence":
        return "Should this evidence move into synthesis?"
    if stage == "patterns":
        return "Should this pattern move into insights?"
    if stage == "insights":
        return "Should this insight move into deliverables?"
    if stage == "recommendations":
        return "Should this recommendation move into outputs?"
    if stage == "deliverables":
        return "Should this deliverable be used?"
    item_type = item.get("type", "").lower()
    if "prior" in item_type or "context" in item_type:
        return "Should this context be used in this round?"
    if "round" in item_type:
        return "Should this round-level proposal move forward?"
    return "Should this become part of the research knowledge?"


def review_explanation(item: dict) -> str:
    stage = review_pipeline_stage(item)
    if stage == "learning":
        return "You are reviewing a Research OS-wide learning inferred from your feedback. If accepted, it will inform future Codex/Cowork analysis prompts."
    if stage == "evidence":
        return "You are reviewing Evidence: one source-backed observation before it feeds patterns and insights."
    if stage == "patterns":
        return "You are reviewing Patterns: a cross-evidence theme before it feeds insights."
    if stage == "insights":
        return "You are reviewing Insights: synthesized meaning before it feeds deliverables."
    if stage == "recommendations":
        return "You are reviewing Recommendations: what Research OS learned and what it suggests changing before outputs are created."
    if stage == "deliverables":
        return "You are reviewing a deliverable before it is shared or reused."
    item_type = item.get("type", "").lower()
    if "prior" in item_type or "context" in item_type:
        return "You are not approving a new Concept Test 02 finding here. You are deciding whether Concept Test 01 should be used as background context when interpreting Concept Test 02."
    return "You are deciding whether this proposed knowledge is ready to be used by Research OS."


def review_choice_hint(item: dict) -> str:
    stage = review_pipeline_stage(item)
    if stage == "learning":
        return "Yes means: use this as a Research OS-wide instruction. Needs changes means: direction is useful but wording or scope needs work. No means: do not use this learning."
    if stage == "evidence":
        return "Yes means: keep this evidence. Needs changes means: useful, but reword, narrow or check it. No means: do not use it."
    if stage == "patterns":
        return "Yes means: keep this pattern. Needs changes means: useful, but wording or evidence links need work. No means: do not use it."
    if stage == "insights":
        return "Yes means: keep this insight. Needs changes means: useful, but sharpen the claim or support. No means: do not use it."
    if stage == "recommendations":
        return "Yes means: use this recommendation in outputs. Needs changes means: useful, but sharpen the action or evidence. No means: do not use it."
    return "Yes means: use this. Needs changes means: useful direction, but wording, scope or evidence needs work. No means: do not use it."


def review_reason_label(item: dict) -> str:
    return "What this helps us understand"


def sentence_case_fragment(text: str) -> str:
    text = text.strip()
    if not text:
        return ""
    if re.match(r"^[A-Z]{2,}\b", text):
        return text
    return text[:1].lower() + text[1:]


def review_reason_text(item: dict) -> str:
    reason = (item.get("reason") or "").strip()
    if not reason:
        return "-"
    if re.match(r"^(This|It|Research OS|We)\b", reason):
        return reason
    reason = sentence_case_fragment(reason)
    if reason.endswith((".", "!", "?")):
        reason = reason[:-1]
    return f"This helps us understand that {reason}."


def inline_markdown_html(text: str) -> str:
    escaped = html.escape(text)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)


def simple_markdown_html(text: str) -> str:
    html_lines = []
    in_list = False
    list_tag = "ul"
    in_code = False
    code_lines = []
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if line.startswith("```"):
            if in_code:
                html_lines.append("<pre>" + html.escape("\n".join(code_lines)) + "</pre>")
                code_lines = []
                in_code = False
            else:
                if in_list:
                    html_lines.append(f"</{list_tag}>")
                    in_list = False
                in_code = True
            continue
        if in_code:
            code_lines.append(line)
            continue
        if not line.strip():
            if in_list:
                html_lines.append(f"</{list_tag}>")
                in_list = False
            continue
        heading = re.match(r"^(#{1,4})\s+(.+)$", line)
        if heading:
            if in_list:
                html_lines.append(f"</{list_tag}>")
                in_list = False
            level = min(len(heading.group(1)) + 1, 5)
            html_lines.append(f"<h{level}>{inline_markdown_html(heading.group(2))}</h{level}>")
            continue
        bullet = re.match(r"^[-*]\s+(.+)$", line)
        if bullet:
            if in_list and list_tag != "ul":
                html_lines.append(f"</{list_tag}>")
                in_list = False
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
                list_tag = "ul"
            html_lines.append(f"<li>{inline_markdown_html(bullet.group(1))}</li>")
            continue
        ordered = re.match(r"^\d+\.\s+(.+)$", line)
        if ordered:
            if in_list and list_tag != "ol":
                html_lines.append(f"</{list_tag}>")
                in_list = False
            if not in_list:
                html_lines.append("<ol>")
                in_list = True
                list_tag = "ol"
            html_lines.append(f"<li>{inline_markdown_html(ordered.group(1))}</li>")
            continue
        nested_bullet = re.match(r"^\s+[-*]\s+(.+)$", line)
        if nested_bullet:
            html_lines.append(f'<div class="nested-bullet">{inline_markdown_html(nested_bullet.group(1))}</div>')
            continue
        if in_list:
            html_lines.append(f"</{list_tag}>")
            in_list = False
        html_lines.append(f"<p>{inline_markdown_html(line)}</p>")
    if in_code:
        html_lines.append("<pre>" + html.escape("\n".join(code_lines)) + "</pre>")
    if in_list:
        html_lines.append(f"</{list_tag}>")
    return "\n".join(html_lines)


def artifact_card_items(text: str, kind: str) -> list[dict]:
    config = {
        "evidence": {
            "pattern": r"^###\s+(EV-[A-Z]+-\d{3})\s*$",
            "statement": "Observation",
            "meta": ["Research Question", "Source", "Source reference", "Helps us understand", "Interpretation note"],
        },
        "patterns": {
            "pattern": r"^###\s+(PAT-\d{3})\s*$",
            "statement": "Pattern",
            "meta": ["Evidence", "Helps us understand", "Confidence"],
        },
        "insights": {
            "pattern": r"^###\s+(INS-\d{3})\s*$",
            "statement": "Insight",
            "meta": ["Based on Patterns", "Helps us understand", "Confidence"],
        },
        "recommendations": {
            "pattern": r"^###\s+(REC-\d{3})\s*$",
            "statement": "What we should do",
            "meta": ["What we learned", "Based on", "Type", "Options", "Tradeoff", "Confidence", "Validation needed", "Open Questions"],
        },
    }.get(kind)
    if not config:
        return []
    matches = list(re.finditer(config["pattern"], text, flags=re.MULTILINE | re.IGNORECASE))
    items = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[start:end]
        items.append(
            {
                "id": match.group(1).upper(),
                "status": markdown_field(block, "Status"),
                "statement": markdown_field(block, config["statement"]),
                "block": f"### {match.group(1).upper()}\n{block.strip()}\n",
                "meta": [
                    (field, markdown_field(block, field))
                    for field in config["meta"]
                    if markdown_field(block, field)
                ],
            }
        )
    return items


def artifact_reference_preview_html(item: dict, target: Path) -> str:
    round_dir = target.parent.parent if len(target.parents) > 1 else None
    if not round_dir:
        return ""
    reference_text = " ".join(value for _label, value in item.get("meta", []))
    previews = []

    def add_preview(label: str, item_id: str, statement: str, detail: str = "") -> None:
        if statement:
            previews.append(
                f"<li><strong>{html.escape(item_id)}</strong><span>{html.escape(label)}</span><p>{html.escape(statement)}</p>{f'<small>{html.escape(detail)}</small>' if detail else ''}</li>"
            )

    evidence_path = round_path(round_dir, "evidence") / "evidence.md"
    for evidence_id in evidence_ids_in(reference_text)[:6]:
        detail = evidence_detail(evidence_path, evidence_id) if evidence_path.exists() else None
        if detail:
            add_preview("Evidence", evidence_id, detail.get("observation", ""), detail.get("interpretation_note", ""))

    pattern_path = round_path(round_dir, "patterns") / "patterns.md"
    for pattern_id in pattern_ids_in(reference_text)[:4]:
        detail = markdown_item_detail(pattern_path, pattern_id, "Pattern") if pattern_path.exists() else None
        if detail:
            add_preview("Pattern", pattern_id, detail.get("statement", ""), detail.get("helps_us_understand", ""))

    insight_path = round_path(round_dir, "insights") / "insights.md"
    for insight_id in insight_ids_in(reference_text)[:4]:
        detail = markdown_item_detail(insight_path, insight_id, "Insight") if insight_path.exists() else None
        if detail:
            add_preview("Insight", insight_id, detail.get("statement", ""), detail.get("helps_us_understand", ""))

    if not previews:
        return ""
    return f"""<details class="artifact-based-on" open>
      <summary>Based on</summary>
      <ul>{"".join(previews)}</ul>
    </details>"""


def dashboard_artifact_cards_page(title: str, text: str, kind: str, base_style: str, target: Path) -> str:
    items = artifact_card_items(text, kind)
    labels = {"evidence": "Evidence", "patterns": "Patterns", "insights": "Insights", "recommendations": "Recommendations"}
    cards = []
    for item in items:
        visible_meta = [
            (label, value)
            for label, value in item["meta"]
            if label.lower() not in {"source", "source reference"}
        ]
        meta = "".join(
            f"<dt>{html.escape(label)}</dt><dd>{html.escape(value)}</dd>"
            for label, value in visible_meta
        )
        status = f'<span class="artifact-status">{html.escape(item["status"])}</span>' if item.get("status") else ""
        block = html.escape(item.get("block", ""))
        based_on = artifact_reference_preview_html(item, target)
        cards.append(
            f"""<article class="artifact-card">
              <div class="artifact-head"><span>{html.escape(item['id'])}</span><div>{status}<button class="artifact-edit" type="button" data-edit="{html.escape(item['id'])}">Edit</button></div></div>
              <p>{html.escape(item['statement'] or 'No statement found.')}</p>
              {f'<dl>{meta}</dl>' if meta else ''}
              {based_on}
              <div class="artifact-editor" data-editor="{html.escape(item['id'])}">
                <textarea spellcheck="false">{block}</textarea>
                <div class="artifact-editor-actions"><button type="button" data-save="{html.escape(item['id'])}">Save</button><button type="button" data-cancel="{html.escape(item['id'])}">Cancel</button><span data-state="{html.escape(item['id'])}"></span></div>
              </div>
            </article>"""
        )
    card_style = base_style + """
      main { max-width: 980px; }
      .artifact-top { display:flex; align-items:flex-end; justify-content:space-between; gap:16px; margin-bottom:16px; }
      .artifact-top h1 { margin:0; }
      .artifact-count { color:var(--fg-3); font-size:12px; }
      .artifact-grid { display:grid; grid-template-columns: 1fr; gap:8px; }
      .artifact-card { border:1px solid var(--line); border-radius:7px; background:var(--surface-subtle); padding:11px 12px; }
      .artifact-head { display:flex; align-items:center; justify-content:space-between; gap:10px; color:var(--fg-2); font-size:11px; font-weight:700; }
      .artifact-status { color:var(--fg-3); font-weight:650; }
      .artifact-card p { margin:7px 0 8px; color:var(--fg-1); font-size:14px; line-height:1.42; }
      .artifact-card dl { display:grid; grid-template-columns:118px 1fr; gap:4px 10px; margin:0; font-size:11px; line-height:1.35; }
      .artifact-card dt { color:var(--fg-3); }
      .artifact-card dd { margin:0; color:var(--fg-2); }
      .artifact-edit { margin-left:8px; height:23px; border:1px solid var(--border-muted); border-radius:4px; background:#fff; color:var(--fg-2); font:inherit; font-size:11px; font-weight:650; padding:0 7px; cursor:pointer; }
      .artifact-editor { display:none; margin-top:10px; }
      .artifact-editor.open { display:block; }
      .artifact-editor textarea { width:100%; min-height:180px; resize:vertical; border:1px solid var(--border-muted); border-radius:5px; padding:9px; font:12px/1.45 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; color:var(--fg-1); box-sizing:border-box; }
      .artifact-editor-actions { display:flex; align-items:center; gap:8px; margin-top:8px; color:var(--fg-3); font-size:11px; }
      .artifact-editor-actions button { height:26px; border:1px solid var(--border-muted); border-radius:4px; background:#fff; color:var(--fg-2); font:inherit; font-size:11px; font-weight:650; padding:0 9px; cursor:pointer; }
      .artifact-based-on { margin-top:9px; border-top:1px solid var(--line); padding-top:8px; }
      .artifact-based-on summary { cursor:pointer; color:var(--fg-2); font-size:11px; font-weight:700; }
      .artifact-based-on ul { list-style:none; padding:0; margin:8px 0 0; display:grid; gap:7px; }
      .artifact-based-on li { border-left:2px solid var(--border-muted); padding-left:8px; }
      .artifact-based-on strong { color:var(--fg-2); font-size:11px; }
      .artifact-based-on span { margin-left:7px; color:var(--fg-3); font-size:11px; }
      .artifact-based-on p { margin:3px 0 0; font-size:12px; color:var(--fg-1); }
      .artifact-based-on small { display:block; margin-top:2px; color:var(--fg-3); font-size:11px; }
      @media (max-width: 680px) {
        .artifact-card dl { grid-template-columns:1fr; }
      }
    """
    body = "\n".join(cards) if cards else "<p>No items found.</p>"
    label = labels.get(kind, title)
    return f"""<!doctype html><html><head><title>{title}</title><style>{card_style}</style></head><body><main>
      <header class="artifact-top"><h1>{title}</h1><div class="artifact-count">{len(items)} {html.escape(label.lower())}</div></header>
      <section class="artifact-grid">{body}</section>
      <details class="raw"><summary>Raw Markdown</summary><pre>{html.escape(text)}</pre></details>
      <script>
        const path = new URLSearchParams(window.location.search).get("path") || "";
        document.querySelectorAll("[data-edit]").forEach(button => button.addEventListener("click", () => {{
          document.querySelector(`[data-editor="${{CSS.escape(button.dataset.edit)}}"]`)?.classList.add("open");
        }}));
        document.querySelectorAll("[data-cancel]").forEach(button => button.addEventListener("click", () => {{
          document.querySelector(`[data-editor="${{CSS.escape(button.dataset.cancel)}}"]`)?.classList.remove("open");
        }}));
        document.querySelectorAll("[data-save]").forEach(button => button.addEventListener("click", async () => {{
          const id = button.dataset.save;
          const editor = document.querySelector(`[data-editor="${{CSS.escape(id)}}"]`);
          const state = document.querySelector(`[data-state="${{CSS.escape(id)}}"]`);
          const textarea = editor?.querySelector("textarea");
          if (!textarea) return;
          state.textContent = "Saving...";
          const response = await fetch("/api/artifact-item", {{
            method: "POST",
            headers: {{ "Content-Type": "application/json" }},
            body: JSON.stringify({{ path, id, block: textarea.value }})
          }});
          if (!response.ok) {{
            state.textContent = await response.text();
            return;
          }}
          state.textContent = "Saved. Run the synthesis prompt to process changes.";
          setTimeout(() => location.reload(), 700);
        }}));
      </script>
    </main></body></html>"""



def has_placeholder_only(path: Path) -> bool:
    meaningful = []
    for file_path in non_empty_files(path):
        try:
            text = read_text(file_path).strip()
        except UnicodeDecodeError:
            meaningful.append(file_path)
            continue
        if text and not any(marker in text for marker in ["No accepted", "No Review Items are pending.", "To be added."]):
            meaningful.append(file_path)
    return not meaningful


def stage_status(path: Path, waiting_count: int = 0, review_count: int = 0) -> dict:
    files = len(non_empty_files(path))
    if review_count:
        status = "yellow"
        label = f"{review_count} to review"
    elif waiting_count:
        status = "yellow"
        label = f"{waiting_count} waiting"
    elif files and not has_placeholder_only(path):
        status = "green"
        label = "up to date"
    elif files:
        status = "gray"
        label = "empty"
    else:
        status = "gray"
        label = "not started"
    return {"status": status, "label": label, "files": files, "waiting": waiting_count, "review": review_count}


def markdown_heading_count(path: Path, pattern: str) -> int:
    count = 0
    for file_path in non_empty_files(path):
        if file_path.suffix.lower() != ".md":
            continue
        try:
            text = read_text(file_path)
        except UnicodeDecodeError:
            continue
        count += len(re.findall(pattern, text, flags=re.MULTILINE | re.IGNORECASE))
    return count


def enrich_stage_progress(stage: dict, total: int = 0, processed: int = 0, item_label: str = "item") -> dict:
    stage["total"] = max(total, 0)
    stage["processed"] = max(min(processed, total), 0) if total else max(processed, 0)
    stage["item_label"] = item_label
    return stage


def pending_review_stage_counts(review_path: Path) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in expanded_review_items(review_path):
        if item["status"].lower() not in {"pending", "proposed", "open"} or item["decision"]:
            continue
        stage = review_pipeline_stage(item)
        counts[stage] = counts.get(stage, 0) + 1
    return counts


def context_present(round_dir: Path) -> bool:
    context_files = [round_file(round_dir, "overview"), round_file(round_dir, "questions"), round_file(round_dir, "pipeline")]
    return all(path.exists() and not placeholder_file(path) for path in context_files[:2]) and context_files[2].exists()


def project_background_present(project_dir: Path) -> bool:
    return project_file(project_dir, "context").exists() and not placeholder_file(project_file(project_dir, "context"))


def ensure_round_recommendations_scaffold(round_dir: Path) -> None:
    recommendations_dir = round_path(round_dir, "recommendations")
    recommendations_dir.mkdir(parents=True, exist_ok=True)
    recommendations_file = recommendations_dir / "recommendations.md"
    if not recommendations_file.exists():
        write_text(recommendations_file, "# Recommendations\n\nNo accepted or proposed Recommendations have been recorded yet.\n")


def read_title(path: Path, fallback: str) -> str:
    if path.exists():
        try:
            match = re.search(r"^#\s+(.+)$", read_text(path), flags=re.MULTILINE)
            if match:
                return match.group(1).strip()
        except UnicodeDecodeError:
            pass
    return title_from_slug(fallback)


def dashboard_file_link(path: Path) -> str:
    return "/file?path=" + urllib.parse.quote(rel(path))


def dashboard_raw_file_link(path: Path) -> str:
    return "/raw-file?path=" + urllib.parse.quote(rel(path))


def dashboard_action(label: str, target: Path, instruction: str, prompt: str) -> dict:
    action = {
        "label": label,
        "path": rel(target),
        "href": dashboard_file_link(target),
        "instruction": instruction,
    }
    if prompt:
        action["prompt"] = prompt
    return action


def gate_instruction(stage: dict) -> str:
    issues = stage.get("gate_issues", [])
    if not issues:
        return ""
    lines = "; ".join(f"{issue.get('id', 'Gate')}: {issue.get('message', '')}" for issue in issues[:4])
    more = stage.get("gates", 0) - len(issues[:4])
    suffix = f"; plus {more} more" if more > 0 else ""
    return f" Checks needing attention: {lines}{suffix}."


def round_stage_action(round_dir: Path, key: str, stage: dict) -> dict:
    if key == "sources":
        target = round_path(round_dir, "sources")
        if stage["waiting"]:
            instruction = "Original research material for this round. Processing these files creates or updates source representations."
            prompt = ""
        else:
            instruction = "Add transcripts, notes, screenshots or other original research material here. Processing these files updates the internal source representations."
            prompt = ""
        return dashboard_action("Open sources", target, instruction, prompt)
    if key == "representations":
        target = round_path(round_dir, "representations")
        instruction = "These are generated by Codex/Cowork source processing. If files are waiting, use the dashboard prompt to process them."
        prompt = f"Check the source representations for this Research OS round: {rel(target)}. If source files are waiting, process them directly in Codex/Cowork. Do not call APIs, do not run local stubs, and do not use the backend pipeline."
        action = dashboard_action("Open representations", target, instruction, prompt)
        action["button_label"] = "Check reps"
        action["copy_label"] = "check representations"
        return action
    if key == "evidence":
        target = round_path(round_dir, "evidence")
        instruction = "Evidence is the source-backed observation layer. These cleanup notes will be handled by AI when you click Run synthesis next; you only need to review Evidence if Codex explicitly flags an item for researcher judgment." + gate_instruction(stage)
        return dashboard_action("Open evidence", target, instruction, "")
    if key == "patterns":
        target = round_path(round_dir, "patterns") / "patterns.md"
        instruction = "Patterns are the next synthesis layer after Evidence. If new Evidence has not been synthesized yet, run synthesis next so Codex can update Patterns and then surface any new or changed synthesis for review." + gate_instruction(stage)
        return dashboard_action("Open patterns", target, instruction, "")
    if key == "insights":
        target = round_path(round_dir, "insights") / "insights.md"
        instruction = "Review insight proposals. Approve only when the interpretation is supported by Evidence and uncertainty is clear." + gate_instruction(stage)
        return dashboard_action("Open insights", target, instruction, "")
    if key == "recommendations":
        target = round_path(round_dir, "recommendations") / "recommendations.md"
        instruction = "Review recommendations and opportunities. Each item should clearly show what Research OS learned and what should change, with traceability to Evidence, Patterns or Insights." + gate_instruction(stage)
        return dashboard_action("Open recommendations", target, instruction, "")
    if key == "reviews":
        target = round_path(round_dir, "reviews") / "review-queue.md"
        instruction = "Review pending items yourself in the web UI. Open the evidence links, add notes, then choose Approve, Reject or Revise."
        return dashboard_action("Review in UI", target, instruction, "")
    target = round_path(round_dir, "deliverables")
    instruction = "Deliverables are shown as separate cards below. Use each card to open, review, copy or generate that specific deliverable."
    return dashboard_action("Open deliverables", target, instruction, "")


def project_action(project_dir: Path, key: str) -> dict:
    project_rel = rel(project_dir)
    if key == "context":
        target = project_path(project_dir, "sources")
        instruction = "Add durable project context sources here. After adding files, use the dashboard prompt to process them in Codex/Cowork."
        prompt = f"Process any new or changed project-level context sources for this Research OS project in Codex/Cowork: {project_rel}. First read {rel(LOOPED_ACTIVE_FILE)} and apply any active Looped Learnings. Do not call APIs, do not run local stubs, and do not use backend processing. Update the Research OS documents directly, keep proposals pending for web UI review, update {PROJECT_STATE_FILE} when sources are genuinely processed, then summarize what changed and what still needs review."
        action = dashboard_action("Open project sources", target, instruction, prompt)
        action["button_label"] = "Process context"
        action["copy_label"] = "process project context"
        return action
    if key == "background":
        target = project_file(project_dir, "context")
        instruction = "This is the durable project background that you can edit yourself. It should contain context that applies across multiple research rounds."
        return dashboard_action("Open project background", target, instruction, "")
    target = project_path(project_dir, "reviews") / "project-context-proposals.md"
    instruction = "Review Project Context proposals yourself in the web UI. Add notes, then choose Approve, Reject or Revise."
    return dashboard_action("Review in UI", target, instruction, "")


def round_codex_processing_prompt(round_dir: Path, sources: list[dict]) -> str:
    round_rel = rel(round_dir)
    source_lines = "\n".join(f"- {source['id']}: {rel(source['path'])}" for source in sources) or "- No changed sources detected."
    return f"""Process this Research OS round in Codex/Cowork, not through the backend pipeline:
{round_rel}

Rules:
- Do not call OpenAI APIs.
- Do not run local stub generation.
- Do not make review decisions for me.
- Read and apply active Looped Learnings from `{rel(LOOPED_ACTIVE_FILE)}`.
- Read the round overview, research questions, pipeline settings, existing source representations, evidence, patterns, insights, recommendations and review queue.
- Apply source-type rules from pipeline settings. If a source is marked `researcher-synthesis`, treat it as high-weight directional researcher interpretation for Insights, Recommendations and Current Understanding; do not treat it as standalone participant Evidence unless explicitly requested.
- {research_lens_prompt_block(round_dir).replace(chr(10), chr(10) + "- ")}
- Check lightweight quality gates while updating synthesis: traceability/timestamps, support strength, contradicting evidence, assumptions/open questions and `Helps us understand` fields.
- Do not over-compress Patterns, Insights or Recommendations. Every item must stand alone: make clear what was unclear/useful/risky/actionable, not only that something should be better.
- Maintain Recommendations as a living synthesis layer. Each Recommendation should include `What we learned` and `What we should do`, with optional options/tradeoff when the research supports multiple routes.
- Process only the new or changed source files listed below unless I explicitly ask for a broader reprocess.
- Update Research OS documents directly: source representations, evidence observations, patterns, insights, recommendations and review queue where needed.
- Keep review decisions pending in the web UI.
- After processing, update `{STATE_FILE}` for the processed source checksums and add a run entry with status `codex-complete`.
- Report what changed and what still needs review.

New or changed sources:
{source_lines}
"""


def project_codex_processing_prompt(project_dir: Path, sources: list[dict]) -> str:
    project_rel = rel(project_dir)
    source_lines = "\n".join(f"- {source['id']}: {rel(source['path'])}" for source in sources) or "- No changed project sources detected."
    return f"""Process this Research OS project input in Codex/Cowork, not through the backend pipeline:
{project_rel}

Rules:
- Do not call OpenAI APIs.
- Do not run local stub generation.
- Do not make review decisions for me.
- Read and apply active Looped Learnings from `{rel(LOOPED_ACTIVE_FILE)}`.
- Read the existing project context, current understanding, project source representations and project context proposal queue.
- Process only the new or changed project-level source files listed below unless I explicitly ask for a broader reprocess.
- Update Research OS documents directly: project source representations and project context proposals where needed.
- Keep proposed project context as pending reviews in the web UI.
- After processing, update `{PROJECT_STATE_FILE}` for the processed source checksums and add a run entry with status `codex-complete`.
- Report what changed and what still needs review.

New or changed project sources:
{source_lines}
"""


def markdown_blocks_for_heading(path: Path, pattern: str) -> list[tuple[str, str]]:
    if not path.exists():
        return []
    try:
        text = read_text(path)
    except UnicodeDecodeError:
        return []
    matches = list(re.finditer(pattern, text, flags=re.MULTILINE | re.IGNORECASE))
    blocks: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        blocks.append((match.group(1), text[start:end]))
    return blocks


def evidence_ids_in(text: str) -> list[str]:
    return sorted(set(re.findall(r"\bEV-[A-Z]+(?:-[A-Z]+)*-\d{3}\b", text, flags=re.IGNORECASE)))


def pattern_ids_in(text: str) -> list[str]:
    return sorted(set(re.findall(r"\bPAT-\d{3}\b", text, flags=re.IGNORECASE)))


def insight_ids_in(text: str) -> list[str]:
    return sorted(set(re.findall(r"\bINS-\d{3}\b", text, flags=re.IGNORECASE)))


def recommendation_ids_in(text: str) -> list[str]:
    return sorted(set(re.findall(r"\bREC-\d{3}\b", text, flags=re.IGNORECASE)))


def weak_reference(value: str) -> bool:
    clean = value.strip().lower()
    return not clean or clean in {"none", "n/a", "not assessed yet", "not assessed", "-"}


def quality_gate_waiver_path(round_dir: Path) -> Path:
    return round_dir / QUALITY_GATE_WAIVERS_FILE


def quality_gate_key(stage: str, gate_id: str) -> str:
    return f"{stage}:{gate_id}"


def load_quality_gate_waivers(round_dir: Path) -> dict:
    path = quality_gate_waiver_path(round_dir)
    if not path.exists():
        return {"waivers": {}}
    try:
        data = json.loads(read_text(path))
    except (json.JSONDecodeError, OSError):
        return {"waivers": {}}
    if not isinstance(data, dict):
        return {"waivers": {}}
    waivers = data.get("waivers")
    if not isinstance(waivers, dict):
        data["waivers"] = {}
    return data


def save_quality_gate_waivers(round_dir: Path, data: dict) -> None:
    if not isinstance(data.get("waivers"), dict):
        data["waivers"] = {}
    write_text(quality_gate_waiver_path(round_dir), json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def waive_quality_gate(round_dir: Path, stage: str, gate_id: str, message: str = "", reason: str = "") -> None:
    allowed_stages = {"evidence", "patterns", "insights", "recommendations"}
    if stage not in allowed_stages:
        raise ValueError(f"Unsupported quality gate stage: {stage}")
    if not gate_id:
        raise ValueError("Missing quality gate id")
    data = load_quality_gate_waivers(round_dir)
    data.setdefault("waivers", {})[quality_gate_key(stage, gate_id)] = {
        "stage": stage,
        "id": gate_id,
        "message": message,
        "reason": reason or "Accepted by reviewer.",
        "waived_at": now().isoformat(),
    }
    save_quality_gate_waivers(round_dir, data)


def apply_quality_gate_waivers(round_dir: Path, gates: dict) -> dict:
    waivers = load_quality_gate_waivers(round_dir).get("waivers", {})
    if not waivers:
        return gates
    filtered: dict[str, list[dict]] = {}
    for stage, issues in gates.items():
        filtered[stage] = [
            issue
            for issue in issues
            if quality_gate_key(stage, str(issue.get("id", ""))) not in waivers
        ]
    return filtered


def quality_gate_cache_path(round_dir: Path) -> Path:
    return round_dir / QUALITY_GATE_CACHE_FILE


def quality_gate_signature(round_dir: Path, source_total: int, evidence_total: int) -> dict:
    paths = [
        round_path(round_dir, "evidence") / "evidence.md",
        round_path(round_dir, "patterns") / "patterns.md",
        round_path(round_dir, "insights") / "insights.md",
        round_path(round_dir, "recommendations") / "recommendations.md",
        quality_gate_waiver_path(round_dir),
    ]
    return {
        "rule_version": QUALITY_GATE_RULE_VERSION,
        "source_total": source_total,
        "evidence_total": evidence_total,
        "files": files_signature(paths),
    }


def round_quality_gates(round_dir: Path, source_total: int = 0, evidence_total: int = 0) -> dict:
    signature = quality_gate_signature(round_dir, source_total, evidence_total)
    cache_path = quality_gate_cache_path(round_dir)
    if cache_path.exists():
        try:
            cached = json.loads(read_text(cache_path))
            if cached.get("signature") == signature and isinstance(cached.get("gates"), dict):
                return cached["gates"]
        except (json.JSONDecodeError, OSError):
            pass
    gates = {"evidence": [], "patterns": [], "insights": [], "recommendations": []}
    evidence_path = round_path(round_dir, "evidence") / "evidence.md"
    pattern_path = round_path(round_dir, "patterns") / "patterns.md"
    insight_path = round_path(round_dir, "insights") / "insights.md"
    recommendation_path = round_path(round_dir, "recommendations") / "recommendations.md"

    evidence_id_pattern = r"EV-[A-Z]+(?:-[A-Z]+)*-\d{3}"
    evidence_blocks = markdown_blocks_for_heading(evidence_path, rf"^###\s+({evidence_id_pattern})\s*$")
    if source_total and evidence_total and evidence_total < source_total * 8:
        gates["evidence"].append(
            {
                "id": "EV-COVERAGE",
                "message": f"Only {evidence_total} evidence items across {source_total} sources. Check whether extraction missed smaller observations.",
            }
        )
    for item_id, block in evidence_blocks:
        if weak_reference(markdown_field(block, "Source reference")):
            gates["evidence"].append({"id": item_id, "message": "AI will add or repair the source reference before this Evidence is used downstream."})
        if weak_reference(markdown_field(block, "Source")):
            gates["evidence"].append({"id": item_id, "message": "AI will add the missing source document before this Evidence is used downstream."})
        if weak_reference(markdown_field(block, "Helps us understand", "Interpretation note")):
            gates["evidence"].append({"id": item_id, "message": "AI will clarify what this Evidence helps us understand."})
        if len(markdown_field(block, "Observation").split()) > 45:
            gates["evidence"].append({"id": item_id, "message": "AI will check whether this observation combines too many ideas and should be split or tightened. No researcher action is needed unless Codex flags it for judgment."})

    active_evidence_ids = [
        item_id
        for item_id, block in evidence_blocks
        if not markdown_field(block, "Status").strip().lower().startswith("rejected")
    ]
    pattern_text = read_text(pattern_path) if pattern_path.exists() else ""
    pattern_evidence_ids = set(evidence_ids_in(pattern_text))
    unsynthesized_evidence = [item_id for item_id in active_evidence_ids if item_id not in pattern_evidence_ids]
    if active_evidence_ids and unsynthesized_evidence:
        preview = ", ".join(unsynthesized_evidence[:8])
        more = len(unsynthesized_evidence) - 8
        suffix = f", plus {more} more" if more > 0 else ""
        gates["patterns"].append(
            {
                "id": "PAT-SYNTHESIS-STALE",
                "message": f"New accepted/curated Evidence has been processed but not synthesized yet. {len(unsynthesized_evidence)} Evidence items are not referenced by Patterns yet ({preview}{suffix}). Run synthesis next so Research OS can update Patterns, propose new or changed Insights, update Recommendations, and mark downstream Deliverables stale if needed.",
            }
        )

    for item_id, block in markdown_blocks_for_heading(pattern_path, r"^###\s+(PAT-\d{3})\s*$"):
        ids = evidence_ids_in(" ".join([markdown_field(block, "Supporting Evidence", "Evidence"), block]))
        if len(ids) < 2:
            gates["patterns"].append({"id": item_id, "message": "Pattern has fewer than 2 supporting evidence items."})
        if weak_reference(markdown_field(block, "Contradicting Evidence")):
            gates["patterns"].append({"id": item_id, "message": "Contradicting evidence is missing or not assessed."})
        if weak_reference(markdown_field(block, "Helps us understand")):
            gates["patterns"].append({"id": item_id, "message": "Missing what this pattern helps us understand."})

    for item_id, block in markdown_blocks_for_heading(insight_path, r"^###\s+(INS-\d{3})\s*$"):
        if not pattern_ids_in(markdown_field(block, "Supporting Patterns", "Based on Patterns")):
            gates["insights"].append({"id": item_id, "message": "Insight is not linked to supporting patterns."})
        if not evidence_ids_in(markdown_field(block, "Supporting Evidence")):
            gates["insights"].append({"id": item_id, "message": "Insight is not linked back to evidence."})
        if weak_reference(markdown_field(block, "Contradicting Evidence")):
            gates["insights"].append({"id": item_id, "message": "Contradicting evidence is missing or not assessed."})
        if weak_reference(markdown_field(block, "Assumptions")) and weak_reference(markdown_field(block, "Open Questions")):
            gates["insights"].append({"id": item_id, "message": "Missing assumptions or open questions."})
        if weak_reference(markdown_field(block, "Helps us understand")):
            gates["insights"].append({"id": item_id, "message": "Missing what this insight helps us understand."})
        if len(markdown_field(block, "Insight").split()) < 12:
            gates["insights"].append({"id": item_id, "message": "Insight may be too compressed to stand alone."})

    for item_id, block in markdown_blocks_for_heading(recommendation_path, r"^###\s+(REC-\d{3})\s*$"):
        if weak_reference(markdown_field(block, "What we learned", "Learned")):
            gates["recommendations"].append({"id": item_id, "message": "Missing 'What we learned'."})
        if weak_reference(markdown_field(block, "What we should do", "Recommendation")):
            gates["recommendations"].append({"id": item_id, "message": "Missing 'What we should do'."})
        if not any(
            [
                evidence_ids_in(markdown_field(block, "Based on", "Supporting Evidence")),
                pattern_ids_in(markdown_field(block, "Based on", "Based on Patterns")),
                insight_ids_in(markdown_field(block, "Based on", "Based on Insights")),
            ]
        ):
            gates["recommendations"].append({"id": item_id, "message": "Recommendation is not linked to Evidence, Patterns or Insights."})
        if weak_reference(markdown_field(block, "Confidence")):
            gates["recommendations"].append({"id": item_id, "message": "Missing confidence."})

    gates = apply_quality_gate_waivers(round_dir, gates)
    write_json_if_changed(cache_path, {"signature": signature, "gates": gates, "updated_at": now().isoformat()})
    return gates


def apply_stage_quality_gates(stage: dict, issues: list[dict]) -> dict:
    stage["gates"] = len(issues)
    stage["gate_issues"] = issues[:6]
    if issues and stage.get("status") == "green":
        stage["status"] = "yellow"
        stage["label"] = f"{len(issues)} checks need attention"
    return stage


def write_json_if_changed(path: Path, payload: dict) -> None:
    content = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if path.exists():
        try:
            if read_text(path) == content:
                return
        except UnicodeDecodeError:
            pass
    write_text(path, content)


def file_signature(path: Path) -> dict:
    if not path.exists() or not path.is_file():
        return {"exists": False, "size": 0, "mtime": 0}
    try:
        stat = path.stat()
    except OSError:
        return {"exists": False, "size": 0, "mtime": 0}
    return {"exists": True, "size": stat.st_size, "mtime": int(stat.st_mtime)}


def files_signature(paths: Iterable[Path]) -> dict:
    return {rel(path): file_signature(path) for path in sorted(set(paths), key=lambda value: str(value))}


def invalidate_dashboard_cache() -> None:
    DASHBOARD_PAYLOAD_CACHE["payload"] = None
    DASHBOARD_PAYLOAD_CACHE["created_at"] = 0.0


def build_round_dashboard(round_dir: Path) -> dict:
    lens = selected_research_lens(round_dir)
    state = load_state(round_dir)
    source_dir = round_path(round_dir, "sources")
    source_items = source_inventory(source_dir)
    source_total = len(source_items)
    monitored = round_is_monitored(round_dir)
    if not monitored:
        deliverable_items = deliverable_dashboard_items(round_path(round_dir, "deliverables"))
        deliverable_files = sum(1 for item in deliverable_items if item.get("exists"))
        deliverable_ready_count = sum(1 for item in deliverable_items if item.get("status") == "green")
        deliverables_stage = enrich_stage_progress(stage_status(round_path(round_dir, "deliverables")), len(deliverable_items), deliverable_ready_count, "deliverable")
        deliverables_stage["items"] = deliverable_items
        deliverables_stage["generated"] = deliverable_files
        deliverables_stage["ready"] = deliverable_ready_count
        payload = {
            "type": "round",
            "id": round_dir.name,
            "name": read_title(round_file(round_dir, "overview"), round_dir.name),
            "path": rel(round_dir),
            "status": "gray",
            "monitored": False,
            "project_context": {"present": context_present(round_dir)},
            "research_lens": lens,
            "research_lenses": available_research_lenses(),
            "source_files": {"total": source_total, "waiting": 0, "waiting_items": []},
            "review": {"pending_items": 0},
            "quality_gates": {},
            "latest_run": latest_run(state),
            "stages": {"deliverables": deliverables_stage},
            "updated_at": now().isoformat(),
        }
        write_json_if_changed(round_dir / "status.json", payload)
        return payload

    ensure_round_recommendations_scaffold(round_dir)
    waiting = waiting_sources(source_dir, state, source_items)
    source_processed = max(source_total - len(waiting), 0)
    evidence_total = markdown_heading_count(round_path(round_dir, "evidence"), r"^###\s+EV-[A-Z]+(?:-[A-Z]+)*-\d{3}\b")
    pattern_total = markdown_heading_count(round_path(round_dir, "patterns"), r"^###\s+PAT-\d{3}\b")
    insight_total = markdown_heading_count(round_path(round_dir, "insights"), r"^###\s+INS-\d{3}\b")
    recommendation_total = markdown_heading_count(round_path(round_dir, "recommendations"), r"^###\s+REC-\d{3}\b")
    deliverable_items = deliverable_dashboard_items(round_path(round_dir, "deliverables"))
    deliverable_files = sum(1 for item in deliverable_items if item.get("exists"))
    deliverable_open_count = sum(int(item.get("review") or 0) for item in deliverable_items if item.get("exists") and item.get("status") == "yellow")
    deliverable_ready_count = sum(1 for item in deliverable_items if item.get("status") == "green")
    review_dir = round_path(round_dir, "reviews")
    review_count = pending_markdown_items(review_dir)
    review_stage_counts = pending_review_stage_counts(review_dir)
    evidence_review_count = review_stage_counts.get("evidence", 0)
    pattern_review_count = review_stage_counts.get("patterns", 0)
    insight_review_count = review_stage_counts.get("insights", 0)
    recommendation_review_count = review_stage_counts.get("recommendations", 0)
    quality_gates = round_quality_gates(round_dir, source_total=source_total, evidence_total=evidence_total)
    stages = {
        "sources": enrich_stage_progress(stage_status(source_dir, waiting_count=len(waiting)), source_total, source_processed, "source"),
        "representations": enrich_stage_progress(stage_status(round_path(round_dir, "representations"), waiting_count=len(waiting)), source_total, source_processed, "source"),
        "evidence": enrich_stage_progress(stage_status(round_path(round_dir, "evidence"), review_count=evidence_review_count), evidence_total, max(evidence_total - evidence_review_count, 0), "evidence item"),
        "patterns": enrich_stage_progress(stage_status(round_path(round_dir, "patterns"), review_count=pattern_review_count), pattern_total, max(pattern_total - pattern_review_count, 0), "pattern"),
        "insights": enrich_stage_progress(stage_status(round_path(round_dir, "insights"), review_count=insight_review_count), insight_total, max(insight_total - insight_review_count, 0), "insight"),
        "recommendations": enrich_stage_progress(stage_status(round_path(round_dir, "recommendations"), review_count=recommendation_review_count), recommendation_total, max(recommendation_total - recommendation_review_count, 0), "recommendation"),
        "reviews": stage_status(review_dir, review_count=review_count),
        "deliverables": enrich_stage_progress(stage_status(round_path(round_dir, "deliverables"), review_count=deliverable_open_count), len(deliverable_items), deliverable_ready_count, "deliverable"),
    }
    stages["deliverables"]["items"] = deliverable_items
    stages["deliverables"]["generated"] = deliverable_files
    stages["deliverables"]["ready"] = deliverable_ready_count
    for key in ("evidence", "patterns", "insights", "recommendations"):
        apply_stage_quality_gates(stages[key], quality_gates.get(key, []))
    for key, stage in stages.items():
        stage["action"] = round_stage_action(round_dir, key, stage)
    payload = {
        "type": "round",
        "id": round_dir.name,
        "name": read_title(round_file(round_dir, "overview"), round_dir.name),
        "path": rel(round_dir),
        "status": worst_status(stage["status"] for stage in stages.values()),
        "monitored": True,
        "project_context": {"present": context_present(round_dir)},
        "research_lens": lens,
        "research_lenses": available_research_lenses(),
        "source_files": {"total": source_total, "waiting": len(waiting), "waiting_items": waiting[:8]},
        "review": {"pending_items": review_count},
        "quality_gates": quality_gates,
        "latest_run": latest_run(state),
        "stages": stages,
        "updated_at": now().isoformat(),
    }
    write_json_if_changed(round_dir / "status.json", payload)
    return payload


def build_project_dashboard(project_dir: Path) -> dict:
    ensure_project_input_scaffold(project_dir)
    state = load_project_state(project_dir)
    source_dir = project_path(project_dir, "sources")
    project_sources = source_inventory(source_dir)
    waiting = waiting_sources(source_dir, state, project_sources)
    project_review_count = pending_markdown_items(project_path(project_dir, "reviews"))
    rounds_dir = project_path(project_dir, "rounds")
    rounds = []
    if rounds_dir.exists():
        for round_dir in sorted((path for path in rounds_dir.iterdir() if path.is_dir()), reverse=True):
            if (round_file(round_dir, "overview")).exists():
                rounds.append(build_round_dashboard(round_dir))
    monitored_rounds = [round_item for round_item in rounds if round_item.get("monitored", True)]
    background_present = project_background_present(project_dir)
    project_needs_context_attention = bool(waiting) or (not monitored_rounds and not background_present)
    project_context_status = "yellow" if project_needs_context_attention else ("green" if project_sources else "gray")
    review_status = "yellow" if project_review_count else "green"
    active_statuses = [project_context_status, review_status]
    if monitored_rounds:
        active_statuses.extend(round_item["status"] for round_item in monitored_rounds)
    payload = {
        "type": "project",
        "id": project_dir.name,
        "name": read_title(project_file(project_dir, "overview"), project_dir.name),
        "path": rel(project_dir),
        "status": worst_status(active_statuses),
        "monitored": bool(monitored_rounds) or project_needs_context_attention or bool(project_review_count),
        "project_context": {
            "status": project_context_status,
            "files_total": len(project_sources),
            "files_processed": max(len(project_sources) - len(waiting), 0),
            "files_waiting": len(waiting),
            "waiting_items": waiting[:8],
            "latest_run": latest_run(state),
            "background_present": background_present,
            "background_action": project_action(project_dir, "background"),
            "action": project_action(project_dir, "context"),
        },
        "review": {"status": review_status, "pending_items": project_review_count, "action": project_action(project_dir, "reviews")},
        "last_round": rounds[0]["id"] if rounds else None,
        "rounds": rounds,
        "updated_at": now().isoformat(),
    }
    write_json_if_changed(project_dir / "status.json", payload)
    return payload


def build_dashboard_payload_uncached() -> dict:
    projects_root = projects_dir()
    projects = []
    current_update_status = update_status()
    if projects_root.exists():
        for project_dir in sorted(path for path in projects_root.iterdir() if path.is_dir() and not path.name.startswith(".")):
            if (project_file(project_dir, "overview")).exists():
                projects.append(build_project_dashboard(project_dir))
    return {
        "name": "Research OS",
        "generated_at": now().isoformat(),
        "refresh_seconds": dashboard_refresh_seconds(),
        "projects": projects,
        "looped_learning": looped_learning_metrics(),
        "settings": dashboard_settings_payload(),
        "update_status": current_update_status,
        "summary": {
            "projects": len(projects),
            "waiting_files": sum(project["project_context"]["files_waiting"] + sum(round_item["source_files"]["waiting"] for round_item in project["rounds"]) for project in projects),
            "pending_reviews": sum(project["review"]["pending_items"] + sum(round_item["review"]["pending_items"] for round_item in project["rounds"]) for project in projects),
        },
    }


def build_dashboard_payload() -> dict:
    cached = DASHBOARD_PAYLOAD_CACHE.get("payload")
    created_at = float(DASHBOARD_PAYLOAD_CACHE.get("created_at") or 0.0)
    if cached is not None and time.monotonic() - created_at < DASHBOARD_CACHE_SECONDS:
        return cached  # type: ignore[return-value]
    payload = build_dashboard_payload_uncached()
    DASHBOARD_PAYLOAD_CACHE["payload"] = payload
    DASHBOARD_PAYLOAD_CACHE["created_at"] = time.monotonic()
    return payload


def backup_status() -> dict:
    settings = load_dashboard_settings()
    if not settings.get("backup_enabled"):
        return {"status": "disabled", "enabled": False, "last_backup_at": "", "started_at": "", "message": "iCloud backup is off.", "backup_dir": settings["backup_dir"]}
    if not BACKUP_STATUS_FILE.exists():
        return {"status": "never", "enabled": True, "last_backup_at": "", "started_at": "", "message": "Not backed up yet.", "backup_dir": settings["backup_dir"]}
    try:
        data = json.loads(read_text(BACKUP_STATUS_FILE))
    except json.JSONDecodeError:
        return {"status": "unknown", "enabled": True, "last_backup_at": "", "started_at": "", "message": "Backup status could not be read.", "backup_dir": settings["backup_dir"]}
    return {
        "status": data.get("status", "unknown"),
        "enabled": True,
        "last_backup_at": data.get("last_backup_at", ""),
        "started_at": data.get("started_at", ""),
        "finished_at": data.get("finished_at", ""),
        "message": data.get("message", ""),
        "backup_dir": settings["backup_dir"],
    }


def write_backup_status(payload: dict) -> None:
    write_text(BACKUP_STATUS_FILE, json.dumps(payload, indent=2, sort_keys=True) + "\n")


def backup_running_is_fresh(current: dict) -> bool:
    if current.get("status") != "running" or not current.get("started_at"):
        return False
    try:
        started = datetime.fromisoformat(current["started_at"])
    except ValueError:
        return False
    return now() - started < timedelta(minutes=2)


def start_backup_to_icloud() -> dict:
    current = backup_status()
    settings = load_dashboard_settings()
    if not settings.get("backup_enabled"):
        return current
    backup_dir = Path(settings["backup_dir"]).expanduser()
    if backup_running_is_fresh(current):
        return current
    if not BACKUP_SCRIPT.exists():
        payload = {"status": "error", "last_backup_at": current.get("last_backup_at", ""), "message": "Backup script is missing."}
        write_backup_status(payload)
        return payload
    started_at = now().isoformat()
    payload = {
        "status": "running",
        "started_at": started_at,
        "last_backup_at": current.get("last_backup_at", ""),
        "message": f"Backup started: {backup_dir}",
    }
    write_backup_status(payload)
    try:
        env = {
            **os.environ,
            "RESEARCH_OS_BACKUP_DIR": str(backup_dir),
            "RESEARCH_OS_PROJECTS_DIR": str(projects_dir()),
        }
        subprocess.Popen([str(BACKUP_SCRIPT), str(backup_dir)], cwd=str(ROOT), env=env)
    except Exception as exc:
        payload = {
            "status": "error",
            "started_at": started_at,
            "finished_at": now().isoformat(),
            "last_backup_at": current.get("last_backup_at", ""),
            "message": str(exc),
        }
        write_backup_status(payload)
    return payload


def resolve_dashboard_file(path_value: str) -> Path:
    requested = resolve_research_path(Path(path_value))
    allowed_roots = [ROOT.resolve(), projects_dir().resolve()]
    if not any(_is_relative_to(requested, root) for root in allowed_roots):
        raise PermissionError("Path is outside Research OS or Projects.")
    return requested


def dashboard_display_title(target: Path) -> str:
    if target.resolve() == LOOPED_SUGGESTIONS_FILE.resolve():
        return "Research OS - Looped Learning Suggestions"
    if target.name == "review-queue.md":
        round_dir = target.parents[1]
        project_dir = round_dir.parents[1]
        project_name = read_title(project_file(project_dir, "overview"), project_dir.name)
        round_name = read_title(round_file(round_dir, "overview"), round_dir.name)
        return f"{project_name} - {round_name} - Review Queue"
    if target.name == "project-context-proposals.md":
        project_dir = target.parents[1]
        project_name = read_title(project_file(project_dir, "overview"), project_dir.name)
        return f"{project_name} - Project Reviews"
    if target.is_dir():
        return title_from_slug(target.name)
    return title_from_slug(target.stem)


def is_deliverable_markdown(target: Path) -> bool:
    return target.is_file() and target.suffix.lower() == ".md" and target.parent.name in ROUND_DIRS["deliverables"]


def deliverable_review_path(target: Path) -> Path:
    return target.parent / ".deliverable-reviews.json"


def load_deliverable_reviews(target: Path) -> dict:
    review_path = deliverable_review_path(target)
    if not review_path.exists():
        return {"sections": {}}
    try:
        root_data = json.loads(read_text(review_path))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {"sections": {}}
    if not isinstance(root_data, dict):
        return {"sections": {}}
    if "deliverables" in root_data and isinstance(root_data.get("deliverables"), dict):
        data = root_data["deliverables"].get(target.name, {})
    else:
        data = root_data if target.name == "research-summary.md" else {}
    if not isinstance(data, dict):
        data = {}
    data.setdefault("sections", {})
    return data


def save_deliverable_reviews(target: Path, data: dict) -> None:
    data.setdefault("sections", {})
    review_path = deliverable_review_path(target)
    root_data: dict = {}
    if review_path.exists():
        try:
            loaded = json.loads(read_text(review_path))
            if isinstance(loaded, dict):
                root_data = loaded
        except (json.JSONDecodeError, UnicodeDecodeError):
            root_data = {}
    if "deliverables" not in root_data or not isinstance(root_data.get("deliverables"), dict):
        migrated = root_data if root_data else {"sections": {}}
        root_data = {"deliverables": {"research-summary.md": migrated}}
    root_data.setdefault("deliverables", {})[target.name] = data
    write_text(review_path, json.dumps(root_data, indent=2, ensure_ascii=False) + "\n")


def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def post_it_note_sections(text: str) -> list[dict]:
    sections = []
    current_context = "General"
    for line in text.splitlines():
        heading = re.match(r"^##\s+(.+)$", line)
        if heading:
            current_context = heading.group(1).strip()
            continue
        note = re.match(r"^\s*([+\-0])\s+(.+)$", line)
        if not note:
            continue
        tone = {"+": "Positive", "-": "Negative", "0": "Neutral"}.get(note.group(1), "Note")
        note_text = note.group(2).strip()
        label_match = re.match(r"^\[([^\]]+)\]\s+(.+)$", note_text)
        display_context = label_match.group(1).strip() if label_match else current_context
        raw_note = f"{note.group(1)} {note_text}" if label_match else f"{note.group(1)} [{current_context}] {note_text}"
        sections.append(
            {
                "id": f"DSEC-{len(sections) + 1:03d}",
                "title": f"{display_context} · {tone}",
                "level": 2,
                "content": f"```\n{raw_note}\n```",
            }
        )
    if sections:
        return sections
    return deliverable_heading_sections(text)


def deliverable_heading_sections(text: str) -> list[dict]:
    matches = list(re.finditer(r"^(#{1,3})\s+(.+)$", text, flags=re.MULTILINE))
    if not matches:
        return [{"id": "DSEC-001", "title": "Full deliverable", "level": 1, "content": text.strip()}]
    sections = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.append(
            {
                "id": f"DSEC-{index + 1:03d}",
                "title": match.group(2).strip(),
                "level": len(match.group(1)),
                "content": text[match.end() : end].strip(),
            }
        )
    return sections


def deliverable_sections(text: str, target: Path | None = None) -> list[dict]:
    if target and target.name == "post-it-notes.md":
        return post_it_note_sections(text)
    return deliverable_heading_sections(text)


def changed_line_numbers(previous: str, current: str) -> list[int]:
    remaining: dict[str, int] = {}
    for line in previous.splitlines():
        key = line.strip()
        if key:
            remaining[key] = remaining.get(key, 0) + 1
    changed = []
    for index, line in enumerate(current.splitlines(), start=1):
        key = line.strip()
        if not key:
            continue
        if remaining.get(key, 0):
            remaining[key] -= 1
        else:
            changed.append(index)
    return changed


def sync_deliverable_review_state(target: Path, sections: list[dict]) -> dict:
    data = load_deliverable_reviews(target)
    data.setdefault("sections", {})
    data.setdefault("history", [])
    data.setdefault("section_snapshots", {})
    data.setdefault("changed_sections", {})
    changed = False
    snapshots = data["section_snapshots"]
    changed_sections = data["changed_sections"]
    for section in sections:
        section_id = section["id"]
        current_content = section.get("content", "")
        current_hash = content_hash(current_content)
        previous = snapshots.get(section_id, {})
        previous_hash = previous.get("hash", "")
        if previous_hash and previous_hash != current_hash:
            changed_sections[section_id] = {
                "from_hash": previous_hash,
                "to_hash": current_hash,
                "changed_at": now().isoformat(),
                "changed_lines": changed_line_numbers(previous.get("content", ""), current_content),
            }
            section_review = data["sections"].get(section_id, {})
            if section_review.get("status") == "Looks good" and not str(section_review.get("notes", "")).strip():
                data["sections"][section_id] = {
                    "status": "",
                    "notes": "",
                    "updated_at": now().isoformat(),
                    "reset_reason": "Section changed after previous approval.",
                }
            changed = True
        if previous_hash != current_hash or previous.get("title") != section.get("title", ""):
            snapshots[section_id] = {
                "hash": current_hash,
                "title": section.get("title", ""),
                "content": current_content,
                "seen_at": now().isoformat(),
            }
            changed = True
    valid_ids = {section["id"] for section in sections}
    for key in list(snapshots.keys()):
        if key not in valid_ids:
            snapshots.pop(key, None)
            changed_sections.pop(key, None)
            changed = True
    if changed:
        save_deliverable_reviews(target, data)
    return data


def simple_markdown_html_with_highlights(text: str, changed_lines: list[int]) -> str:
    if not changed_lines:
        return simple_markdown_html(text)
    changed = set(changed_lines)
    html_lines = []
    in_list = False
    list_tag = "ul"
    for index, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.rstrip()
        if not line.strip():
            if in_list:
                html_lines.append(f"</{list_tag}>")
                in_list = False
            continue
        marker = " changed-line" if index in changed else ""
        heading = re.match(r"^(#{1,4})\s+(.+)$", line)
        if heading:
            if in_list:
                html_lines.append(f"</{list_tag}>")
                in_list = False
            level = min(len(heading.group(1)) + 1, 5)
            html_lines.append(f'<h{level} class="{marker.strip()}">{inline_markdown_html(heading.group(2))}</h{level}>')
            continue
        bullet = re.match(r"^[-*]\s+(.+)$", line)
        if bullet:
            if in_list and list_tag != "ul":
                html_lines.append(f"</{list_tag}>")
                in_list = False
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
                list_tag = "ul"
            html_lines.append(f'<li class="{marker.strip()}">{inline_markdown_html(bullet.group(1))}</li>')
            continue
        ordered = re.match(r"^\d+\.\s+(.+)$", line)
        if ordered:
            if in_list and list_tag != "ol":
                html_lines.append(f"</{list_tag}>")
                in_list = False
            if not in_list:
                html_lines.append("<ol>")
                in_list = True
                list_tag = "ol"
            html_lines.append(f'<li class="{marker.strip()}">{inline_markdown_html(ordered.group(1))}</li>')
            continue
        nested_bullet = re.match(r"^\s+[-*]\s+(.+)$", line)
        if nested_bullet:
            html_lines.append(f'<div class="nested-bullet{marker}">{inline_markdown_html(nested_bullet.group(1))}</div>')
            continue
        if in_list:
            html_lines.append(f"</{list_tag}>")
            in_list = False
        html_lines.append(f'<p class="{marker.strip()}">{inline_markdown_html(line)}</p>')
    if in_list:
        html_lines.append(f"</{list_tag}>")
    return "\n".join(html_lines)


def deliverable_review_count(deliverables_dir: Path) -> int:
    count = 0
    cache: dict[str, dict] = {}
    for file_path in non_empty_files(deliverables_dir):
        if file_path.suffix.lower() != ".md" or file_path.name == "README.md" or file_path.name in NON_REVIEWABLE_DELIVERABLES:
            continue
        count += deliverable_file_review_count(file_path, cache)
    return count


def deliverable_file_review_count(file_path: Path, cache: dict[str, dict] | None = None) -> int:
    if cache is not None:
        return int(deliverable_file_review_summary(file_path, cache)["review"])
    return int(deliverable_file_review_summary(file_path, {})["review"])


def deliverable_file_review_summary(file_path: Path, cache: dict[str, dict]) -> dict:
    cache_key = str(file_path.resolve())
    if cache_key in cache:
        return cache[cache_key]
    if file_path.name in NON_REVIEWABLE_DELIVERABLES:
        summary = {"review": 0, "status": "green" if file_path.exists() else "gray", "status_label": "ready to copy" if file_path.exists() else "not generated"}
        cache[cache_key] = summary
        return summary
    if not file_path.exists():
        summary = {"review": 0, "status": "gray", "status_label": "not generated"}
        cache[cache_key] = summary
        return summary
    if file_path.suffix.lower() != ".md":
        summary = {"review": 0, "status": "yellow", "status_label": "generated"}
        cache[cache_key] = summary
        return summary
    data = load_deliverable_reviews(file_path)
    sections = deliverable_sections(read_text(file_path), file_path)
    changed_sections = data.get("changed_sections", {})
    active_count = sum(
        1
        for section in data.get("sections", {}).values()
        if str(section.get("status", "")).lower() in {"needs review", "pending review", "needs changes", "revise", "do not use"} or str(section.get("notes", "")).strip()
    )
    changed_count = sum(
        1
        for section in sections
        if section["id"] in changed_sections
        and not (
            data.get("sections", {}).get(section["id"], {}).get("status") == "Looks good"
            and not str(data.get("sections", {}).get(section["id"], {}).get("notes", "")).strip()
        )
    )
    review = active_count + changed_count
    if review:
        status, status_label = "yellow", "Start review"
    else:
        reviews = data.get("sections", {})
        if sections and all(
            reviews.get(section["id"], {}).get("status") == "Looks good"
            and not str(reviews.get(section["id"], {}).get("notes", "")).strip()
            and section["id"] not in changed_sections
            for section in sections
        ):
            status, status_label = "green", "reviewed"
        else:
            status, status_label = "yellow", "start review"
    summary = {"review": review, "status": status, "status_label": status_label}
    cache[cache_key] = summary
    return summary


def deliverable_file_review_status(file_path: Path, cache: dict[str, dict] | None = None) -> tuple[str, str]:
    summary = deliverable_file_review_summary(file_path, cache if cache is not None else {})
    return str(summary["status"]), str(summary["status_label"])


def copyable_prompt_text(text: str) -> str:
    match = re.search(r"^##\s+Prompt\s*$", text, flags=re.MULTILINE)
    if match:
        return text[match.end() :].strip()
    return text.strip()


def copyable_post_it_text(text: str) -> str:
    notes = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(("+ ", "- ", "0 ")):
            notes.append(stripped)
    return "\n".join(notes).strip()


def post_it_notes_prompt(deliverables_dir: Path, mode: str = "prepare") -> dict:
    round_dir = deliverables_dir.parent
    lens_block = research_lens_prompt_block(round_dir)
    action_verb = "Update" if mode == "smart" else ("Revise" if mode == "revise" else "Prepare")
    return {
        "label": f"{action_verb} post-it notes",
        "button_label": action_verb,
        "copy_label": DELIVERABLE_COPY_LABELS["post-it-notes"],
        "instruction": "Smart post-it workflow: draft notes, apply completed review decisions, or confirm final copy depending on current state.",
        "prompt_description": "Codex handles the next safe post-it step: draft missing notes, apply completed reviews, keep only flagged notes active, or confirm approved notes are final.",
        "prompt": f"""Smart process optional reviewable Figma workshop post-it notes for this Research OS round in Codex/Cowork: {rel(round_dir)}.

First read Research OS/08-looped-learning/active-learnings.md and apply any active Looped Learnings.
{lens_block}
Read accepted Evidence, Patterns, Insights and Recommendations for this round. Use source detail when needed, but do not create new Evidence or review decisions.

Use exactly this Markdown deliverable:
{rel(deliverables_dir / "post-it-notes.md")}

Purpose:
This deliverable is for copying insight notes into a Figma/FigJam workshop board. It is not a report.

Smart workflow:
- If `post-it-notes.md` does not exist yet, draft it from accepted research knowledge using the format rules below.
- If `post-it-notes.md` exists, first read {rel(deliverable_review_path(deliverables_dir / "post-it-notes.md"))} if it exists and apply completed review decisions before creating or changing notes.
- If existing post-it reviews include completed `Do not use` decisions, remove those exact post-it lines from the Markdown and then re-sync the review state against the remaining post-it text so approved notes remain `Looks good`.
- If existing post-it reviews include `Needs changes` notes, revise only those flagged post-it lines, preserve unchanged `Looks good` notes, and leave revised notes pending for another review pass.
- If every active remaining note is already `Looks good` with no notes/comments and there are no changed sections, do not rewrite the Markdown. Report that the post-it notes are approved and ready as final Figma/FigJam copyable notes.

Format rules:
- Group notes by source-derived context labels such as screen, feature, workflow, concept area or moment. Derive labels from the round material and normalize similar labels so the list stays usable.
- Under each context heading, write one post-it per line.
- Every post-it must start with one of these markers:
  - + for positive insight
  - - for negative insight
  - 0 for neutral insight, tension, trade-off or conditional insight
- Include the context label in the note line using this pattern: `- [Context label] Insight text`.
- Do not include participant names, source IDs or evidence IDs in the note text. Keep traceability in Research OS, not on the Figma notes.
- Each note should be short, but it must stand alone. It should explain what happens and why it matters. One sentence is preferred; two short sentences are allowed when needed.
- Notes may summarize multiple participants when the synthesis is clear and still understandable on its own.
- Do not smooth over contradictory signals. If positive and negative signals both matter, create separate + and - notes, and optionally add one 0 note that names the tension or condition.
- Include all relevant notes that are well-formed and useful for a workshop. Do not arbitrarily cap the count.

Review rules:
- Before changing review state, read {rel(deliverable_review_path(deliverables_dir / "post-it-notes.md"))} if it exists. Preserve existing researcher decisions. Do not change `Looks good`, `Do not use` or notes for unchanged post-its. In particular, never convert an existing `Do not use` decision back to `Needs changes` or pending review.
- If existing post-it reviews include completed `Do not use` decisions, apply those decisions to the Markdown by removing those exact post-it lines before reporting the deliverable ready. After removing rejected notes, re-sync the review state against the remaining post-it text so approved notes remain `Looks good` and are not re-opened only because line order changed.
- If existing post-it reviews include `Needs changes` notes, revise only those flagged post-it lines, preserve unchanged `Looks good` notes, and leave revised notes pending for another review pass.
- On reruns, only create review state for new or changed post-its. If a previously flagged post-it has already been reviewed, keep that decision unless the post-it text itself changes.
- Use exception-based review. Mark normal short, source-backed, low-risk post-its as curated/ready by default instead of requiring one-by-one researcher review.
- Keep each post-it as a separate line so the web UI can still inspect or edit individual notes.
- Surface only flagged post-its for active review: weakly supported, too interpretive, duplicate/overlapping, potentially misleading, unusually broad, too compressed, high-impact for downstream framing or based on narrow/conditional support.
- For every flagged note, make the review reason explicit in the review state or report: e.g. "narrow support", "possibly too broad", "conditional claim", "may be duplicate" or "needs wording check".
- Do not make researcher judgment calls on flagged notes; keep them pending in the UI.
- Leave unclear or weakly supported notes out unless you can write them as a clear neutral/tension note and flag it for review.

Do not call APIs.
Do not run local stubs.
Do not use backend deliverable generation.
Do not treat these notes as final Figma/FigJam copy until every active flagged note is approved in the UI.

Report what happened in this pass: drafted, applied reviews, revised flagged notes, or confirmed final. Include how many context groups and post-it notes remain, how many are curated/approved, how many are still flagged for review and why."""
    }


def deliverable_ai_prompt(deliverables_dir: Path, deliverable_type: str, fallback_title: str, mode: str = "prepare") -> dict:
    if deliverable_type == "post-it-notes":
        return post_it_notes_prompt(deliverables_dir, mode=mode)
    round_dir = deliverables_dir.parent
    output = deliverables_dir / f"{deliverable_type}.md"
    title = DELIVERABLE_DESCRIPTIONS.get(deliverable_type, fallback_title)
    lens_block = research_lens_prompt_block(round_dir)
    type_guidance = deliverable_type_guidance(deliverable_type)
    action_verb = "Revise" if mode == "revise" else "Prepare"
    prerequisite = (
        "Before drafting this deliverable, confirm that research-summary.md exists and every active section is marked Looks good with no notes. "
        "If the research summary is missing or still under review, report what blocks this deliverable instead of drafting it."
    )
    if deliverable_type == "research-summary":
        prerequisite = "Create or update the research summary directly from accepted Evidence, Patterns, Insights and Recommendations."
    return {
        "label": f"{action_verb} {fallback_title}",
        "button_label": action_verb,
        "copy_label": DELIVERABLE_COPY_LABELS.get(deliverable_type, f"create {fallback_title.lower()}"),
        "instruction": f"Draft or update the reviewable Markdown source for {fallback_title}. This does not export the final artefact.",
        "prompt_description": f"Codex creates or updates only the reviewable Markdown source {output.name}. After every section is approved, use the export/finalize action for the final artefact.",
        "prompt": f"""{action_verb} this reviewable Research OS Markdown deliverable in Codex/Cowork: {fallback_title}.

Round: {rel(round_dir)}
Markdown source file for review: {rel(output)}

First read Research OS/08-looped-learning/active-learnings.md and apply any active Looped Learnings.
{lens_block}
{prerequisite}

Deliverable purpose:
{title}

Format guidance:
{type_guidance}

Rules:
- Create or update exactly this Markdown deliverable: {rel(output)}
- Use accepted knowledge where available. If using proposed material, clearly label it as proposed.
- Do not create new Evidence, Patterns, Insights, Recommendations or review decisions.
- Keep the deliverable reviewable in the web UI.
- Do not export PDF, PPT, Slack-ready final copy or any other final artefact in this pass.
- Do not call APIs.
- Do not run local stubs.
- Do not use backend deliverable generation.

Report what changed and whether {output.name} is ready for UI review."""
    }


def deliverable_export_prompt(deliverables_dir: Path, deliverable_type: str, fallback_title: str) -> dict | None:
    round_dir = deliverables_dir.parent
    source = deliverables_dir / f"{deliverable_type}.md"
    export_map = {
        "research-summary": ("PDF", deliverables_dir / "pdf-deliverables" / "research-summary.pdf"),
        "design-actions-summary": ("PDF", deliverables_dir / "pdf-deliverables" / "design-brief.pdf"),
        "powerpoint-preparation-prompt": ("final copyable deck prompt", source),
        "stakeholder-slack-message": ("final ready-to-post Slack message", source),
        "post-it-notes": ("final Figma/FigJam copyable notes", source),
    }
    if deliverable_type not in export_map:
        return None
    artifact_label, output = export_map[deliverable_type]
    if artifact_label == "PDF":
        action_label = "Create PDF"
        instruction = f"Create the approved final PDF for {fallback_title}. Do not change the Markdown unless explicitly instructed."
        prompt = f"""Generate this approved Research OS deliverable in Codex/Cowork: {fallback_title}.

Round: {rel(round_dir)}
Approved Markdown source: {rel(source)}
Output file: {rel(output)}

First read Research OS/08-looped-learning/active-learnings.md and apply any active Looped Learnings.
Before exporting, read {rel(deliverable_review_path(source))} and confirm every active section for {source.name} is marked Looks good with no notes/comments. History entries are previous review rounds and should not block export.
If any active section is not approved, has notes/comments, or is marked changed, report what blocks PDF generation.
If ready, create a polished PDF at exactly the output file above.
Preserve the approved Markdown wording exactly: do not shorten, rewrite, merge or rename titles, bullets, numbered items or section content for layout reasons. Only change visual formatting in the PDF export.
Use the configured company-branded report style for Research OS PDF deliverables:
- Use local branding assets from Research OS/branding/ when present, especially company-logo.png and company-footer.png.
- Use the configured accent color, logo in the page header, subtle section underlines, a light executive-summary callout and confidential footer/page numbering.
- Place section accent rules directly under the section title with visible whitespace above and below; do not center the rule inside the section body.
- Format bullets and numbered items for stakeholder scanning: keep the original bold lead sentence/title slightly larger or stronger than the body, place the explanation directly below it in the same text column without a hanging or stepped indent, use enough whitespace between items and avoid page-wide undifferentiated text blocks.
- Start major action sections such as Recommended Next Steps on a new page when that improves scanability and still fits the expected page count.
- Keep footer branding recognizable when a footer asset is configured, without letting it compete with content.
- Keep the same visual language across research-summary and design-actions-summary PDF exports.
Render the PDF to PNG pages and inspect the output before reporting it ready to share.
Do not change the Markdown content unless explicitly instructed.
Do not call APIs.
Do not run local stubs.
Do not use backend deliverable generation.

Report the PDF path and whether it is ready to share."""
    else:
        action_label = "Finalize"
        instruction = f"Confirm the approved Markdown source for {fallback_title} is ready as the final artefact."
        post_it_finalize_note = ""
        if deliverable_type == "post-it-notes":
            post_it_finalize_note = "\nFor post-it notes specifically: if the review file still contains completed `Do not use` decisions, do not finalize yet and do not resurrect those notes. Use the Revise post-it notes action first so those rejected post-it lines are removed from the Markdown and the remaining notes are re-synced as approved."
        prompt = f"""Finalize the approved Research OS deliverable in Codex/Cowork: {fallback_title}.

Round: {rel(round_dir)}
Approved Markdown source: {rel(source)}
Final artefact type: {artifact_label}

First read Research OS/08-looped-learning/active-learnings.md and apply any active Looped Learnings.
Before finalizing, read {rel(deliverable_review_path(source))} and confirm every active section for {source.name} is marked Looks good with no notes/comments. History entries are previous review rounds and should not block finalization.
If any active section is not approved, has notes/comments, or is marked changed, report what blocks finalization.
{post_it_finalize_note}
If ready, report that {source.name} is approved and ready to use as the {artifact_label}.
Do not change the Markdown content unless explicitly instructed.
Do not create new Evidence, Patterns, Insights, Recommendations or review decisions.
Do not call APIs.
Do not run local stubs.
Do not use backend deliverable generation."""
    return {
        "label": action_label,
        "button_label": action_label,
        "copy_label": action_label.lower(),
        "instruction": instruction,
        "prompt_description": f"Codex checks that {source.name} is fully approved, then creates or confirms the final {artifact_label}.",
        "prompt": prompt,
    }


def deliverable_dashboard_items(deliverables_dir: Path) -> list[dict]:
    items = []
    seen: set[str] = set()
    review_cache: dict[str, dict] = {}
    copy_stems = {
        "research-summary": "research-summary",
        "design-actions-summary": "design-brief",
    }
    for deliverable_type, fallback_title in DELIVERABLE_REVIEW_ORDER:
        file_path = deliverables_dir / f"{deliverable_type}.md"
        summary = deliverable_file_review_summary(file_path, review_cache)
        status, status_label = str(summary["status"]), str(summary["status_label"])
        export_action = deliverable_export_prompt(deliverables_dir, deliverable_type, fallback_title)
        if deliverable_type == "post-it-notes":
            if file_path.exists() and status == "green" and export_action:
                actions = [
                    {
                        "label": "Copy all notes",
                        "copy_path": rel(file_path),
                        "copy_mode": "post-it-notes",
                    }
                ]
            else:
                actions = [deliverable_ai_prompt(deliverables_dir, deliverable_type, fallback_title, mode="smart")]
        elif file_path.exists() and status == "green" and export_action:
            actions = [export_action]
        else:
            mode = "revise" if file_path.exists() else "prepare"
            actions = [deliverable_ai_prompt(deliverables_dir, deliverable_type, fallback_title, mode=mode)]
        if deliverable_type in {"research-summary", "design-actions-summary"}:
            copy_stem = copy_stems.get(deliverable_type, deliverable_type)
            copy_html = deliverables_dir / "open-copy" / f"{copy_stem}.html"
            copy_pdf = deliverables_dir / "pdf-deliverables" / f"{copy_stem}.pdf"
            if file_path.exists():
                actions.append(
                    {
                        "label": "Copy summary" if deliverable_type == "research-summary" else "Copy brief",
                        "copy_path": rel(file_path),
                        "copy_mode": "raw",
                    }
                )
            if copy_html.exists():
                actions.append(
                    {
                        "label": "Open copy version",
                        "href": dashboard_file_link(copy_html) + "&mode=focus",
                    }
                )
            if copy_pdf.exists():
                actions.append(
                    {
                        "label": "PDF",
                        "href": dashboard_file_link(copy_pdf),
                        "local_path": str(copy_pdf.resolve()),
                    }
                )
        if deliverable_type == "powerpoint-preparation-prompt" and file_path.exists() and status == "green":
            actions.append(
                {
                    "label": "Copy prompt",
                    "copy_path": rel(file_path),
                }
            )
        seen.add(file_path.name)
        items.append(
            {
                "name": file_path.name,
                "title": read_title(file_path, fallback_title) if file_path.exists() else fallback_title,
                "description": DELIVERABLE_DESCRIPTIONS.get(deliverable_type, ""),
                "href": dashboard_file_link(file_path) + "&mode=focus" if file_path.exists() else "",
                "kind": "MD",
                "exists": file_path.exists(),
                "status": status,
                "status_label": status_label,
                "review": int(summary["review"]) if file_path.exists() else 0,
                "actions": actions,
            }
        )
    for file_path in non_empty_files(deliverables_dir):
        try:
            relative_parts = file_path.relative_to(deliverables_dir).parts
        except ValueError:
            relative_parts = file_path.parts
        if (
            any(folder in relative_parts for folder in {"open-copy", "pdf-deliverables"})
            or file_path.name in seen
            or file_path.name in {"README.md", ".deliverable-reviews.json"}
            or file_path.name.startswith(".")
        ):
            continue
        summary = deliverable_file_review_summary(file_path, review_cache)
        status, status_label = str(summary["status"]), str(summary["status_label"])
        items.append(
            {
                "name": file_path.name,
                "title": read_title(file_path, file_path.stem) if file_path.suffix.lower() == ".md" else file_path.name,
                "description": "Additional generated deliverable.",
                "href": dashboard_file_link(file_path) + "&mode=focus" if file_path.exists() else "",
                "kind": file_path.suffix.lstrip(".").upper() or "File",
                "exists": file_path.exists(),
                "status": status,
                "status_label": status_label,
                "review": int(summary["review"]) if file_path.suffix.lower() == ".md" else 0,
            }
        )
    return items


def update_deliverable_review(target: Path, section_id: str, status: str, notes: str) -> None:
    if not is_deliverable_markdown(target):
        raise ValueError("Deliverable reviews are only supported for Markdown deliverables.")
    if not re.match(r"^DSEC-\d{3}$", section_id):
        raise ValueError("Unsupported deliverable section ID.")
    if status not in {"Looks good", "Needs changes", "Do not use", ""}:
        raise ValueError("Status must be Looks good, Needs changes or Do not use.")
    data = load_deliverable_reviews(target)
    section_map = {section["id"]: section for section in deliverable_sections(read_text(target), target)}
    section_hash = content_hash(section_map.get(section_id, {}).get("content", ""))
    data.setdefault("sections", {})[section_id] = {
        "status": status,
        "notes": notes,
        "updated_at": now().isoformat(),
        "content_hash": section_hash,
    }
    if status == "Looks good" and not notes.strip():
        data.setdefault("changed_sections", {}).pop(section_id, None)
    save_deliverable_reviews(target, data)


def dashboard_deliverable_review_page(title: str, text: str, base_style: str, target: Path) -> str:
    sections = deliverable_sections(text, target)
    review_data = sync_deliverable_review_state(target, sections)
    reviews = review_data.get("sections", {})
    changed_sections = review_data.get("changed_sections", {})
    iteration = len(review_data.get("history", [])) + 1
    path_attr = html.escape(rel(target))
    notes_path = html.escape(rel(deliverable_review_path(target)))
    review_cards = []
    for section in sections:
        stored = reviews.get(section["id"], {})
        status = stored.get("status", "")
        notes = stored.get("notes", "")
        changed_info = changed_sections.get(section["id"], {})
        changed_lines = changed_info.get("changed_lines", []) if isinstance(changed_info, dict) else []
        is_complete = status == "Looks good" and not notes.strip() and not changed_info
        content_html = simple_markdown_html_with_highlights(section["content"], changed_lines)
        changed_badge = '<span class="changed-badge">Changed in this iteration</span>' if changed_info else ""
        saved_html = f'<span class="deliverable-saved"><strong>{html.escape(status)}</strong>{f"<em>{html.escape(notes)}</em>" if notes else ""}</span>' if status else ""
        editor_style = " hidden" if is_complete else ""
        complete_html = (
            f"""<div class="deliverable-complete">
              <span class="deliverable-saved"><strong>Looks good</strong><em>Ready for this iteration</em></span>
              <button class="edit-deliverable-review" type="button" data-edit-section="{html.escape(section['id'])}">Edit</button>
            </div>"""
            if is_complete
            else ""
        )
        review_cards.append(
            f"""<article class="deliverable-section" data-section="{html.escape(section['id'])}">
              <div class="deliverable-section-head"><span>{html.escape(section['id'])}</span><strong>{html.escape(section['title'])}</strong>{changed_badge}</div>
              <div class="deliverable-content">{content_html or '<p class="muted">No section body.</p>'}</div>
              {complete_html}
              <div class="deliverable-review-controls{editor_style}">
                <textarea data-notes="{html.escape(section['id'])}" placeholder="Optional: what would you change, trust, or reject?">{html.escape(notes)}</textarea>
                <div class="decision-row">
                  <button class="decision-yes" type="button" data-deliverable-decision="Looks good" data-id="{html.escape(section['id'])}">
                    <svg viewBox="0 0 20 20" aria-hidden="true"><path d="M16.5 5.5 8 14l-4.5-4.5"/></svg>
                    <span>Yes, use this</span>
                  </button>
                  <button class="decision-revise" type="button" data-deliverable-decision="Needs changes" data-id="{html.escape(section['id'])}">
                    <svg viewBox="0 0 20 20" aria-hidden="true"><path d="M11.8 4.2 15.8 8.2 7.2 16.8 3.2 17.8 4.2 13.8 11.8 4.2z"/><path d="M10.7 5.3 14.7 9.3"/></svg>
                    <span>Needs changes</span>
                  </button>
                  <button class="decision-no" type="button" data-deliverable-decision="Do not use" data-id="{html.escape(section['id'])}">
                    <svg viewBox="0 0 20 20" aria-hidden="true"><path d="M5 5 15 15M15 5 5 15"/></svg>
                    <span>No, don't use</span>
                  </button>
                  <span data-state="{html.escape(section['id'])}">{saved_html}</span>
                </div>
              </div>
            </article>"""
        )
    revise_prompt = f"""Revise this Research OS deliverable in Codex/Cowork: {rel(target)}.

First read Research OS/08-looped-learning/active-learnings.md and apply any active Looped Learnings.
Read the deliverable and its review notes from {rel(deliverable_review_path(target))}.
Apply completed deliverable review notes directly to the Markdown deliverable.
Preserve sections marked Looks good with no notes unless you changed their content.
After applying notes, add a history entry in {rel(deliverable_review_path(target))} for the review round you processed. Keep completed section decisions available so unchanged approved sections do not need to be reviewed again. Sections whose content changes will be marked changed by the UI and should be reviewed again.
Do not call APIs, do not run local stubs, and do not use backend deliverable generation.
After updating, report exactly which sections changed and confirm the deliverable is ready for review iteration {iteration + 1}."""
    deliverable_style = base_style + """
      main { max-width: 1040px; }
      .deliverable-top { display:grid; grid-template-columns:auto 1fr auto auto; align-items:flex-start; gap:16px; margin-bottom:16px; }
      .deliverable-back { display:inline-flex; align-items:center; min-height:30px; border:1px solid var(--border-muted); border-radius:5px; background:#fff; color:var(--fg-2); padding:0 10px; font-size:12px; font-weight:700; text-decoration:none; }
      .deliverable-back:hover { border-color:var(--blue-dark); text-decoration:none; }
      .deliverable-top h1 { margin:0 0 6px; }
      .iteration-badge { display:inline-flex; align-items:center; min-height:24px; border:1px solid var(--border-muted); border-radius:999px; padding:0 9px; background:#fff; color:var(--fg-2); font-size:12px; font-weight:700; }
      .muted { color:var(--fg-3); font-size:12px; }
      .copy-prompt { border:1px solid var(--border-muted); border-radius:5px; background:#fff; color:var(--fg-2); font:inherit; font-size:12px; font-weight:700; padding:7px 10px; cursor:pointer; }
      .deliverable-grid { display:grid; gap:10px; }
      .deliverable-section { border:1px solid var(--line); border-radius:8px; background:var(--surface-subtle); padding:13px; }
      .deliverable-section-head { display:flex; gap:9px; align-items:center; color:var(--fg-2); font-size:12px; margin-bottom:8px; }
      .deliverable-section-head span { font-weight:800; color:var(--fg-3); }
      .deliverable-section-head strong { color:var(--fg-1); }
      .changed-badge { margin-left:auto; display:inline-flex; align-items:center; min-height:22px; border:1px solid rgba(124,58,237,.35); border-radius:999px; background:var(--ai-purple-bg); color:var(--blue); padding:0 8px; font-size:11px; font-weight:750; }
      .deliverable-content { background:#fff; border:1px solid var(--line); border-radius:6px; padding:10px 12px; line-height:1.5; }
      .deliverable-content h2, .deliverable-content h3, .deliverable-content h4 { margin:12px 0 6px; }
      .deliverable-content p { margin:7px 0; }
      .deliverable-content ul { padding-left:20px; }
      .deliverable-content pre { margin:0; white-space:pre-wrap; user-select:text; background:var(--surface-muted); border:1px solid var(--line); border-radius:6px; padding:9px 10px; font:inherit; color:var(--fg-1); }
      .deliverable-content .nested-bullet { margin: -4px 0 8px 22px; color:var(--fg-2); font-size:12.5px; line-height:1.45; }
      .deliverable-content .nested-bullet::before { content:"- "; color:var(--fg-3); }
      .changed-line { background:var(--changed-bg); box-shadow: -4px 0 0 var(--changed-bar); border-radius:3px; padding:1px 3px; }
      .deliverable-complete { display:flex; align-items:center; justify-content:space-between; gap:10px; margin-top:10px; border:1px solid var(--status-success-bg); border-radius:6px; background:var(--status-success-bg); padding:8px 10px; }
      .edit-deliverable-review { min-height:28px; border:1px solid var(--border-muted); border-radius:5px; background:#fff; color:var(--fg-2); font:inherit; font-size:12px; font-weight:700; padding:0 9px; cursor:pointer; }
      .deliverable-review-controls { display:grid; gap:8px; margin-top:10px; }
      .deliverable-review-controls.hidden { display:none; }
      .deliverable-review-controls textarea { display:block; width:100%; max-width:100%; min-width:0; min-height:70px; border:1px solid var(--border-muted); border-radius:5px; padding:10px; font:inherit; font-size:13px; resize:vertical; background:#fff; color:var(--fg-1); }
      .decision-row { position:relative; display:flex; gap:8px; flex-wrap:wrap; align-items:center; }
      .decision-row button { min-height:36px; border:1px solid var(--border-muted); border-radius:5px; background:#fff; color:var(--fg-1); font:inherit; font-size:12px; font-weight:650; cursor:pointer; padding:0 12px; }
      .decision-row [data-deliverable-decision] { display:inline-flex; align-items:center; gap:7px; }
      .decision-row [data-deliverable-decision] svg { width:15px; height:15px; fill:none; stroke:currentColor; stroke-width:2.4; stroke-linecap:round; stroke-linejoin:round; }
      .decision-row .decision-yes { color:var(--status-success); border-color:var(--status-success-bg); background:var(--status-success-bg); }
      .decision-row .decision-revise { color:var(--status-warning); border-color:var(--status-warning-bg); background:var(--status-warning-soft-bg); }
      .decision-row .decision-no { color:var(--status-danger); border-color:var(--status-danger-bg); background:var(--status-danger-bg); }
      .decision-row button:hover { border-color:var(--blue-dark); }
      .deliverable-saved { display:inline-flex; align-items:center; gap:7px; color:var(--fg-2); font-size:12px; }
      .deliverable-saved em { font-style:normal; color:var(--fg-3); }
      .raw { margin-top:18px; }
    """
    return f"""<!doctype html><html><head><title>{title}</title><style>{deliverable_style}</style></head><body><main>
      <header class="deliverable-top">
        <a class="deliverable-back" href="/dashboard">← Dashboard</a>
        <div><h1>{title}</h1><div class="muted">Review notes are stored in {notes_path}</div></div>
        <div class="iteration-badge">Review iteration {iteration}</div>
        <button class="copy-prompt" type="button" data-prompt="{html.escape(revise_prompt)}">Copy revise prompt</button>
      </header>
      <section class="deliverable-grid">{"".join(review_cards)}</section>
      <details class="raw"><summary>Raw Markdown</summary><pre>{html.escape(text)}</pre></details>
      <script>
        const path = "{path_attr}";
        const decisionLabels = {{ "Looks good": "Looks good", "Needs changes": "Needs changes", "Do not use": "Do not use" }};
        document.querySelectorAll("[data-deliverable-decision]").forEach(button => button.addEventListener("click", async () => {{
          const id = button.dataset.id;
          const status = button.dataset.deliverableDecision || "";
          const notes = document.querySelector(`[data-notes="${{CSS.escape(id)}}"]`)?.value || "";
          const state = document.querySelector(`[data-state="${{CSS.escape(id)}}"]`);
          if (state) state.textContent = "Saving...";
          const response = await fetch("/api/deliverable-review-note", {{
            method: "POST",
            headers: {{ "Content-Type": "application/json" }},
            body: JSON.stringify({{ path, section_id: id, status, notes }})
          }});
          if (!response.ok) {{
            if (state) state.textContent = await response.text();
            return;
          }}
          if (state) state.innerHTML = `<span class="deliverable-saved"><strong>${{decisionLabels[status] || status}}</strong>${{notes ? `<em>${{notes.replace(/[&<>"']/g, char => ({{ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }}[char]))}}</em>` : ""}}</span>`;
          if (status === "Looks good" && !notes.trim()) setTimeout(() => location.reload(), 250);
        }}));
        document.querySelectorAll("[data-edit-section]").forEach(button => button.addEventListener("click", () => {{
          const section = button.closest(".deliverable-section");
          section?.querySelector(".deliverable-complete")?.remove();
          section?.querySelector(".deliverable-review-controls")?.classList.remove("hidden");
        }}));
        document.querySelectorAll("[data-prompt]").forEach(button => button.addEventListener("click", async () => {{
          const original = button.textContent;
          await navigator.clipboard.writeText(button.dataset.prompt || "");
          button.textContent = "Copied";
          setTimeout(() => button.textContent = original, 1200);
        }}));
      </script>
    </main></body></html>"""


REVIEW_PIPELINE_STAGES = [
    ("context", "Context"),
    ("sources", "Sources"),
    ("evidence", "Evidence"),
    ("patterns", "Patterns"),
    ("insights", "Insights"),
    ("recommendations", "Recommendations"),
    ("reviews", "Review"),
    ("learning", "Learning"),
    ("deliverables", "Deliverable"),
]


def review_pipeline_stage(item: dict) -> str:
    type_text = (item.get("type") or "").lower()
    item_id = (item.get("id") or "").lower()
    source_text = (item.get("source") or "").lower()
    fields = " ".join([type_text, item_id, source_text])
    if "looped learning" in fields or item_id.startswith("ll-") or "learning" in fields:
        return "learning"
    if "recommendation" in fields or item_id.startswith("rec-") or "rec-" in fields:
        return "recommendations"
    if "pattern" in fields:
        return "patterns"
    if "insight" in fields:
        return "insights"
    if item.get("is_virtual") or item.get("evidence_id") or "finding" in fields or "evidence" in fields:
        return "evidence"
    if "deliverable" in fields or "slack" in fields:
        return "deliverables"
    if "source" in fields:
        return "sources"
    if "context" in fields or "prior" in fields:
        return "context"
    return "reviews"


def review_pipeline_html(item: dict) -> str:
    active = review_pipeline_stage(item)
    active_index = next(
        (index for index, (key, _label) in enumerate(REVIEW_PIPELINE_STAGES) if key == active),
        len(REVIEW_PIPELINE_STAGES) - 2,
    )
    parts = []
    for index, (key, label) in enumerate(REVIEW_PIPELINE_STAGES):
        state = " active" if key == active else " past" if index < active_index else ""
        current = ' aria-current="step"' if key == active else ""
        parts.append(f'<span class="review-step{state}"{current}>{html.escape(label)}</span>')
    return f'<nav class="review-pipeline" aria-label="Research pipeline stage">{"".join(parts)}</nav>'


def dashboard_pdf_page(target: Path) -> str:
    display_title = html.escape(dashboard_display_title(target))
    raw_href = html.escape(dashboard_raw_file_link(target), quote=True)
    file_label = html.escape(rel(target))
    style = """
      :root {
        color-scheme: light;
        --bg-1:#ffffff; --bg-2:#F4F5F7; --surface:#ffffff; --surface-muted:#F4F5F7; --surface-subtle:#FBFBFA; --grey-3:#E2E0DF;
        --fg-1:#222222; --fg-2:#575654; --fg-3:#9A9997; --border-1:#E2E0DF; --border-muted:#D8DFEB;
        --blue:#3D74FF; --blue-dark:#194FCF; --ai-purple:#7C3AED; --ai-purple-bg:#F4EFFF;
        --status-success:#00893F; --status-success-bg:#D5F4E3;
        --status-warning:#9A6200; --status-warning-bg:#FFF3C4; --status-warning-soft-bg:#FFF9E8; --status-warning-bar:#F2B83B;
        --status-danger:#C1002F; --status-danger-bg:#F9D8DF;
        --changed-bg:#FFF4BD; --changed-bar:#F5D84F;
        --line:var(--border-1); --fg:var(--fg-1); --muted:var(--fg-3); --bg:var(--bg-2); --accent:var(--ai-purple);
      }
      * { box-sizing: border-box; }
      body { margin: 0; background: var(--bg); color: var(--fg); font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
      .file-top { position: sticky; top: 0; z-index: 20; min-height: 52px; display: grid; grid-template-columns: auto 1fr auto; gap: 12px; align-items: center; padding: 0 18px; background: rgba(255,255,255,.96); border-bottom: 1px solid var(--line); backdrop-filter: blur(10px); }
      .file-top a, .file-top button { height: 30px; display: inline-flex; align-items: center; justify-content: center; border: 1px solid var(--border-muted); border-radius: 6px; background: var(--surface); color: var(--fg-2); padding: 0 10px; font: inherit; font-size: 12px; font-weight: 650; line-height: 28px; text-decoration: none; cursor: pointer; }
      .file-top a:hover, .file-top button:hover { border-color: var(--blue-dark); text-decoration: none; }
      .file-title { min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; text-align: center; font-size: 13px; font-weight: 700; color: var(--fg-2); }
      .file-actions { display: flex; gap: 8px; justify-content: flex-end; align-items: center; }
      .file-meta { padding: 8px 18px; color: var(--muted); font-size: 11px; border-bottom: 1px solid var(--line); background: var(--surface); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
      .pdf-frame { width: 100%; height: calc(100vh - 87px); border: 0; display: block; background: var(--surface); }
      .pdf-fallback { margin: 24px; padding: 18px; border: 1px solid var(--line); border-radius: 8px; background: var(--surface); }
      @media (max-width: 760px) {
        .file-top { grid-template-columns: 1fr; padding: 10px 14px; }
        .file-title { text-align: left; }
        .file-actions { justify-content: flex-start; }
        .pdf-frame { height: calc(100vh - 150px); }
      }
    """
    return f"""<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>{display_title}</title>
    <style>{style}</style>
  </head>
  <body>
    <header class="file-top">
      <a href="/dashboard">← Dashboard</a>
      <div class="file-title">{display_title}</div>
      <div class="file-actions">
        <button type="button" onclick="history.length > 1 ? history.back() : location.href='/dashboard'">Back</button>
        <a href="{raw_href}" target="_blank" rel="noopener">Open PDF</a>
      </div>
    </header>
    <div class="file-meta">{file_label}</div>
    <iframe class="pdf-frame" src="{raw_href}" title="{display_title}">
      <div class="pdf-fallback">PDF preview is unavailable. <a href="{raw_href}">Open the PDF directly</a>.</div>
    </iframe>
  </body>
</html>"""


def dashboard_file_page(path_value: str, mode: str = "", stage: str = "") -> str:
    try:
        target = resolve_dashboard_file(path_value)
    except PermissionError:
        return "<!doctype html><title>Blocked</title><p>Path is outside Research OS.</p>"
    title = html.escape(dashboard_display_title(target))
    if not target.exists():
        return f"<!doctype html><title>Missing</title><p>Missing: {title}</p>"
    style = """
      :root {
        color-scheme: light;
        --bg-1:#ffffff; --bg-2:#F4F5F7; --surface:#ffffff; --surface-muted:#F4F5F7; --surface-subtle:#FBFBFA; --grey-3:#E2E0DF;
        --fg-1:#222222; --fg-2:#575654; --fg-3:#9A9997; --border-1:#E2E0DF; --border-muted:#D8DFEB;
        --blue:#3D74FF; --blue-dark:#194FCF; --ai-purple:#7C3AED; --ai-purple-bg:#F4EFFF;
        --status-success:#00893F; --status-success-bg:#D5F4E3;
        --status-warning:#9A6200; --status-warning-bg:#FFF3C4; --status-warning-soft-bg:#FFF9E8; --status-warning-bar:#F2B83B;
        --status-danger:#C1002F; --status-danger-bg:#F9D8DF;
        --changed-bg:#FFF4BD; --changed-bar:#F5D84F;
        --line:var(--border-1); --fg:var(--fg-1); --muted:var(--fg-3); --bg:var(--bg-2); --accent:var(--ai-purple);
        --decision-yes-bg:var(--status-success-bg); --decision-yes:var(--status-success);
        --decision-revise-bg:var(--status-warning-bg); --decision-revise:var(--status-warning);
        --decision-no-bg:var(--status-danger-bg); --decision-no:var(--status-danger);
      }
      body { margin: 0; padding: 28px; background: var(--bg); color: var(--fg-1); font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
      main { max-width: 980px; margin: 0 auto; background: var(--surface); border: 1px solid var(--line); border-radius: 8px; padding: 22px; }
      h1 { margin: 0 0 16px; font-size: 16px; }
      a { color: var(--blue); text-decoration: none; }
      a:hover { text-decoration: underline; }
      pre { white-space: pre-wrap; overflow-wrap: anywhere; line-height: 1.5; font-size: 13px; }
      li { margin: 8px 0; }
    """
    if target.is_dir():
        children = [child for child in sorted(target.iterdir()) if child.name not in {".DS_Store", ".gitkeep"}]
        non_readme_children = [child for child in children if child.name != "README.md"]
        if non_readme_children:
            children = non_readme_children
        files = [child for child in children if child.is_file()]
        if len(files) == 1 and len(children) == 1:
            return dashboard_file_page(rel(files[0]), mode=mode, stage=stage)
        items = []
        for child in children:
            href = dashboard_file_link(child)
            suffix = "/" if child.is_dir() else ""
            kind = "Folder" if child.is_dir() else child.suffix.lstrip(".").upper() or "File"
            items.append(f'<a class="doc-card" href="{href}"><strong>{html.escape(child.name + suffix)}</strong><span>{html.escape(kind)}</span></a>')
        listing = "\n".join(items) if items else "<p>No files.</p>"
        listing_style = style + """
          .doc-list { display: grid; gap: 10px; }
          .doc-card { display: flex; justify-content: space-between; gap: 16px; padding: 12px; border: 1px solid var(--line); border-radius: 8px; background: var(--surface-subtle); color: inherit; }
          .doc-card:hover { text-decoration: none; border-color: var(--border-muted); }
          .doc-card span { color: var(--fg-3); font-size: 12px; }
        """
        return f"<!doctype html><html><head><title>{title}</title><style>{listing_style}</style></head><body><main><h1>{title}</h1><section class=\"doc-list\">{listing}</section></main></body></html>"
    if target.suffix.lower() == ".html" and "open-copy" in target.parts:
        return read_text(target)
    try:
        text = read_text(target)
    except UnicodeDecodeError:
        return f"<!doctype html><html><head><title>{title}</title><style>{style}</style></head><body><main><h1>{title}</h1><p>This file is not text-readable in the dashboard. Open it from Finder or Codex.</p></main></body></html>"
    if target.name in {"review-queue.md", "project-context-proposals.md", "suggested-learnings.md"}:
        return dashboard_review_focus_page(target, title, text, style, stage=stage)
    artifact_kind = {
        "evidence.md": "evidence",
        "patterns.md": "patterns",
        "insights.md": "insights",
        "recommendations.md": "recommendations",
    }.get(target.name)
    if artifact_kind:
        return dashboard_artifact_cards_page(title, text, artifact_kind, style, target)
    if is_deliverable_markdown(target) and target.name != "README.md" and target.name not in NON_REVIEWABLE_DELIVERABLES:
        return dashboard_deliverable_review_page(title, text, style, target)
    readable_style = style + """
      .markdown { line-height: 1.55; }
      .markdown h2, .markdown h3, .markdown h4, .markdown h5 { margin: 20px 0 8px; }
      .markdown p { margin: 8px 0; }
      .markdown ul { padding-left: 20px; }
      .markdown li { margin: 5px 0; }
      .markdown pre { background: var(--surface-muted); border: 1px solid var(--line); border-radius: 6px; padding: 12px; }
    """
    return f"<!doctype html><html><head><title>{title}</title><style>{readable_style}</style></head><body><main><h1>{title}</h1><article class=\"markdown\">{simple_markdown_html(text)}</article><details><summary>Raw Markdown</summary><pre>{html.escape(text)}</pre></details></main></body></html>"


def split_recommendation_sections(summary: str) -> tuple[str, str]:
    learned = ""
    should_do = ""
    match = re.search(
        r"What we learned:\s*(.*?)(?:\n\s*\n|\s+)What we should do:\s*(.*)",
        summary,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if match:
        learned = match.group(1).strip()
        should_do = match.group(2).strip()
    return learned, should_do


def paragraph_and_bullets(text: str) -> str:
    clean = re.sub(r"\s+", " ", text.strip())
    if not clean:
        return ""
    sentences = re.split(r"(?<=[.!?])\s+", clean)
    lead = sentences[0].strip()
    rest = " ".join(sentence.strip() for sentence in sentences[1:] if sentence.strip())
    bullets: list[str] = []
    if rest:
        parts = re.split(r";\s+|,\s+(?=(?:and\s+)?(?:add|always|show|include|consider|make|keep|let|separate|clarify|redesign|create|treat|reserve|use|support)\b)", rest, flags=re.IGNORECASE)
        bullets = [part.strip().rstrip(".") for part in parts if part.strip()]
    html_parts = [f"<p>{html.escape(lead)}</p>"]
    if bullets:
        html_parts.append("<ul>" + "".join(f"<li>{html.escape(item)}</li>" for item in bullets) + "</ul>")
    elif len(sentences) > 1:
        html_parts.extend(f"<p>{html.escape(sentence.strip())}</p>" for sentence in sentences[1:] if sentence.strip())
    return "".join(html_parts)


def review_proposal_html(item: dict, target: Path) -> str:
    summary = review_summary_text(item, target)
    changed = bool(item.get("changed_fields", {}).get("proposal"))
    changed_class = " changed-review-field" if changed else ""
    changed_badge = '<strong class="review-changed-badge">Changed since last review</strong>' if changed else ""
    learning_context = ""
    if review_pipeline_stage(item) == "learning":
        context_sections = []
        if item.get("example"):
            context_sections.append(
                f'<section><h3>Example</h3><p>{html.escape(item["example"])}</p></section>'
            )
        if item.get("future_analysis_change"):
            context_sections.append(
                f'<section><h3>What will change for future analysis</h3><p>{html.escape(item["future_analysis_change"])}</p></section>'
            )
        if context_sections:
            learning_context = f'<div class="learning-impact">{"".join(context_sections)}</div>'
    if review_pipeline_stage(item) == "recommendations":
        learned, should_do = split_recommendation_sections(summary)
        if learned or should_do:
            return f"""<div class="review-summary recommendation-proposal{changed_class}">
              <span>Proposal</span>{changed_badge}
              <section><h3>What we learned</h3>{paragraph_and_bullets(learned)}</section>
              <section><h3>What we should do</h3>{paragraph_and_bullets(should_do)}</section>
            </div>{learning_context}"""
    return f'<div class="review-summary{changed_class}"><span>Proposal</span>{changed_badge}<p>{html.escape(summary)}</p></div>{learning_context}'


def review_item_context(item: dict, target: Path) -> tuple[str, str, str, str, str, str]:
    supporting_reference = item.get("supporting_evidence") or item.get("source_reference", "")
    supporting = review_reference_link(supporting_reference, target)
    contradicting = review_reference_link(item["contradicting_evidence"], target)
    meta_rows = []
    if item.get("research_question"):
        meta_rows.append(f"<dt>Question</dt><dd>{html.escape(item['research_question'])}</dd>")
    if item.get("source_detail"):
        meta_rows.append(f"<dt>Source</dt><dd>{html.escape(item['source_detail'])}</dd>")
    if item.get("source_reference") and item.get("is_virtual"):
        meta_rows.append(f"<dt>Moment</dt><dd>{html.escape(item['source_reference'])}</dd>")
    if item.get("salience"):
        meta_rows.append(f"<dt>Salience</dt><dd>{html.escape(item['salience'])}</dd>")
    if item.get("uncertainty"):
        meta_rows.append(f"<dt>Uncertainty</dt><dd>{html.escape(item['uncertainty'])}</dd>")
    if not meta_rows:
        meta_rows.extend(
            [
                f"<dt>Document</dt><dd>{supporting}</dd>",
                f"<dt>Tension</dt><dd>{contradicting}</dd>",
            ]
        )
    snippet = source_snippet_html(item, target)
    preview = evidence_preview_html(item, target)
    gates = review_quality_gate_html(item)
    meta_html = f'<dl>{"".join(meta_rows)}</dl>'
    evidence_html = f"{preview or snippet}{gates}"
    return (
        review_question(item),
        review_explanation(item),
        review_choice_hint(item),
        review_proposal_html(item, target),
        evidence_html,
        meta_html,
    )


def review_quality_gate_html(item: dict) -> str:
    issues = item.get("gate_issues", [])
    if not issues:
        return ""
    rows = "".join(
        f'<li><strong>{html.escape(issue.get("id", "Gate"))}</strong><span>{html.escape(issue.get("message", ""))}</span></li>'
        for issue in issues[:4]
    )
    more = len(issues) - 4
    more_html = f'<p>{more} more gate{"s" if more != 1 else ""} on this item.</p>' if more > 0 else ""
    return f"""<section class="quality-gates">
      <h3>Quality gates</h3>
      <ul>{rows}</ul>
      {more_html}
    </section>"""


def review_decision_controls(item: dict, hint: str, textarea_min: bool = False) -> str:
    textarea_class = "compact-notes" if textarea_min else ""
    item_id = html.escape(item["id"])
    hint_html = html.escape(hint)
    notes = html.escape(item.get("notes", ""))
    return f"""
      <textarea class="{textarea_class}" data-notes="{item_id}" placeholder="Optional: what would you change, trust, or reject?">{notes}</textarea>
      <div class="decision-row">
        <button class="decision-yes" data-decision="Approve" data-id="{item_id}">
          <svg viewBox="0 0 20 20" aria-hidden="true"><path d="M16.5 5.5 8 14l-4.5-4.5"/></svg>
          <span>Yes, use this</span>
        </button>
        <button class="decision-revise" data-decision="Revise" data-id="{item_id}">
          <svg viewBox="0 0 20 20" aria-hidden="true"><path d="M11.8 4.2 15.8 8.2 7.2 16.8 3.2 17.8 4.2 13.8 11.8 4.2z"/><path d="M10.7 5.3 14.7 9.3"/></svg>
          <span>Needs changes</span>
        </button>
        <button class="decision-no" data-decision="Reject" data-id="{item_id}">
          <svg viewBox="0 0 20 20" aria-hidden="true"><path d="M5 5 15 15M15 5 5 15"/></svg>
          <span>No, don't use</span>
        </button>
        <span class="choice-help">
          <button class="choice-help-button" type="button" aria-label="Decision help">i</button>
          <span class="choice-help-tip">{hint_html}</span>
        </span>
      </div>
    """


def review_decided_controls(item: dict, labels: dict[str, str]) -> str:
    item_id = html.escape(item["id"])
    decision = item.get("decision") or item.get("status", "")
    label = html.escape(labels.get(decision, decision))
    date = html.escape(item.get("date", ""))
    notes = html.escape(item.get("notes", ""))
    return f"""<div class="decided">
      <div><strong>You answered: {label}</strong>{f'<span>{date}</span>' if date else ''}</div>
      {f'<p>{notes}</p>' if notes else ''}
      <button class="edit-review" type="button" data-edit-review="{item_id}">Edit review</button>
    </div>"""


def dashboard_review_focus_page(target: Path, title: str, text: str, base_style: str, stage: str = "") -> str:
    stage = stage.strip().lower()
    valid_stages = {key for key, _label in REVIEW_PIPELINE_STAGES}
    if stage not in valid_stages:
        stage = ""
    def is_pending(item: dict) -> bool:
        return item["status"].lower() in {"pending", "proposed", "open"} and not item["decision"]

    items = [
        item
        for item in expanded_review_items(target)
        if (not stage or review_pipeline_stage(item) == stage) and (not stage or is_pending(item))
    ]
    impact_order = {"recommendations": 6, "insights": 5, "patterns": 4, "evidence": 3, "context": 2, "learning": 1}
    items = [
        item
        for _index, item in sorted(
            enumerate(items),
            key=lambda pair: (
                not is_pending(pair[1]),
                -int(pair[1].get("gate_count", 0)),
                -impact_order.get(review_pipeline_stage(pair[1]), 0),
                pair[0],
            ),
        )
    ]
    stage_label = dict(REVIEW_PIPELINE_STAGES).get(stage, "")
    display_title = f"{title} - {stage_label}" if stage_label else title
    round_dir = round_dir_for_review_path(target)
    lens = selected_research_lens(round_dir) if round_dir else None
    lens_notice = ""
    if lens:
        lens_class = " special" if lens.get("is_special") else ""
        lens_notice = f'<div class="focus-lens{lens_class}"><strong>Research lens</strong><span>{html.escape(lens["label"])}</span>{f"<em>Special lens active</em>" if lens.get("is_special") else "<em>Default</em>"}</div>'
    cards = []
    labels = {"Approve": "Yes, use this", "Revise": "Needs changes", "Reject": "No, don't use"}
    for index, item in enumerate(items):
        pending = is_pending(item)
        question, explanation, hint, summary, evidence_html, meta_html = review_item_context(item, target)
        edit_controls = review_decision_controls(item, hint)
        if pending:
            controls = edit_controls
        else:
            controls = review_decided_controls(item, labels)
        reason = review_reason_text(item)
        reason_class = "review-reason changed-review-field" if item.get("changed_fields", {}).get("reason") else "review-reason"
        gate_badge = f'<strong class="gate-badge">{int(item.get("gate_count", 0))} quality gate{"s" if int(item.get("gate_count", 0)) != 1 else ""}</strong>' if item.get("gate_count") else ""
        changed_badge = '<strong class="review-changed-badge">Changed since last review</strong>' if item.get("changed_fields") else ""
        cards.append(
            f"""<article class="focus-card" data-index="{index}" data-pending="{str(pending).lower()}">
              <div class="review-head"><span>{html.escape(item['type'])}</span><em>{html.escape(item['id'])}</em>{gate_badge}{changed_badge}</div>
              <h2>{html.escape(question)}</h2>
              <p class="review-explanation">{html.escape(explanation)}</p>
              {review_pipeline_html(item)}
              <section class="review-action">
                {summary}
                <div class="focus-controls" data-control-for="{html.escape(item['id'])}">{controls}</div>
                <template data-edit-template="{html.escape(item['id'])}">{edit_controls}</template>
                <p class="{reason_class}"><span>{html.escape(review_reason_label(item))}</span>{html.escape(reason)}</p>
              </section>
              <section class="focus-context">{evidence_html}<div class="review-meta">{meta_html}</div></section>
            </article>"""
        )
    focus_style = base_style + """
      *, *::before, *::after { box-sizing: border-box; }
      body { padding: 0; background: var(--bg); }
      main { max-width: none; min-height: 100vh; margin: 0; border: 0; border-radius: 0; padding: 0; background: var(--bg); }
      .focus-top { position: sticky; top: 0; z-index: 20; display: grid; grid-template-columns: 120px 1fr auto; gap: 12px; align-items: center; min-height: 52px; padding: 0 18px; background: rgba(255,255,255,.96); border-bottom: 1px solid var(--line); backdrop-filter: blur(10px); }
      .focus-top a, .focus-top button { height: 28px; border: 1px solid var(--border-muted); border-radius: 5px; background: #fff; color: var(--fg-2); padding: 0 9px; font: inherit; font-size: 12px; font-weight: 650; text-decoration: none; cursor: pointer; }
      .focus-back { display: inline-flex; align-items: center; justify-content: center; justify-self: start; }
      .focus-title { min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: 13px; font-weight: 650; color: var(--fg-2); text-align: center; }
      .focus-nav { display: flex; gap: 8px; justify-content: flex-end; }
      .focus-count { color: var(--fg-3); font-size: 12px; margin-right: 8px; align-self: center; }
      .focus-wrap { max-width: 1080px; margin: 0 auto; padding: 24px; }
      .focus-lens { max-width: 1080px; margin: 14px auto 0; display:flex; align-items:center; gap:8px; border:1px solid var(--border-muted); border-radius:8px; background:#fff; padding:9px 12px; color:var(--fg-2); font-size:12px; }
      .focus-lens.special { border-color:var(--status-warning-bg); background:var(--status-warning-soft-bg); color:var(--status-warning); }
      .focus-lens strong { color:var(--fg-2); }
      .focus-lens span { font-weight:700; }
      .focus-lens em { margin-left:auto; font-style:normal; color:var(--fg-3); }
      .focus-lens.special em { color:var(--status-warning); }
      .focus-card { display: none; width: 100%; min-width: 0; overflow: hidden; border: 1px solid rgba(124,58,237,.25); border-radius: 10px; padding: 18px; background: #fff; box-shadow: 0 12px 30px rgba(31, 43, 70, .08); }
      .focus-card.active { display: block; }
      .review-head { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }
      .review-head span, .review-head em { color: var(--fg-2); font-size: 12px; font-style: normal; }
      .gate-badge { display: inline-flex; align-items: center; min-height: 18px; border: 1px solid var(--status-warning-bg); border-radius: 999px; background: var(--status-warning-soft-bg); color: var(--status-warning); padding: 0 7px; font-size: 11px; font-weight: 700; }
      .review-changed-badge { display:inline-flex; align-items:center; min-height:18px; border:1px solid var(--status-warning-bg); border-radius:999px; background:var(--status-warning-bg); color:var(--status-warning); padding:0 7px; font-size:11px; font-weight:750; }
      h2 { margin: 8px 0 6px; font-size: 22px; line-height: 1.2; color: var(--fg-1); }
      .review-explanation { color: var(--fg-2); font-size: 13px; margin: 0 0 12px; }
      .review-pipeline { display: flex; align-items: center; flex-wrap: wrap; gap: 7px 0; overflow: visible; margin: 8px 0 12px; padding: 1px 0 3px; }
      .review-step { display: inline-flex; align-items: center; gap: 6px; min-height: 18px; color: var(--fg-3); font-size: 11px; font-weight: 700; white-space: nowrap; }
      .review-step::before { content: ""; width: 8px; height: 8px; border-radius: 999px; background: var(--grey-3); box-shadow: 0 0 0 3px rgba(200,206,216,.16); }
      .review-step::after { content: ""; width: 24px; height: 1px; margin: 0 8px; background: var(--line); flex: 0 0 24px; }
      .review-step:last-child::after { display: none; }
      .review-step.past::before { background: var(--status-success); box-shadow: 0 0 0 3px rgba(99,211,138,.14); }
      .review-step.active { color: #2f3847; }
      .review-step.active::before { background: var(--blue); box-shadow: 0 0 0 3px rgba(61,116,255,.16); }
      .focus-context { border-top: 1px solid var(--line); padding: 14px 0 0; margin: 12px 0 0; min-width: 0; }
      .review-meta { margin-top: 14px; padding-top: 12px; border-top: 1px solid var(--line); }
      dl { display: grid; grid-template-columns: 120px 1fr; gap: 7px 14px; font-size: 13px; }
      dt { color: var(--fg-3); }
      dd { margin: 0; }
      blockquote { margin: 10px 0 0; border-left: 3px solid var(--border-muted); padding: 8px 10px; color: var(--fg-2); background: var(--surface-subtle); font-size: 13px; line-height: 1.45; }
      .source-snippet { margin-top: 12px; }
      .source-snippet h3 { margin: 0 0 3px; color: var(--fg-2); font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: .04em; }
      .source-meta { margin: 0; color: var(--fg-3); font-size: 11px; }
      .quality-gates { margin: 10px 0 0; border: 1px solid var(--status-warning-bg); border-radius: 7px; background: var(--status-warning-soft-bg); padding: 10px 12px; }
      .quality-gates h3 { margin: 0 0 6px; color: var(--status-warning); font-size: 11px; font-weight: 750; text-transform: uppercase; letter-spacing: .04em; }
      .quality-gates ul { display: grid; gap: 5px; margin: 0; padding: 0; list-style: none; }
      .quality-gates li { display: grid; grid-template-columns: 84px 1fr; gap: 8px; color: var(--fg-2); font-size: 12px; line-height: 1.35; }
      .quality-gates li strong { color: var(--status-warning); font-size: 11px; }
      .quality-gates p { margin: 6px 0 0; color: var(--status-warning); font-size: 12px; }
      .evidence-preview { margin-top: 12px; border: 1px solid var(--line); border-radius: 7px; background: var(--surface-subtle); padding: 10px 12px; }
      .evidence-preview summary { cursor: pointer; font-weight: 650; font-size: 12px; color:var(--fg-2); }
      .evidence-preview ul { list-style: none; padding: 0; margin: 10px 0 0; display: grid; gap: 8px; }
      .evidence-preview li { border-top: 1px solid var(--line); padding-top: 8px; }
      .evidence-preview li:first-child { border-top: 0; padding-top: 0; }
      .evidence-preview strong { font-size: 12px; }
      .evidence-preview span { color: var(--fg-3); font-size: 11px; margin-left: 8px; }
      .evidence-preview p { margin: 4px 0; color:var(--fg-1); font-size:13px; line-height:1.45; }
      .evidence-preview small { display:block; margin: 3px 0; color:var(--fg-3); font-size:11px; }
      .evidence-preview em { color: var(--fg-2); font-size: 12px; font-style: normal; }
      .transcript-lines { margin-top: 8px; display: grid; gap: 5px; }
      .transcript-line { display: grid; grid-template-columns: 52px 1fr; gap: 10px; align-items: start; border-left: 3px solid var(--border-muted); background: var(--surface-subtle); padding: 7px 10px; }
      .transcript-line time { color: var(--fg-3); font-size: 12px; font-variant-numeric: tabular-nums; }
      .transcript-line p { margin: 0; color: var(--fg-2); font-size: 13px; line-height: 1.4; }
      .review-action { display: grid; gap: 12px; min-width: 0; }
      .review-summary { width: 100%; min-width: 0; overflow-wrap: anywhere; font-size: 16px; color: var(--fg-1); background: var(--ai-purple-bg); border-left: 3px solid var(--ai-purple); border-radius: 5px; padding: 12px 14px; margin: 0; }
      .changed-review-field { background:var(--changed-bg) !important; box-shadow:-4px 0 0 var(--changed-bar); }
      .review-summary span { display: block; margin-bottom: 5px; color: var(--fg-2); font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: .04em; }
      .review-summary .review-changed-badge { margin:0 0 7px; width:max-content; }
      .review-summary p { margin: 0; line-height: 1.42; }
      .recommendation-proposal section { margin-top: 10px; }
      .recommendation-proposal section:first-of-type { margin-top: 0; }
      .recommendation-proposal h3 { margin: 0 0 4px; color:var(--fg-2); font-size: 13px; line-height: 1.25; }
      .recommendation-proposal ul { margin: 7px 0 0; padding-left: 18px; display:grid; gap:4px; }
      .recommendation-proposal li { margin:0; line-height:1.35; }
      .review-summary, .review-reason, .source-snippet, .quality-gates, .evidence-preview, .review-meta { user-select: text; -webkit-user-select: text; }
      .review-reason { margin: -2px 0 0; color: var(--fg-2); font-size: 13px; line-height: 1.45; }
      .review-reason span { display: block; margin-bottom: 2px; color: var(--fg-2); font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: .04em; }
      .focus-controls { display: grid; gap: 14px; min-width: 0; }
      textarea { display: block; width: 100%; max-width: 100%; min-width: 0; min-height: 70px; border: 1px solid var(--border-muted); border-radius: 5px; padding: 10px; font: inherit; font-size: 13px; resize: vertical; }
      .decision-row { position: relative; display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }
      .decision-row button { min-height: 36px; border: 1px solid var(--border-muted); border-radius: 5px; background: #fff; color: var(--fg-1); font-weight: 650; cursor: pointer; padding: 0 12px; }
      .decision-row [data-decision] { display: inline-flex; align-items: center; gap: 7px; }
      .decision-row [data-decision] svg { width: 15px; height: 15px; fill: none; stroke: currentColor; stroke-width: 2.4; stroke-linecap: round; stroke-linejoin: round; }
      .decision-row .decision-yes { color: var(--status-success); border-color: var(--status-success-bg); background: var(--status-success-bg); }
      .decision-row .decision-revise { color: var(--status-warning); border-color: var(--status-warning-bg); background: var(--status-warning-soft-bg); }
      .decision-row .decision-no { color: var(--status-danger); border-color: var(--status-danger-bg); background: var(--status-danger-bg); }
      .choice-help { position: relative; display: inline-flex; align-items: center; }
      .decision-row .choice-help-button { width: 22px; min-height: 22px; height: 22px; border-radius: 50%; border-color: var(--border-muted); background: #fff; color: var(--fg-3); padding: 0; display: inline-grid; place-items: center; font-size: 11px; font-weight: 700; line-height: 1; }
      .choice-help-tip { position: absolute; left: 0; bottom: calc(100% + 8px); z-index: 30; display: none; width: min(380px, 80vw); border: 1px solid var(--border-muted); border-radius: 8px; background: #fff; box-shadow: 0 14px 36px rgba(31,43,70,.16); padding: 10px 12px; color: var(--fg-2); font-size: 12px; line-height: 1.45; }
      .choice-help:hover .choice-help-tip, .choice-help:focus-within .choice-help-tip { display: block; }
      .decision-row button:hover, .focus-top button:hover, .focus-top a:hover { border-color: var(--blue-dark); text-decoration: none; }
      .decided { color: var(--status-success); font-weight: 650; font-size: 13px; }
      .decided span { color: var(--fg-3); margin-left: 8px; font-weight: 400; }
      .edit-review { margin-top: 8px; min-height: 28px; border: 1px solid var(--border-muted); border-radius: 5px; background: #fff; color: var(--fg-2); font: inherit; font-size: 12px; font-weight: 650; cursor: pointer; padding: 0 10px; }
      .done { display:none; max-width: 720px; margin: 80px auto; text-align:center; color:var(--fg-2); }
      .done.active { display:block; }
      .doc-reference { display: grid; gap: 2px; color: inherit; text-decoration: none; }
      .doc-reference strong { color: var(--fg-2); font-size: 13px; }
      .doc-reference span { color: var(--fg-3); font-size: 11px; overflow-wrap: anywhere; }
      @media (max-width: 760px) {
        .focus-top { grid-template-columns: 1fr; padding: 10px 14px; }
        .focus-title { text-align: left; }
        .focus-lens { margin: 10px 14px 0; flex-wrap:wrap; }
        .focus-lens em { margin-left:0; }
        .focus-wrap { padding: 14px; }
        dl { grid-template-columns: 1fr; }
      }
    """
    path_attr = html.escape(rel(target))
    path_js = json.dumps(rel(target))
    body = "\n".join(cards) if cards else ""
    return f"""<!doctype html><html><head><title>{display_title}</title><style>{focus_style}</style></head><body><main>
      <header class="focus-top">
        <a class="focus-back" href="/dashboard">← Dashboard</a>
        <div class="focus-title">{display_title}</div>
        <div class="focus-nav"><span class="focus-count" id="focusCount"></span><button type="button" id="prevBtn">← Previous</button><button type="button" id="nextBtn">Next →</button></div>
      </header>
      {lens_notice}
      <section class="focus-wrap">{body}<div class="done" id="doneState"><h2>All reviews handled</h2><p>No open review items remain in this queue.</p></div></section>
      <script>
        const reviewPath = {path_js};
        const cards = Array.from(document.querySelectorAll(".focus-card"));
        const decisionLabels = {{ Approve: "Yes, use this", Revise: "Needs changes", Reject: "No, don't use" }};
        let current = cards.findIndex(card => card.dataset.pending === "true");
        if (current < 0) current = cards.length ? 0 : -1;
        function firstPendingFrom(start) {{
          for (let index = start; index < cards.length; index += 1) {{
            if (cards[index].dataset.pending === "true") return index;
          }}
          for (let index = 0; index < start; index += 1) {{
            if (cards[index].dataset.pending === "true") return index;
          }}
          return -1;
        }}
        function show(index) {{
          cards.forEach(card => card.classList.remove("active"));
          const done = document.getElementById("doneState");
          if (!cards.length || index < 0) {{
            done.classList.add("active");
            document.getElementById("focusCount").textContent = "0 / 0";
            return;
          }}
          current = Math.max(0, Math.min(index, cards.length - 1));
          cards[current].classList.add("active");
          done.classList.remove("active");
          document.getElementById("focusCount").textContent = `${{current + 1}} / ${{cards.length}}`;
          document.getElementById("prevBtn").disabled = current <= 0;
          document.getElementById("nextBtn").disabled = current >= cards.length - 1;
          window.scrollTo(0, 0);
        }}
        async function decide(id, decision) {{
          const notes = document.querySelector(`[data-notes="${{CSS.escape(id)}}"]`);
          const response = await fetch("/api/review-decision", {{
            method: "POST",
            headers: {{ "Content-Type": "application/json" }},
            body: JSON.stringify({{ path: reviewPath, id, decision, notes: notes ? notes.value : "" }})
          }});
          if (!response.ok) {{
            alert(await response.text());
            return;
          }}
          const card = cards[current];
          card.dataset.pending = "false";
          const controls = card.querySelector(".focus-controls");
          controls.innerHTML = `<div class="decided"><div><strong>You answered: ${{decisionLabels[decision] || decision}}</strong></div>${{notes && notes.value ? `<p>${{notes.value.replace(/[&<>"']/g, char => ({{ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }}[char]))}}</p>` : ""}}<button class="edit-review" type="button" data-edit-review="${{id}}">Edit review</button></div>`;
          const next = firstPendingFrom(current + 1);
          if (next >= 0) {{
            show(next);
          }} else {{
            cards.forEach(item => item.classList.remove("active"));
            document.getElementById("doneState").classList.add("active");
            document.getElementById("focusCount").textContent = `${{cards.length}} / ${{cards.length}}`;
          }}
        }}
        document.getElementById("prevBtn").addEventListener("click", () => show(current - 1));
        document.getElementById("nextBtn").addEventListener("click", () => show(current + 1));
        document.addEventListener("click", event => {{
          const decisionButton = event.target.closest("[data-decision]");
          if (decisionButton) {{
            decide(decisionButton.dataset.id, decisionButton.dataset.decision);
            return;
          }}
          const editButton = event.target.closest("[data-edit-review]");
          if (editButton) {{
            const id = editButton.dataset.editReview;
            const template = document.querySelector(`[data-edit-template="${{CSS.escape(id)}}"]`);
            const controls = document.querySelector(`[data-control-for="${{CSS.escape(id)}}"]`);
            if (template && controls) controls.innerHTML = template.innerHTML;
          }}
        }});
        show(current);
      </script>
    </main></body></html>"""


def dashboard_review_page(target: Path, title: str, text: str, base_style: str) -> str:
    items = expanded_review_items(target)
    cards = []
    for item in items:
        pending = item["status"].lower() in {"pending", "proposed", "open"} and not item["decision"]
        question, explanation, hint, summary, evidence_html, meta_html = review_item_context(item, target)
        edit_controls = review_decision_controls(item, hint, textarea_min=True)
        if pending:
            controls = edit_controls
        else:
            labels = {"Approve": "Yes, use this", "Revise": "Needs changes", "Reject": "No, don't use"}
            controls = review_decided_controls(item, labels)
        reason = review_reason_text(item)
        reason_class = "review-reason changed-review-field" if item.get("changed_fields", {}).get("reason") else "review-reason"
        gate_badge = f'<strong class="gate-badge">{int(item.get("gate_count", 0))} quality gate{"s" if int(item.get("gate_count", 0)) != 1 else ""}</strong>' if item.get("gate_count") else ""
        changed_badge = '<strong class="review-changed-badge">Changed since last review</strong>' if item.get("changed_fields") else ""
        cards.append(
            f"""<article class="review-card {'pending-review' if pending else 'decided-review'}">
              <div class="review-head"><span>{html.escape(item['type'])}</span><em>{html.escape(item['id'])}</em>{gate_badge}{changed_badge}</div>
              <h2>{html.escape(question)}</h2>
              <p class="review-explanation">{html.escape(explanation)}</p>
              {review_pipeline_html(item)}
              <div class="review-action">
                {summary}
                <div class="focus-controls" data-control-for="{html.escape(item['id'])}">{controls}</div>
                <template data-edit-template="{html.escape(item['id'])}">{edit_controls}</template>
                <p class="{reason_class}"><span>{html.escape(review_reason_label(item))}</span>{html.escape(reason)}</p>
              </div>
              <div class="review-context">{evidence_html}<div class="review-meta">{meta_html}</div></div>
            </article>"""
        )
    review_style = base_style + """
      *, *::before, *::after { box-sizing: border-box; }
      main { max-width: 1100px; }
      .review-grid { display: grid; gap: 12px; margin-bottom: 20px; }
      .review-card { width: 100%; min-width: 0; overflow: hidden; border: 1px solid var(--line); border-radius: 8px; padding: 12px; background: var(--surface-subtle); }
      .review-card.pending-review { border-color: rgba(124,58,237,.25); }
      .review-head { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }
      .review-head span, .review-head em { color: var(--fg-2); font-size: 12px; font-style: normal; }
      .gate-badge { display: inline-flex; align-items: center; min-height: 17px; border: 1px solid var(--status-warning-bg); border-radius: 999px; background: var(--status-warning-soft-bg); color: var(--status-warning); padding: 0 7px; font-size: 10px; font-weight: 700; }
      .review-changed-badge { display:inline-flex; align-items:center; min-height:17px; border:1px solid var(--status-warning-bg); border-radius:999px; background:var(--status-warning-bg); color:var(--status-warning); padding:0 7px; font-size:10px; font-weight:750; }
      .review-card h2 { margin: 6px 0; font-size: 17px; line-height: 1.2; font-weight: 650; color: var(--fg-1); }
      .review-card p { line-height: 1.45; }
      .review-explanation { color: var(--fg-2); font-size: 12px; margin: 0 0 7px; }
      .review-pipeline { display: flex; align-items: center; flex-wrap: wrap; gap: 7px 0; overflow: visible; margin: 7px 0 10px; padding: 1px 0 3px; }
      .review-step { display: inline-flex; align-items: center; gap: 6px; min-height: 18px; color: var(--fg-3); font-size: 11px; font-weight: 700; white-space: nowrap; }
      .review-step::before { content: ""; width: 8px; height: 8px; border-radius: 999px; background: var(--grey-3); box-shadow: 0 0 0 3px rgba(200,206,216,.16); }
      .review-step::after { content: ""; width: 24px; height: 1px; margin: 0 8px; background: var(--line); flex: 0 0 24px; }
      .review-step:last-child::after { display: none; }
      .review-step.past::before { background: var(--status-success); box-shadow: 0 0 0 3px rgba(99,211,138,.14); }
      .review-step.active { color: #2f3847; }
      .review-step.active::before { background: var(--blue); box-shadow: 0 0 0 3px rgba(61,116,255,.16); }
      .review-summary { width: 100%; min-width: 0; overflow-wrap: anywhere; font-size: 14px; color: var(--fg-1); background: var(--ai-purple-bg); border-left: 3px solid var(--ai-purple); border-radius: 5px; padding: 8px 10px; }
      .changed-review-field { background:var(--changed-bg) !important; box-shadow:-4px 0 0 var(--changed-bar); }
      .review-summary span { display: block; margin-bottom: 4px; color: var(--fg-2); font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: .04em; }
      .review-summary .review-changed-badge { margin:0 0 6px; width:max-content; }
      .review-summary p { margin: 0; line-height: 1.42; }
      .recommendation-proposal section { margin-top: 9px; }
      .recommendation-proposal section:first-of-type { margin-top: 0; }
      .recommendation-proposal h3 { margin: 0 0 4px; color:var(--fg-2); font-size: 12px; line-height: 1.25; }
      .recommendation-proposal ul { margin: 6px 0 0; padding-left: 18px; display:grid; gap:3px; }
      .recommendation-proposal li { margin:0; line-height:1.35; }
      .learning-impact { display: grid; gap: 8px; }
      .learning-impact section { border: 1px solid var(--line); border-radius: 6px; background: #fff; padding: 9px 10px; }
      .learning-impact h3 { margin: 0 0 4px; color: var(--fg-2); font-size: 11px; font-weight: 750; text-transform: uppercase; letter-spacing: .04em; }
      .learning-impact p { margin: 0; color: var(--fg-2); font-size: 13px; line-height: 1.45; }
      .review-summary, .review-reason, .source-snippet, .quality-gates, .evidence-preview, .review-meta { user-select: text; -webkit-user-select: text; }
      .review-action { margin-top: 10px; display: grid; gap: 8px; }
      .review-context { margin-top: 10px; min-width: 0; }
      .review-meta { margin-top: 12px; padding-top: 10px; border-top: 1px solid var(--line); }
      blockquote { margin: 8px 0; border-left: 3px solid var(--border-muted); padding: 6px 10px; color: var(--fg-2); background: #fff; font-size: 13px; line-height: 1.45; }
      .review-reason { margin: -2px 0 0; color: var(--fg-2); font-size: 12px; line-height: 1.45; }
      .review-reason span { display: block; margin-bottom: 2px; color: var(--fg-2); font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: .04em; }
      dl { display: grid; grid-template-columns: 110px 1fr; gap: 6px 12px; font-size: 12px; }
      dt { color: var(--fg-3); }
      dd { margin: 0; }
      .source-snippet { margin-top: 10px; }
      .source-snippet h3 { margin: 0 0 3px; color: var(--fg-2); font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: .04em; }
      .source-meta { margin: 0; color: var(--fg-3); font-size: 11px; }
      .quality-gates { margin: 9px 0 0; border: 1px solid var(--status-warning-bg); border-radius: 6px; background: var(--status-warning-soft-bg); padding: 8px 10px; }
      .quality-gates h3 { margin: 0 0 5px; color: var(--status-warning); font-size: 10px; font-weight: 750; text-transform: uppercase; letter-spacing: .04em; }
      .quality-gates ul { display: grid; gap: 5px; margin: 0; padding: 0; list-style: none; }
      .quality-gates li { display: grid; grid-template-columns: 76px 1fr; gap: 8px; color: var(--fg-2); font-size: 12px; line-height: 1.35; }
      .quality-gates li strong { color: var(--status-warning); font-size: 10px; }
      .quality-gates p { margin: 6px 0 0; color: var(--status-warning); font-size: 11px; }
      .transcript-lines { margin-top: 8px; display: grid; gap: 5px; }
      .transcript-line { display: grid; grid-template-columns: 52px 1fr; gap: 10px; align-items: start; border-left: 3px solid var(--border-muted); background: #fff; padding: 7px 10px; }
      .transcript-line time { color: var(--fg-3); font-size: 12px; font-variant-numeric: tabular-nums; }
      .transcript-line p { margin: 0; color: var(--fg-2); font-size: 13px; line-height: 1.4; }
      .doc-reference { display: grid; gap: 2px; color: inherit; text-decoration: none; }
      .doc-reference strong { color: var(--fg-2); font-size: 12px; }
      .doc-reference span { color: var(--fg-3); font-size: 11px; overflow-wrap: anywhere; }
      a.doc-reference:hover strong { color: var(--blue-dark); text-decoration: underline; }
      .evidence-preview { margin-top: 12px; border: 1px solid var(--line); border-radius: 6px; background: #fff; padding: 10px 12px; }
      .evidence-preview summary { cursor: pointer; font-weight: 650; font-size: 12px; }
      .evidence-preview ul { list-style: none; padding: 0; margin: 10px 0 0; display: grid; gap: 8px; }
      .evidence-preview li { border-top: 1px solid var(--line); padding-top: 8px; }
      .evidence-preview li:first-child { border-top: 0; padding-top: 0; }
      .evidence-preview strong { font-size: 12px; }
      .evidence-preview span { color: var(--fg-3); font-size: 11px; margin-left: 8px; }
      .evidence-preview p { margin: 4px 0; }
      .evidence-preview small { display:block; margin: 3px 0; color:var(--fg-3); font-size:11px; }
      .evidence-preview em { color: var(--fg-2); font-size: 12px; font-style: normal; }
      .preview-more { color: var(--fg-3); font-size: 12px; margin-top: 8px; }
      textarea { display: block; width: 100%; max-width: 100%; min-width: 0; min-height: 48px; border: 1px solid var(--border-muted); border-radius: 4px; padding: 8px; font: inherit; font-size: 12px; resize: vertical; }
      .decision-row { position: relative; display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
      button { min-height: 32px; border: 1px solid var(--border-muted); border-radius: 4px; background: #fff; color: var(--fg-1); font-weight: 650; cursor: pointer; padding: 0 10px; }
      .decision-row [data-decision] { display: inline-flex; align-items: center; gap: 7px; }
      .decision-row [data-decision] svg { width: 14px; height: 14px; fill: none; stroke: currentColor; stroke-width: 2.4; stroke-linecap: round; stroke-linejoin: round; }
      .decision-row .decision-yes { color: var(--status-success); border-color: var(--status-success-bg); background: var(--status-success-bg); }
      .decision-row .decision-revise { color: var(--status-warning); border-color: var(--status-warning-bg); background: var(--status-warning-soft-bg); }
      .decision-row .decision-no { color: var(--status-danger); border-color: var(--status-danger-bg); background: var(--status-danger-bg); }
      .choice-help { position: relative; display: inline-flex; align-items: center; }
      .decision-row .choice-help-button { width: 20px; min-height: 20px; height: 20px; border-radius: 50%; border-color: var(--border-muted); background: #fff; color: var(--fg-3); padding: 0; display: inline-grid; place-items: center; font-size: 10px; font-weight: 700; line-height: 1; }
      .choice-help-tip { position: absolute; left: 0; bottom: calc(100% + 8px); z-index: 30; display: none; width: min(360px, 80vw); border: 1px solid var(--border-muted); border-radius: 8px; background: #fff; box-shadow: 0 14px 36px rgba(31,43,70,.16); padding: 10px 12px; color: var(--fg-2); font-size: 12px; line-height: 1.45; }
      .choice-help:hover .choice-help-tip, .choice-help:focus-within .choice-help-tip { display: block; }
      button:hover { border-color: var(--blue-dark); }
      .decided { margin-top: 12px; color: var(--status-success); font-weight: 650; font-size: 12px; }
      .decided span { color: var(--fg-3); margin-left: 8px; font-weight: 400; }
      .decided p { color: var(--fg-2); font-weight: 400; margin: 6px 0 0; }
      .edit-review { margin-top: 8px; min-height: 26px; border: 1px solid var(--border-muted); border-radius: 4px; background: #fff; color: var(--fg-2); font: inherit; font-size: 11px; font-weight: 650; cursor: pointer; padding: 0 8px; }
      .raw { margin-top: 24px; }
    """
    body = "\n".join(cards) if cards else "<p>No review items found.</p>"
    path_attr = html.escape(rel(target))
    return f"""<!doctype html><html><head><title>{title}</title><style>{review_style}</style></head><body><main><h1>{title}</h1>
      <section class="review-grid">{body}</section>
      <details class="raw"><summary>Raw Markdown</summary><pre>{html.escape(text)}</pre></details>
      <script>
        async function decide(id, decision) {{
          const notes = document.querySelector(`[data-notes="${{CSS.escape(id)}}"]`);
          const response = await fetch("/api/review-decision", {{
            method: "POST",
            headers: {{ "Content-Type": "application/json" }},
            body: JSON.stringify({{ path: "{path_attr}", id, decision, notes: notes ? notes.value : "" }})
          }});
          if (!response.ok) {{
            alert(await response.text());
            return;
          }}
          location.reload();
        }}
        document.querySelectorAll("[data-decision]").forEach(button => {{
          button.addEventListener("click", () => decide(button.dataset.id, button.dataset.decision));
        }});
        document.querySelectorAll("[data-edit-review]").forEach(button => {{
          button.addEventListener("click", () => {{
            const id = button.dataset.editReview;
            const template = document.querySelector(`[data-edit-template="${{CSS.escape(id)}}"]`);
            const controls = document.querySelector(`[data-control-for="${{CSS.escape(id)}}"]`);
            if (template && controls) controls.innerHTML = template.innerHTML;
            controls.querySelectorAll("[data-decision]").forEach(nextButton => {{
              nextButton.addEventListener("click", () => decide(nextButton.dataset.id, nextButton.dataset.decision));
            }});
          }});
        }});
        window.addEventListener("load", () => {{
          const firstPending = document.querySelector(".pending-review");
          if (firstPending) {{
            firstPending.scrollIntoView({{ block: "start" }});
          }}
        }});
      </script>
    </main></body></html>"""


DASHBOARD_HTML = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#FBFBFA">
  <meta name="apple-mobile-web-app-title" content="Research OS">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <link rel="manifest" href="/manifest.webmanifest">
  <link rel="icon" href="/app-icon.svg?v=4" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/assets/app-icon.png?v=4">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;600;700&display=swap" rel="stylesheet">
  <title>Research OS Dashboard</title>
  <style>
    :root {
      --bg-1: #ffffff; --bg-2: #F4F5F7; --surface: #ffffff; --surface-muted: #F4F5F7; --surface-subtle: #FBFBFA; --grey-0: #ffffff; --grey-3: #E2E0DF;
      --fg-1: #222222; --fg-2: #575654; --fg-3: #9A9997; --border-1: #E2E0DF; --border-muted: #D8DFEB;
      --blue: #3D74FF; --blue-dark: #194FCF; --ai-purple: #7C3AED; --ai-purple-dark: #4C1D95; --ai-purple-bg: #F4EFFF;
      --red: #C1002F; --red-dark: #680814; --green: #00893F;
      --status-success: #00893F; --status-success-bg: #D5F4E3;
      --status-warning: #9A6200; --status-warning-bg: #FFF3C4; --status-warning-soft-bg: #FFF9E8; --status-warning-bar: #F2B83B;
      --status-danger: #C1002F; --status-danger-bg: #F9D8DF;
      --changed-bg: #FFF4BD; --changed-bar: #F5D84F;
      --bg: var(--bg-2); --panel: var(--bg-1); --line: var(--border-1); --text: var(--fg-1); --muted: var(--fg-3);
      --yellow: var(--status-warning); --gray: var(--grey-3);
      --shadow-small-bottom: 0 2px 8px rgba(34, 34, 34, .06);
      --shadow: none;
    }
    * { box-sizing: border-box; }
    body { margin: 0; min-height: 100vh; background: var(--panel); color: var(--text); font-family: Roboto, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; letter-spacing: .003em; font-size: 14px; }
    .shell { width: 100%; min-height: 100vh; margin: 0; padding: 0; }
    .topbar { position: sticky; top: 0; z-index: 40; height: 56px; display: flex; align-items: center; justify-content: space-between; gap:18px; background: rgba(255,255,255,.94); border-bottom: 1px solid var(--line); padding: 0 18px; box-shadow: var(--shadow); backdrop-filter: blur(12px); }
    .brand { display:flex; align-items:center; gap:12px; font-weight: 650; }
    .mark { width: 24px; height: 24px; border-radius: 6px; color: transparent; background: url('/assets/app-icon.png?v=4') center / contain no-repeat; display:flex; align-items:center; justify-content:center; font-size:0; line-height:1; padding:0; overflow:hidden; }
    .top-status { display:flex; align-items:center; gap:10px; min-width:0; }
    .updated { color: var(--muted); font-size: 12px; white-space:nowrap; display:inline-flex; align-items:center; gap:6px; min-width:104px; justify-content:flex-end; }
    .dashboard-loading { min-height: 260px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:12px; border:1px dashed var(--border-1); border-radius:12px; background:#fff; color:var(--muted); }
    .dashboard-loading-icon { display:inline-flex; align-items:center; justify-content:center; width:44px; height:44px; border-radius:999px; border:1px solid #dbe5f5; background:#f7f9fd; font-size:24px; line-height:1; transform-origin:center; animation: hourglass-pulse 900ms ease-in-out infinite; }
    .dashboard-loading-text { font-size:13px; font-weight:650; color:var(--fg-2); }
    @keyframes hourglass-pulse { 0%, 100% { opacity:.45; transform:scale(.96); } 50% { opacity:1; transform:scale(1.06); } }
    .backup-status { height:26px; display:inline-flex; align-items:center; gap:7px; border:1px solid var(--line); border-radius:999px; background:#fff; padding:0 8px; color:var(--fg-2); font-size:11px; white-space:nowrap; }
    .backup-status[hidden], .backup-button[hidden] { display:none; }
    .backup-status.yellow { border-color:var(--status-warning-bg); background:var(--status-warning-bg); color:var(--status-warning); }
    .backup-status.green { border-color:var(--status-success-bg); background:var(--status-success-bg); color:var(--status-success); }
    .backup-status.red { border-color:var(--status-danger-bg); background:var(--status-danger-bg); color:var(--status-danger); }
    .version-button { height:26px; border:1px solid var(--status-warning-bg); border-radius:999px; background:var(--status-warning-bg); color:var(--status-warning); padding:0 10px; font:inherit; font-size:11px; font-weight:750; cursor:pointer; white-space:nowrap; }
    .version-button[hidden] { display:none; }
    .version-button:hover { border-color:var(--status-warning-bar); background:var(--status-warning-soft-bg); }
    .backup-button { height:26px; border:1px solid var(--border-1); border-radius:12px; background:#fff; color:var(--fg-2); padding:0 9px; font:inherit; font-size:11px; font-weight:650; cursor:pointer; white-space:nowrap; }
    .backup-button:hover { border-color:var(--blue-dark); color:var(--blue-dark); }
    .backup-button:disabled { opacity:.55; cursor:default; }
    .layout { display: grid; grid-template-columns: 64px 1fr; align-items:start; min-height: calc(100vh - 56px); background: var(--panel); box-shadow: var(--shadow); }
    .rail { position: sticky; top: 56px; z-index: 30; width: 64px; height: calc(100vh - 56px); border-right: 1px solid var(--line); padding: 18px 0 18px; display:flex; flex-direction:column; align-items:stretch; gap:0; color: var(--fg-2); background: var(--panel); overflow-y:auto; }
    .rail-tab { width: 100%; height: 48px; border-radius: 0; border: 0; background: transparent; color: var(--fg-2); display:flex; align-items:center; justify-content:center; cursor:pointer; padding:0; }
    .rail-tab:hover { background:#FBFBFA; color:var(--fg-1); }
    .rail-tab.active { color: var(--blue); background: #F2F6FF; }
    .rail-icon { width: 24px; height: 24px; display:block; flex:0 0 auto; background: currentColor; -webkit-mask: var(--icon) center / 24px 24px no-repeat; mask: var(--icon) center / 24px 24px no-repeat; }
    .rail-spacer { flex: 1 1 auto; min-height: 18px; }
    main { padding: 22px 34px 42px; min-width: 0; }
    h1 { margin:0; font-size: 24px; font-weight: 700; color: var(--fg-1); line-height: 1.2; }
    .toolbar { display:flex; align-items:center; justify-content:space-between; gap:12px; margin: 0 0 14px; }
    .toolbar-left { display:flex; align-items:center; gap:10px; min-width:0; }
    .toolbar-actions { display:flex; align-items:center; gap:8px; }
    .tab-panel { display:none; }
    .tab-panel.active { display:block; }
    .search { width: 260px; max-width: 100%; height: 34px; border: 1px solid var(--line); border-radius: 8px; padding: 0 12px; color: var(--text); outline: none; background: #fff; }
    .toolbar-status { display:flex; align-items:center; gap:8px; color:var(--muted); font-size:12px; }
    .manual-refresh { height:32px; display:inline-flex; align-items:center; gap:7px; border:1px solid var(--blue); border-radius:999px; background:#fff; color:var(--blue); padding:0 13px; font:inherit; font-size:12px; font-weight:750; cursor:pointer; box-shadow:var(--shadow-small-bottom); white-space:nowrap; }
    .manual-refresh:hover { border-color:var(--blue-dark); color:var(--blue-dark); background:#F2F6FF; }
    .manual-refresh:disabled { opacity:.6; cursor:default; }
    .manual-refresh-icon { width:14px; height:14px; display:inline-block; flex:0 0 auto; }
    .learning-top-grid { display:grid; grid-template-columns:repeat(2, minmax(0, 1fr)); gap:12px; align-items:stretch; margin-bottom:12px; }
    .learning-detail-grid { display:grid; grid-template-columns:repeat(2, minmax(0, 1fr)); gap:12px; align-items:stretch; }
    .learning-detail-grid > .learning-card { height:100%; }
    .learning-analysis-stack { display:grid; grid-template-rows:auto 1fr; gap:12px; min-width:0; height:100%; }
    .learning-analysis-stack .learning-section { margin-bottom:0; }
    .learning-card { border:1px solid var(--line); border-radius:12px; background:#fff; padding:14px; box-shadow: var(--shadow-small-bottom); min-width:0; overflow:hidden; }
    .learning-card h2 { margin:0 0 7px; color:var(--fg-1); font-size:17px; line-height:1.2; }
    .learning-card p { margin:0; color:var(--fg-2); font-size:13px; line-height:1.45; }
    .learning-card strong { display:block; font-size:22px; line-height:1; font-weight:650; color:var(--fg-1); }
    .learning-card > span { display:block; margin-top:7px; color:var(--muted); font-size:12px; }
    .learning-card .trend { margin-top:8px; font-size:11px; font-weight:700; color:var(--fg-3); }
    .learning-card .trend.up { color:var(--status-warning); }
    .learning-card .trend.down { color:var(--status-success); }
    .learning-card .trend.flat { color:var(--fg-2); }
    .learning-card .trend.attention { color:var(--status-warning); }
    .learning-card .trend.good { color:var(--status-success); }
    .learning-status-line { display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-top:10px; }
    .learning-status-line .phase-status { flex:0 0 auto; width:max-content; max-width:100%; line-height:1; }
    .learning-status-metrics { display:grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap:8px; margin-top:12px; }
    .learning-mini-metric { border:1px solid var(--line); border-radius:10px; padding:9px 10px; background:var(--surface-subtle); min-width:0; }
    .learning-mini-metric strong { font-size:18px; }
    .learning-mini-metric span { font-size:11px; line-height:1.25; }
    .learning-recent-list { display:grid; gap:0; margin:10px 0 0; padding:0; list-style:none; }
    .learning-recent-item { display:grid; grid-template-columns:22px 1fr; gap:8px; border-top:1px solid var(--line); padding:9px 0; }
    .learning-recent-item:first-child { border-top:0; padding-top:0; }
    .learning-recent-number { width:22px; height:22px; border-radius:999px; display:grid; place-items:center; background:var(--surface-subtle); border:1px solid var(--line); color:var(--fg-2); font-size:11px; font-weight:700; line-height:1; }
    .learning-recent-item strong { font-size:12px; line-height:1.25; color:var(--fg-1); }
    .learning-recent-item p { margin-top:3px; color:var(--fg-2); font-size:12px; line-height:1.35; }
    .learning-more-link { display:inline-flex; width:max-content; margin-top:8px; color:var(--blue); font-size:12px; font-weight:650; text-decoration:none; }
    .learning-more-link:hover { color:var(--blue-dark); text-decoration:underline; }
    .learning-context-card { margin-bottom:0; }
    .learning-context-card h2 { margin-bottom:6px; }
    .learning-context-summary { max-width:980px; color:var(--fg-1); font-size:13px; line-height:1.45; }
    .learning-context-points { display:grid; grid-template-columns:1fr; gap:8px; margin-top:10px; }
    .learning-context-point { border:1px solid var(--line); border-radius:10px; background:var(--surface-subtle); padding:9px 10px; color:var(--fg-2); font-size:12px; line-height:1.35; }
    .learning-context-point span { display:block; margin:0 0 5px; color:var(--fg-3); font-size:10px; font-weight:750; text-transform:uppercase; letter-spacing:.003em; }
    .learning-context-trend { margin-top:10px; border-left:3px solid var(--status-warning-bar); background:var(--status-warning-soft-bg); padding:8px 10px; color:var(--fg-2); font-size:12px; line-height:1.4; }
    .learning-context-trend span { display:block; margin:0 0 2px; color:var(--status-warning); font-size:10px; font-weight:750; text-transform:uppercase; letter-spacing:.003em; }
    .learning-section { position:relative; border:1px solid var(--line); border-radius:12px; background:#fff; margin-bottom:12px; overflow:visible; box-shadow: var(--shadow-small-bottom); }
    .learning-section-head { min-height:42px; display:flex; justify-content:space-between; align-items:center; gap:12px; padding:10px 14px; border-bottom:1px solid var(--line); }
    .learning-section-title { font-size:13px; line-height:1.25; font-weight:700; color:var(--fg-1); }
    .mini-sub { margin-top:4px; color:var(--muted); font-size:12px; line-height:1.35; font-weight:400; }
    .learning-list { display:grid; gap:0; }
    .learning-row { display:grid; grid-template-columns: 1fr auto; gap:12px; align-items:center; min-height:38px; padding:0 14px; border-bottom:1px solid #f1f3f7; font-size:12px; }
    .learning-row:last-child { border-bottom:0; }
    .learning-row span { color:var(--muted); }
    .learning-row .trend { color:var(--fg-2); font-size:12px; font-weight:400; }
    .learning-quality-row { grid-template-columns: 190px 1fr 148px; padding:9px 14px; }
    .learning-rate { display:grid; gap:5px; }
    .learning-rate-bar { height:8px; border-radius:999px; overflow:hidden; background:var(--grey-3); display:flex; }
    .learning-rate-good { background:var(--status-success); }
    .learning-rate-iterated { background:var(--status-warning-bar); }
    .learning-rate-meta { display:flex; justify-content:space-between; gap:10px; color:var(--fg-3); font-size:11px; }
    .settings-grid { display:grid; gap:12px; max-width:860px; }
    .settings-card { border:1px solid var(--line); border-radius:12px; background:#fff; box-shadow:var(--shadow-small-bottom); padding:14px; }
    .settings-card h2 { margin:0 0 4px; font-size:14px; line-height:1.25; color:var(--fg-1); }
    .settings-card p { margin:0 0 12px; color:var(--muted); font-size:12px; line-height:1.4; }
    .settings-card.update-card.yellow { border-color:var(--status-warning-bg); background:var(--status-warning-soft-bg); }
    .settings-card.update-card.green { border-color:var(--status-success-bg); }
    .update-meta-grid { display:grid; grid-template-columns:repeat(3, minmax(0, 1fr)); gap:8px; margin:10px 0 12px; }
    .update-meta-item { border:1px solid var(--line); border-radius:10px; background:#fff; padding:9px 10px; min-width:0; }
    .update-meta-item span { display:block; margin-bottom:4px; color:var(--fg-3); font-size:10px; font-weight:750; text-transform:uppercase; letter-spacing:.003em; }
    .update-meta-item strong { display:block; color:var(--fg-1); font-size:12px; line-height:1.25; overflow-wrap:anywhere; }
    .update-command { margin:8px 0 0; border:1px solid var(--line); border-radius:10px; background:#fff; padding:10px; color:var(--fg-1); font:12px/1.45 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; white-space:pre-wrap; overflow-wrap:anywhere; }
    .update-actions { display:flex; gap:8px; align-items:center; flex-wrap:wrap; margin-top:10px; }
    .settings-link { height:28px; display:inline-flex; align-items:center; border:1px solid var(--border-1); border-radius:8px; background:#fff; color:var(--fg-2); padding:0 10px; font-size:12px; font-weight:650; text-decoration:none; }
    .settings-link:hover { border-color:var(--blue-dark); color:var(--blue-dark); text-decoration:none; }
    .settings-form { display:grid; gap:12px; }
    .settings-field { display:grid; gap:5px; }
    .settings-field label { color:var(--fg-2); font-size:12px; font-weight:700; }
    .settings-field input, .settings-field select { width:100%; min-width:0; height:34px; border:1px solid var(--line); border-radius:8px; background:#fff; color:var(--fg-1); padding:0 10px; font:inherit; font-size:12px; }
    .settings-field select { appearance:auto; }
    .settings-field input[readonly] { background:var(--bg-2); color:var(--fg-3); }
    .settings-path-display { min-height:34px; display:flex; align-items:center; width:100%; min-width:0; border:1px solid var(--line); border-radius:8px; background:var(--bg-2); color:var(--fg-2); padding:7px 10px; font-size:12px; line-height:1.35; overflow-wrap:anywhere; }
    .settings-meta { color:var(--muted); font-size:11px; line-height:1.35; }
    .settings-toggle { display:flex; align-items:flex-start; gap:9px; padding:10px; border:1px solid var(--line); border-radius:10px; background:var(--surface-subtle); }
    .settings-toggle input { width:16px; height:16px; margin:1px 0 0; flex:0 0 auto; accent-color:var(--ai-purple); }
    .settings-toggle strong { display:block; color:var(--fg-1); font-size:12px; line-height:1.25; }
    .settings-toggle span { display:block; margin-top:3px; color:var(--muted); font-size:11px; line-height:1.35; }
    .settings-actions { display:flex; gap:8px; align-items:center; flex-wrap:wrap; }
    .settings-save, .settings-reset { height:28px; border:1px solid var(--border-1); border-radius:8px; background:#fff; color:var(--fg-2); padding:0 10px; font:inherit; font-size:12px; font-weight:650; cursor:pointer; }
    .settings-save { border-color:rgba(124,58,237,.35); color:var(--ai-purple); }
    .settings-save:hover, .settings-reset:hover { border-color:var(--blue-dark); color:var(--blue-dark); }
    .settings-note-list { display:grid; gap:7px; margin:0; padding:0; list-style:none; }
    .settings-note-list li { color:var(--fg-2); font-size:12px; line-height:1.4; }
    .onboarding { display:grid; gap:12px; max-width:1120px; }
    .onboarding-hero { border:1px solid var(--line); border-radius:12px; background:#fff; box-shadow:var(--shadow-small-bottom); padding:18px; display:grid; grid-template-columns:1fr 280px; gap:18px; align-items:center; overflow:hidden; }
    .onboarding-hero h2 { margin:0; color:var(--fg-1); font-size:20px; line-height:1.2; }
    .onboarding-hero p { margin:8px 0 0; max-width:760px; color:var(--fg-2); font-size:13px; line-height:1.45; }
    .onboarding-hero .phase-status { margin-top:12px; }
    .onboarding-mini-dashboard { border:1px solid var(--line); border-radius:12px; background:var(--surface-subtle); padding:10px; display:grid; gap:8px; }
    .onboarding-mini-head { min-height:28px; display:flex; align-items:center; justify-content:space-between; gap:8px; }
    .onboarding-mini-title { font-size:12px; font-weight:750; color:var(--fg-1); }
    .onboarding-stage { display:grid; grid-template-columns:92px 1fr auto; gap:8px; align-items:center; min-height:26px; font-size:11px; color:var(--fg-2); }
    .onboarding-stage strong { font-size:11px; color:var(--fg-2); }
    .onboarding-stage .bar { height:6px; }
    .onboarding-grid { display:grid; grid-template-columns:repeat(2, minmax(0, 1fr)); gap:12px; }
    .onboarding-card { border:1px solid var(--line); border-radius:12px; background:#fff; box-shadow:var(--shadow-small-bottom); padding:14px; min-width:0; display:grid; gap:10px; align-content:start; }
    .onboarding-card h3 { margin:0 0 8px; color:var(--fg-1); font-size:14px; line-height:1.25; }
    .onboarding-card p { margin:0; color:var(--fg-2); font-size:12px; line-height:1.45; }
    .onboarding-card ul, .onboarding-card ol { margin:0; padding-left:18px; color:var(--fg-2); font-size:12px; line-height:1.45; }
    .onboarding-card li + li { margin-top:5px; }
    .onboarding-card strong { color:var(--fg-1); }
    .onboarding-info-card { border-color:rgba(61,116,255,.2); background:linear-gradient(180deg, #fff 0%, #F7FAFF 100%); }
    .onboarding-sidebar-demo { display:grid; grid-template-columns:52px 1fr; gap:12px; align-items:center; }
    .demo-rail { width:46px; height:154px; border:1px solid var(--line); border-radius:14px; background:#fff; overflow:hidden; display:flex; flex-direction:column; box-shadow:var(--shadow-small-bottom); }
    .demo-tab { height:34px; display:grid; place-items:center; border-bottom:1px solid var(--line); color:var(--fg-3); }
    .demo-spacer { flex:1 1 auto; min-height:18px; border-bottom:1px solid var(--line); }
    .demo-info { background:#F1F5FF; color:var(--blue); }
    .demo-info .rail-icon { width:18px; height:18px; -webkit-mask-size:18px 18px; mask-size:18px 18px; }
    .demo-arrow { color:var(--blue); font-size:12px; font-weight:750; line-height:1.3; display:flex; align-items:center; gap:8px; }
    .demo-arrow::before { content:""; width:26px; height:2px; border-radius:999px; background:var(--blue); display:block; box-shadow:-6px -4px 0 -3px var(--blue), -6px 4px 0 -3px var(--blue); }
    .onboarding-actions { display:flex; gap:8px; align-items:center; flex-wrap:wrap; margin-top:12px; }
    .onboarding-folder-card { border:1px solid var(--line); border-radius:10px; background:var(--surface-subtle); overflow:hidden; }
    .onboarding-folder-row { display:grid; grid-template-columns:8px 1fr auto; gap:8px; align-items:center; min-height:34px; padding:0 10px; border-bottom:1px solid var(--line); font-size:12px; color:var(--fg-2); }
    .onboarding-folder-row:last-child { border-bottom:0; }
    .onboarding-folder-row strong { color:var(--fg-1); font-size:12px; }
    .onboarding-pill-list { display:flex; flex-wrap:wrap; gap:6px; }
    .onboarding-pill { min-height:24px; display:inline-flex; align-items:center; border:1px solid var(--line); border-radius:999px; background:#fff; padding:0 9px; color:var(--fg-2); font-size:11px; font-weight:650; }
    .learning-intro { margin-bottom:12px; }
    .project { border: 1px solid var(--line); border-radius: 12px; margin-bottom: 12px; overflow: visible; background: #fff; box-shadow: var(--shadow-small-bottom); }
    .row { display:grid; grid-template-columns: 28px 1fr auto; gap: 12px; align-items:center; min-height: 58px; padding: 11px 14px; border-bottom: 1px solid var(--line); }
    .project > .row { grid-template-columns: 28px 46px 1fr auto; }
    .round .row { grid-template-columns: 28px 1fr auto auto; min-height: 50px; padding-left: 34px; background: #fff; }
    .round.round-muted .name, .round.round-muted .meta { color: var(--fg-3); }
    .round-monitor-cell { display:flex; align-items:center; justify-content:flex-end; min-width:48px; }
    .monitor-switch { position:relative; display:inline-flex; align-items:center; width:38px; height:22px; cursor:pointer; }
    .monitor-switch input { position:absolute; opacity:0; width:1px; height:1px; }
    .monitor-switch-track { width:38px; height:22px; border:1px solid var(--border-1); border-radius:999px; background:var(--surface-muted); transition:background .16s ease, border-color .16s ease; }
    .monitor-switch-track::after { content:""; position:absolute; top:3px; left:3px; width:16px; height:16px; border-radius:50%; background:#fff; box-shadow:0 1px 3px rgba(31,41,55,.22); transition:transform .16s ease; }
    .monitor-switch input:checked + .monitor-switch-track { border-color:rgba(45,140,99,.35); background:var(--status-success-bg); }
    .monitor-switch input:checked + .monitor-switch-track::after { transform:translateX(16px); }
    .monitor-switch input:focus-visible + .monitor-switch-track { outline:2px solid var(--blue); outline-offset:2px; }
    .monitor-switch input:disabled + .monitor-switch-track { opacity:.6; cursor:wait; }
    .toggle { width: 24px; height: 24px; border: 0; background: transparent; color: var(--fg-3); font-size: 17px; cursor: pointer; line-height: 1; display:grid; place-items:center; border-radius:4px; }
    .toggle:hover { background:#FBFBFA; color:var(--fg-2); }
    .project-icon { width: 42px; height: 42px; border-radius: 10px; display:grid; place-items:center; font-size: 24px; background: #fff; border: 1px solid var(--border-1); box-shadow: var(--shadow-small-bottom); }
    .title { min-width: 0; }
    .name { font-size: 14px; font-weight: 600; color: var(--fg-1); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .meta { color: var(--fg-2); font-size: 12px; margin-top: 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .badges { display:flex; gap:8px; align-items:center; flex-wrap: wrap; justify-content:flex-end; }
    .badge { height: 26px; display:inline-flex; align-items:center; gap: 6px; border: 1px solid var(--line); border-radius: 999px; padding: 0 10px; font-size: 11px; color: var(--fg-2); background: #fff; }
    .badge.green { border-color: var(--status-success-bg); background: var(--status-success-bg); color: var(--status-success); }
    .badge.yellow { border-color: var(--status-warning-bg); background: var(--status-warning-bg); color: var(--status-warning); }
    .badge.red { border-color: var(--status-danger-bg); background: var(--status-danger-bg); color: var(--status-danger); }
    .badge.gray { color: var(--fg-3); background: #fff; }
    .dot { width: 7px; height: 7px; border-radius: 50%; display:inline-block; }
    .dot.green, .green > .dot { background: var(--status-success); }
    .dot.yellow, .yellow > .dot { background: var(--status-warning); }
    .dot.red, .red > .dot { background: var(--status-danger); }
    .dot.gray, .gray > .dot { background: var(--grey-3); }
    .dot.blue, .blue > .dot { background: var(--blue); }
    .fill.green { background: var(--green); }
    .fill.yellow { background: var(--status-warning-bar); }
    .fill.blue { background: var(--blue); }
    .fill.red { background: var(--red); }
    .fill.gray { background: var(--grey-3); }
    .project-body, .round-body { display:none; }
    .open > .project-body, .open > .round-body { display:block; }
    .project-info-section { border-bottom: 1px solid var(--line); }
    .project-info-row, .rounds-head { display:grid; grid-template-columns: 28px 1fr auto; gap:12px; align-items:center; min-height: 46px; padding: 0 14px; background: var(--bg-2); border-bottom: 1px solid var(--line); }
    .project-info-title, .rounds-title { font-size: 12px; font-weight: 700; color: var(--fg-1); }
    .project-info-sub, .rounds-sub { color: var(--fg-3); font-size: 12px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .project-info-section .project-stack { display:none; }
    .project-info-section.open .project-stack { display:grid; }
    .project-stack { display:grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; padding: 12px 14px; background:#fff; }
    .project-part { min-height: 86px; border: 1px solid var(--line); border-radius: 12px; padding: 16px; display:flex; flex-direction:column; justify-content:space-between; gap:10px; background: #fff; box-shadow: var(--shadow-small-bottom); }
    .project-part-main { min-width:0; }
    .project-part-title { font-size: 13px; font-weight: 700; color:var(--fg-1); }
    .project-part-sub { margin-top: 5px; color: var(--fg-2); font-size: 12px; line-height:1.35; }
    .project-part-actions { display:flex; align-items:center; gap:7px; justify-content:flex-start; flex-wrap:wrap; }
    .mini-note { color: var(--muted); font-size: 12px; white-space: nowrap; }
    .rounds { overflow: visible; }
    .round { overflow: visible; }
    .stages { padding: 10px 14px 14px 78px; background:#fff; overflow: visible; display: grid; gap: 10px; }
    .stage-group { border: 1px solid var(--border-1); border-radius: 12px; background: #fff; overflow: visible; }
    .stage-group-title { min-height: 34px; display: flex; align-items: center; justify-content: flex-start; gap: 12px; padding: 0 12px; color: var(--fg-3); font-size: 11px; font-weight: 700; border-bottom: 1px solid var(--border-1); }
    .phase-left { display:flex; align-items:center; gap:8px; min-width:0; }
    .phase-left { flex:1; }
    .phase-name { text-transform: uppercase; letter-spacing: .003em; white-space:nowrap; }
    .phase-status { min-width:max-content; height:26px; display:inline-flex; align-items:center; justify-content:center; gap:6px; border:1px solid var(--line); border-radius:999px; background:#fff; padding:0 10px; color:var(--fg-2); font-size:11px; font-weight:650; text-transform:none; letter-spacing:.003em; white-space:nowrap; line-height:1; }
    .phase-status.yellow { border-color:var(--status-warning-bg); background:var(--status-warning-bg); color:var(--status-warning); }
    .phase-status.green { border-color:var(--status-success-bg); background:var(--status-success-bg); color:var(--status-success); }
    .phase-status.gray { color:var(--fg-3); }
    .phase-copy { height:26px; border:1px solid rgba(124,58,237,.35); border-radius:12px; background:#fff; color:var(--ai-purple); padding:0 10px; font:inherit; font-size:11px; font-weight:700; cursor:pointer; white-space:nowrap; }
    .phase-copy:hover { border-color:var(--ai-purple); background:var(--ai-purple-bg); color:var(--ai-purple-dark); }
    .stage { display:grid; grid-template-columns: 170px minmax(180px, 1fr) 190px 28px; align-items:center; gap: 12px; min-height: 38px; padding: 0 12px; border-bottom: 1px solid var(--border-1); font-size: 12px; }
    .stage-link { display: contents; color: inherit; text-decoration: none; }
    .stage:last-child { border-bottom: 0; }
    .stage-name { font-weight: 500; color: var(--fg-2); }
    .stage.child .stage-name { color: var(--fg-2); }
    .bar { height: 7px; border-radius: 999px; background: var(--grey-3); overflow:hidden; display:flex; }
    .fill { height: 100%; opacity:1; flex: 0 0 auto; }
    .fill:first-child { border-radius: 999px 0 0 999px; }
    .fill:last-child { border-radius: 0 999px 999px 0; }
    .fill.only { border-radius: 999px; }
    .stage-label { min-width:0; color: var(--muted); white-space: nowrap; display:flex; justify-content:flex-start; }
    .stage-cta { max-width:100%; height: 26px; display: inline-flex; align-items: center; border: 1px solid var(--border-1); border-radius: 8px; background: #fff; color: var(--fg-2); padding: 0 9px; font-size: 12px; font-weight: 650; text-decoration: none; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
    .stage-cta.review { border-color: var(--status-warning-bg); background: var(--status-warning-bg); color: var(--status-warning); }
    .stage-cta:hover { border-color: var(--blue-dark); color: var(--blue-dark); text-decoration: none; }
    .stage.deliverables-stage { display:block; padding: 10px 12px 12px; min-height: 0; }
    .deliverables-head { display:flex; align-items:center; justify-content:space-between; gap:12px; margin-bottom:8px; }
    .deliverables-title { display:flex; align-items:center; gap:6px; color:var(--fg-2); font-size:12px; font-weight:650; }
    .deliverables-meta { display:flex; align-items:center; gap:8px; color:var(--muted); font-size:12px; }
    .deliverable-links { display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 8px; }
    .deliverable-doc { min-width:0; display:grid; grid-template-rows:1fr auto; gap:8px; min-height:116px; padding:10px; border:1px solid var(--border-1); border-radius:8px; background:var(--bg-2); }
    .deliverable-link { min-width:0; display:grid; grid-template-rows:32px 20px 1fr; gap:7px; align-content:start; min-height:0; color:inherit; text-decoration:none; }
    .deliverable-link:hover { border-color:var(--blue-dark); text-decoration:none; }
    .deliverable-link.missing { color:var(--fg-3); }
    .deliverable-link.missing strong { color:var(--fg-3); }
    .deliverable-link strong { min-width:0; overflow:hidden; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; font-size:12px; color:var(--fg-1); line-height:1.3; }
    .deliverable-link .deliverable-desc { color:var(--fg-3); font-size:11px; line-height:1.35; }
    .deliverable-link .doc-status { width:max-content; max-width:100%; height:20px; display:inline-flex; align-items:center; gap:5px; border:1px solid var(--line); border-radius:999px; background:#fff; padding:0 8px; color:var(--fg-2); font-size:10.5px; font-weight:650; white-space:nowrap; }
    .deliverable-link .doc-status.yellow { border-color:var(--status-warning-bg); background:var(--status-warning-bg); color:var(--status-warning); }
    .deliverable-link .doc-status.green { border-color:var(--status-success-bg); background:var(--status-success-bg); color:var(--status-success); }
    .deliverable-link .doc-status.gray { color:var(--fg-3); }
    .deliverable-actions { min-width:0; display:flex; justify-content:flex-start; align-items:center; gap:6px; flex-wrap:wrap; overflow:hidden; }
    .deliverable-actions .prompt-wrap { max-width:100%; min-width:0; }
    .deliverable-actions .prompt-wrap .info.has-label { max-width:100%; }
    .deliverable-actions .prompt-button-label { min-width:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
    .deliverable-action { max-width:100%; height:24px; display:inline-flex; align-items:center; gap:6px; border:1px solid var(--border-muted); border-radius:999px; background:#fff; color:var(--fg-2); padding:0 9px; font:inherit; font-size:11px; font-weight:650; text-decoration:none; cursor:pointer; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
    .deliverable-action:hover { border-color:var(--blue-dark); text-decoration:none; }
    .round-review-line { margin: 10px 14px 0 78px; border: 1px solid var(--status-warning-bg); border-radius: 12px; background: var(--status-warning-soft-bg); display:grid; grid-template-columns: 1fr auto 28px; gap: 12px; align-items:center; padding: 11px 12px; }
    .round-review-line.clear { border-color: var(--border-1); background:#fff; }
    .round-review-title { font-size: 12px; font-weight: 650; color:var(--fg-1); }
    .round-review-sub { margin-top: 4px; color: var(--muted); font-size: 12px; }
    .round-review-actions { display:flex; align-items:center; gap:10px; flex-wrap:wrap; justify-content:flex-end; }
    .monitor-note { margin: 10px 14px 0 78px; border:1px solid var(--line); border-radius:12px; background:var(--bg-2); padding:11px 12px; color:var(--fg-2); font-size:12px; line-height:1.4; }
    .monitor-note strong { color:var(--fg-1); }
    .readonly-deliverables { margin:10px 14px 14px 78px; border:1px solid var(--line); border-radius:12px; background:#fff; overflow:hidden; }
    .readonly-deliverables-head { min-height:34px; display:flex; align-items:center; justify-content:space-between; gap:12px; padding:0 12px; border-bottom:1px solid var(--line); color:var(--fg-3); font-size:11px; font-weight:700; text-transform:uppercase; }
    .readonly-deliverable { display:grid; grid-template-columns:1fr auto; gap:12px; align-items:center; min-height:48px; padding:9px 12px; border-bottom:1px solid var(--line); }
    .readonly-deliverable:last-child { border-bottom:0; }
    .readonly-deliverable-title { font-size:12px; font-weight:700; color:var(--fg-1); }
    .readonly-deliverable-sub { margin-top:3px; color:var(--fg-3); font-size:11px; line-height:1.35; }
    .readonly-deliverable-actions { display:flex; align-items:center; justify-content:flex-end; gap:6px; flex-wrap:wrap; }
    .lens-control { display:flex; align-items:center; gap:7px; min-height:28px; color:var(--muted); font-size:11px; }
    .lens-control span { font-weight:700; color:var(--fg-2); white-space:nowrap; }
    .lens-control select { height:28px; min-width:190px; border:1px solid var(--border-1); border-radius:8px; background:#fff; color:var(--fg-2); font:inherit; font-size:12px; font-weight:650; padding:0 8px; }
    .lens-control em { min-width:220px; font-style:normal; color:var(--fg-3); font-size:11px; }
    .lens-control:focus-within em, .lens-control:hover em { color:var(--status-warning); }
    .info-wrap { position: relative; display: inline-flex; justify-content: flex-end; }
    .info {
      width: 18px; height: 18px; border-radius: 50%; border: 1px solid var(--border-1);
      color: var(--fg-3); background: #fff; font-size: 11px; line-height: 16px;
      display: inline-grid; place-items: center; cursor: help; font-weight: 700;
    }
    .prompt-wrap { justify-content: flex-start; }
    .prompt-wrap .info {
      width: 24px; height: 26px; border-radius: 12px; border-color: rgba(124,58,237,.35);
      background: #fff; color: var(--ai-purple); cursor: pointer; padding: 0;
    }
    .prompt-wrap .info:hover, .prompt-wrap .info:active { border-color: var(--ai-purple); background: var(--ai-purple-bg); color: var(--ai-purple-dark); }
    .prompt-wrap .info.has-label {
      width: auto; min-width: 0; height: 26px; padding: 0 10px; gap: 6px;
      display: inline-flex; align-items:center; justify-content:center;
      font-size: 11px; line-height: 1; font-weight: 750; white-space: nowrap;
    }
    .prompt-wrap .sparkle { width: 14px; height: 14px; display:block; }
    .prompt-wrap .prompt-button-label { display:inline-block; }
    .tip {
      position: fixed; z-index: 1000; right: auto; left: 16px; top: 16px; width: min(420px, calc(100vw - 32px));
      display: none; padding: 12px; border: 1px solid var(--border-1); border-radius: 12px;
      max-height: calc(100vh - 32px); overflow: auto;
      background: #fff; box-shadow: 0 14px 34px rgba(32, 43, 64, 0.16);
      color: var(--fg-2); font-size: 12px; line-height: 1.45; cursor: default; text-transform:none; letter-spacing:.003em; font-weight:400;
    }
    .prompt-wrap .tip { width: min(420px, calc(100vw - 32px)); }
    .badges .prompt-wrap .tip,
    .project-part-actions .prompt-wrap .tip,
    .deliverable-actions .prompt-wrap .tip,
    .deliverables-meta .prompt-wrap .tip { left: 16px; right: auto; }
    .info-wrap.tip-open .tip { display: block; }
    .tip a { display: inline-block; margin-top: 8px; color: var(--blue); text-decoration: none; font-weight: 650; }
    .tip a:hover { color: var(--blue-dark); }
    .tip a:hover { text-decoration: underline; }
    .gate-accept-note { margin-top: 10px; color: #6c7483; font-size: 11px; line-height: 1.4; }
    .prompt-explain { margin-top: 8px; border-left: 3px solid var(--ai-purple); padding: 7px 9px; background:var(--ai-purple-bg); color:var(--fg-2); font-size:12px; line-height:1.45; }
    .prompt-use { margin-top: 8px; border:1px solid rgba(124,58,237,.18); border-radius:8px; background:#fff; color:var(--fg-2); padding:7px 9px; font-size:12px; line-height:1.45; }
    .prompt-use strong { display:block; color:var(--fg-1); font-size:10px; text-transform:uppercase; letter-spacing:.08em; margin-bottom:2px; }
    .prompt-explain strong { display:block; margin-bottom:3px; color:var(--fg-1); font-size:11px; text-transform:uppercase; letter-spacing:.003em; }
    .copy {
      margin-top: 9px; height: 26px; border: 1px solid rgba(124,58,237,.35); border-radius: 12px;
      background: #fff; color: var(--ai-purple); font-size: 11px; font-weight: 650;
      padding: 0 9px; cursor: pointer;
    }
    .copy:hover { border-color: var(--ai-purple); background: var(--ai-purple-bg); color: var(--ai-purple-dark); }
    .toast { position: fixed; left: 50%; bottom: 18px; z-index: 1200; max-width: min(420px, calc(100vw - 36px)); border:1px solid var(--line); border-radius:12px; background:#222; color:#fff; box-shadow:0 14px 34px rgba(32,43,64,.18); padding:10px 12px; font-size:12px; font-weight:400; opacity:0; transform:translate(-50%, 8px); pointer-events:none; transition:opacity .16s ease, transform .16s ease; }
    .toast.show { opacity:1; transform:translate(-50%, 0); }
    .empty { border: 1px dashed var(--border-1); border-radius: 12px; padding: 34px; color: var(--muted); text-align:center; background:#fff; }
    .inline-viewer { border: 1px solid var(--line); border-radius: 8px; overflow: hidden; background: #fff; }
    .inline-viewer-head { min-height: 36px; display:flex; align-items:center; justify-content:space-between; gap:12px; padding: 0 10px; border-bottom: 1px solid var(--line); background:var(--surface-subtle); }
    .inline-viewer-title { min-width:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; font-size:12px; font-weight:650; color:var(--fg-2); }
    .inline-viewer-actions { display:flex; gap:6px; align-items:center; flex-shrink:0; }
    .inline-viewer-actions a, .inline-viewer-actions button { height:24px; border:1px solid var(--border-muted); border-radius:4px; background:#fff; color:var(--fg-2); padding:0 8px; font:inherit; font-size:11px; font-weight:650; line-height:22px; text-decoration:none; cursor:pointer; }
    .inline-viewer-actions button { appearance:none; }
    .inline-viewer iframe { width:100%; height:min(720px, 72vh); border:0; display:block; background:#fff; }
    .document-open > .project-stack, .document-open > .rounds, .document-open > .stages, .review-project.document-open > .review-list { display:none; }
    @media (max-width: 760px) {
      .topbar, .layout { border-radius: 0; box-shadow: none; }
      .layout { grid-template-columns: 1fr; }
      .rail { top:56px; width:auto; height:auto; min-height: 44px; border-right:0; border-bottom:1px solid var(--line); padding:0 14px; flex-direction:row; justify-content:flex-start; overflow-x:auto; overflow-y:hidden; }
      .rail-tab { width:48px; height:44px; flex:0 0 auto; }
      .rail-spacer { flex:0 0 auto; min-width:8px; min-height:0; }
      main { padding: 20px 14px 30px; }
      .toolbar { align-items:flex-start; flex-direction:column; }
      .learning-top-grid { grid-template-columns: 1fr; }
      .learning-detail-grid { grid-template-columns:1fr; }
      .learning-context-points { grid-template-columns:1fr; }
      .onboarding-grid { grid-template-columns:1fr; }
      .onboarding-hero { grid-template-columns:1fr; }
      .update-meta-grid { grid-template-columns:1fr; }
      .row { grid-template-columns: 28px 1fr; }
      .project > .row { grid-template-columns: 28px 44px 1fr; }
      .round .row { grid-template-columns: 28px 1fr auto; }
      .round-monitor-cell { grid-column:3; grid-row:1 / span 2; }
      .project-icon { width:40px; height:40px; font-size:23px; }
      .badges { grid-column: 2; justify-content:flex-start; }
      .project > .row .badges { grid-column: 3; }
      .project-stack { grid-template-columns: 1fr; }
      .stages { padding-left: 14px; }
      .round-review-line { margin-left: 14px; grid-template-columns: 1fr; }
      .monitor-note { margin-left:14px; }
      .readonly-deliverables { margin-left:14px; }
      .readonly-deliverable { grid-template-columns:1fr; }
      .readonly-deliverable-actions { justify-content:flex-start; }
      .round-review-actions { justify-content:flex-start; }
      .lens-control { align-items:flex-start; flex-direction:column; }
      .stage { grid-template-columns: 118px minmax(120px, 1fr) 28px; }
      .stage-label { grid-column: 1 / span 2; grid-row:2; }
      .info-wrap { grid-column: 3; grid-row: 1 / span 2; }
      .inline-viewer iframe { height: 70vh; }
    }
    @media (min-width: 761px) and (max-width: 1080px) {
      .project-stack { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .learning-detail-grid { grid-template-columns:1fr; }
    }
  </style>
</head>
<body>
  <div class="shell">
    <header class="topbar"><div class="brand"><div class="mark">R</div><span>Research OS</span></div><div class="top-status"><button class="version-button" id="versionButton" type="button" hidden>New version available</button><div class="backup-status gray" id="backupStatus" hidden>Backup: loading</div><button class="backup-button" id="backupButton" type="button" hidden>Sync to iCloud</button><div class="updated" id="updated"><span id="updatedText">Loading...</span></div></div></header>
    <div class="layout">
      <aside class="rail" aria-label="Research OS sections">
        <button class="rail-tab active" type="button" data-tab="dashboard" title="Dashboard" aria-label="Dashboard">
          <span class="rail-icon" style="--icon: url('/assets/icons/beaker.png')" aria-hidden="true"></span>
        </button>
        <button class="rail-tab" type="button" data-tab="learning" title="Looped Learning" aria-label="Looped Learning">
          <span class="rail-icon" style="--icon: url('/assets/icons/lightbulb.svg')" aria-hidden="true"></span>
        </button>
        <div class="rail-spacer" aria-hidden="true"></div>
        <button class="rail-tab" type="button" data-tab="about" title="Research OS basics" aria-label="Research OS basics">
          <span class="rail-icon" style="--icon: url('/assets/icons/info.svg')" aria-hidden="true"></span>
        </button>
        <button class="rail-tab" type="button" data-tab="settings" title="Settings" aria-label="Settings">
          <span class="rail-icon" style="--icon: url('/assets/icons/settings.svg')" aria-hidden="true"></span>
        </button>
      </aside>
      <main>
        <section class="tab-panel active" id="dashboardPanel">
          <section class="toolbar"><div class="toolbar-left"><input class="search" id="search" type="search" placeholder="Search projects"><div class="toolbar-actions" id="toolbarActions"></div></div><div class="toolbar-status"><button class="manual-refresh" id="refreshButton" type="button" data-label="Refresh dashboard"><svg class="manual-refresh-icon" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M17.7 6.3A8 8 0 1 0 20 12h-2a6 6 0 1 1-1.76-4.24L13 11h8V3l-3.3 3.3z"/></svg><span>Refresh dashboard</span></button><span>Auto every <span id="refreshMinutes">15</span> min</span></div></section>
          <section id="projects"></section>
        </section>
        <section class="tab-panel" id="learningPanel"></section>
        <section class="tab-panel" id="aboutPanel"></section>
        <section class="tab-panel" id="settingsPanel"></section>
      </main>
    </div>
  </div>
  <div class="toast" id="toast" role="status" aria-live="polite"></div>
  <script>
    const stateKey = "research-os-dashboard-open";
    const openState = JSON.parse(localStorage.getItem(stateKey) || "{}");
    let activeTab = localStorage.getItem("research-os-dashboard-tab") || "dashboard";
    let refreshIntervalSeconds = 900;
    let refreshTimer = null;
    let dashboardRefreshing = false;
    const stageNames = { sources: "Sources", representations: "Representations", evidence: "Evidence", patterns: "Patterns", insights: "Insights", recommendations: "Recommendations", deliverables: "Deliverables" };
    const stageGroups = [
      { key: "input", title: "Input", keys: ["sources"] },
      { key: "synthesis", title: "Synthesis", keys: ["evidence", "patterns", "insights", "recommendations"], child: true },
      { key: "output", title: "Output", keys: ["deliverables"] }
    ];
    const statusLabel = { green: "up to date", yellow: "needs attention", red: "blocked", gray: "not started", blue: "running" };
    let lastPayload = null;
    let inlineState = null;
    function escapeHtml(value) { return String(value || "").replace(/[&<>"']/g, char => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[char])); }
    function saveOpen(id, value) { openState[id] = value; localStorage.setItem(stateKey, JSON.stringify(openState)); }
    function dot(status) { return `<span class="dot ${status || "gray"}"></span>`; }
    function setUpdatedText(text) {
      document.getElementById("updatedText").textContent = text;
    }
    function setDashboardLoading(isLoading) {
      if (isLoading) {
        document.getElementById("projects").innerHTML = `<div class="dashboard-loading"><span class="dashboard-loading-icon" aria-hidden="true">&#8987;</span><span class="dashboard-loading-text">Loading dashboard...</span></div>`;
      }
    }
    function hasOpenTip() {
      return Boolean(document.querySelector(".tip-open"));
    }
    function scheduleDashboardRefresh(seconds) {
      refreshIntervalSeconds = Math.max(30, Math.min(3600, Number(seconds) || 900));
      if (refreshTimer) clearInterval(refreshTimer);
      refreshTimer = setInterval(refresh, refreshIntervalSeconds * 1000);
    }
    function badge(status, text) { return `<span class="badge ${status || "gray"}">${dot(status)}${text}</span>`; }
    function plural(count, singular, pluralValue) {
      return `${count} ${count === 1 ? singular : (pluralValue || `${singular}s`)}`;
    }
    function learningLabel(key) {
      return {
        scope_abstractness: "Scope / abstraction level",
        interpretation_quality: "Interpretation quality",
        evidence_quality: "Evidence quality",
        quality_gates: "Quality gates",
        evidence: "Evidence",
        patterns: "Patterns",
        insights: "Insights",
        recommendations: "Recommendations",
        context: "Context",
        reviews: "Reviews",
        learning: "Learning",
        Approve: "Yes",
        Revise: "Needs changes",
        Reject: "No"
      }[key] || key;
    }
    function projectReviewTotal(project) {
      return project.review.pending_items + project.rounds.reduce((sum, round) => sum + round.review.pending_items, 0);
    }
    function projectWaitingTotal(project) {
      return project.project_context.files_waiting + project.rounds.reduce((sum, round) => sum + round.source_files.waiting, 0);
    }
    function projectEmoji(project) {
      const foods = ["🍎", "🍌", "🥕", "🥦", "🥑", "🍅", "🥬", "🧀", "🥖", "🥐", "🍞", "🥔", "🧅", "🧄", "🍓", "🍇", "🍋", "🍊", "🍒", "🌽", "🥒", "🫑", "🥨", "🥯", "🍉", "🍍", "🥭", "🥝"];
      const key = String(project.id || project.name || "");
      let hash = 0;
      for (let index = 0; index < key.length; index += 1) {
        hash = ((hash << 5) - hash + key.charCodeAt(index)) | 0;
      }
      return foods[Math.abs(hash) % foods.length];
    }
    function attentionBadges(status, waiting, reviews) {
      const parts = [];
      if (waiting) parts.push(badge("yellow", `${plural(waiting, "source")} waiting`));
      if (reviews) parts.push(badge("yellow", `${reviews} to review`));
      return parts.join("");
    }
    function lensInstruction(round) {
      const lens = round.research_lens || { label: "Neutral research lens", key: "neutral", path: "Research OS/lenses/neutral.md", is_special: false };
      return `Research lens: ${lens.label}. Read ${lens.path} and apply it as additional instructions on top of common Research OS rules. Evidence stays source-faithful; apply lens-specific interpretation mainly to Patterns, Insights, Recommendations and Deliverables. Do not let the lens override traceability, uncertainty, contradictions or researcher review.`;
    }
    function lensBadge(round) {
      const lens = round.research_lens || {};
      if (!lens.is_special) return "";
      return badge("yellow", `Lens: ${escapeHtml(lens.label || "Special lens")}`);
    }
    function renderResearchLensControl(round) {
      const lens = round.research_lens || { key: "neutral", label: "Neutral research lens", is_special: false };
      const options = (round.research_lenses || []).map(item => `<option value="${escapeHtml(item.key)}" ${item.key === lens.key ? "selected" : ""}>${escapeHtml(item.label)}</option>`).join("");
      const warning = lens.is_special ? "Special lens active for synthesis and review prompts" : "Default synthesis behavior";
      return `<label class="lens-control"><span>Research lens</span><select data-round-lens="${escapeHtml(round.path)}">${options}</select><em>${escapeHtml(warning)}</em></label>`;
    }
    function newProjectAction() {
      return {
        label: "+ New project",
        button_label: "+ New project",
        copy_label: "create project",
        instruction: "Start a new Research OS project. Codex will scaffold the project folders and files, then report what was created.",
        prompt_description: "Codex creates a new Research OS project scaffold from a project name. It should ask for the name first if you have not provided one, then create the project locally using the Research OS CLI.",
        prompt: `Create a new Research OS project in Codex/Cowork.\n\nIf I have not given you the project name yet, ask me for it before changing files.\n\nUse the Research OS CLI scaffold, not APIs or backend AI generation:\ncd "Research OS"\n./research-os project create --name "[Project name]"\n\nAfter creating it, report:\n- the project path\n- the files and folders that were created\n- where I should add project background sources\n- the next prompt/action I should run from the web UI\n\nDo not call APIs.\nDo not run local stubs.\nDo not use backend processing.\nDo not create any research findings or review decisions.`
      };
    }
    function workspaceSetupAction() {
      return {
        label: "Read workspace",
        button_label: "Read workspace prompt",
        copy_label: "read workspace",
        instruction: "Copy this prompt and paste it into Codex, Claude or another AI tool that can access your local Research OS workspace before creating your first project.",
        prompt_description: "This orients the AI tool before it starts creating or changing Research OS files. It should only inspect the workspace and report the next safe action.",
        prompt: `Read CLAUDE.md, AGENTS.md and the Research OS instructions. Then inspect the Projects folder and tell me what projects and rounds exist, what needs review, and what the next safe Research OS action is.\n\nDo not change files yet.\nDo not call APIs.\nDo not run local stubs.\nDo not use backend processing.`
      };
    }
    function newRoundAction(project) {
      return {
        label: "Create round",
        button_label: "Create round",
        copy_label: "create round",
        instruction: `Start a new Research Round inside ${project.name}. Codex will scaffold the round, then report where to add sources and background.`,
        prompt_description: "Codex creates a new Research Round inside this project. It should ask for the round date and name first if they are missing, then create only the local scaffold.",
        prompt: `Create a new Research OS round inside this project in Codex/Cowork.\n\nProject: ${project.name}\nProject id: ${project.id}\nProject path: ${project.path}\n\nIf I have not given you the round date and round name yet, ask me for them before changing files.\nUse date format YYYY-MM-DD.\n\nUse the Research OS CLI scaffold, not APIs or backend AI generation:\ncd "Research OS"\n./research-os round create --project ${project.id} --date "[YYYY-MM-DD]" --name "[Round name]"\n\nAfter creating it, report:\n- the round path\n- the files and folders that were created\n- where I should add round sources\n- where I should add or check round background\n- the next prompt/action I should run from the web UI\n\nDo not call APIs.\nDo not run local stubs.\nDo not use backend processing.\nDo not create Evidence, Patterns, Insights, Recommendations or review decisions.`
      };
    }
    function info(action, kind = "info") {
      if (!action) return "";
      const prompt = action.prompt ? escapeHtml(action.prompt) : "";
      const defaultPromptDescription = "Codex/Cowork uses this prompt to work on this part of Research OS directly. It should follow the prompt rules, avoid backend/API generation, update the relevant documents, and leave review decisions to you.";
      const promptDescription = action.prompt_description ? escapeHtml(action.prompt_description) : (prompt ? defaultPromptDescription : "");
      const explanation = promptDescription ? `<div class="prompt-explain"><strong>What this does</strong>${promptDescription}</div>` : "";
      const promptUse = prompt ? `<div class="prompt-use"><strong>How to use this</strong>Click the purple AI button to copy the prompt. Then paste it into Codex, Claude or another AI tool that has access to your <code>UX Research</code> folder.</div>` : "";
      const promptTools = prompt ? `${promptUse}${explanation}` : "";
      const qualityGates = Array.isArray(action.quality_gates) ? action.quality_gates : [];
      const waivableChecks = qualityGates.filter(gate => gate.id !== "PAT-SYNTHESIS-STALE");
      const gateTools = waivableChecks.length ? `<div class="gate-accept-note">Checks reviewed and acceptable?</div><button class="copy" type="button" data-waive-gates="${encodeURIComponent(JSON.stringify(waivableChecks))}" data-waive-path="${escapeHtml(action.quality_gate_path || "")}">Mark checks acceptable</button>` : "";
      const href = action.href && isReviewHref(action.href) ? focusHref(action.href) : action.href;
      const link = href ? `<br><a href="${href}">${escapeHtml(action.label || "Open")}</a>` : "";
      const isPrompt = kind === "prompt";
      const wrapClass = isPrompt ? "info-wrap prompt-wrap" : "info-wrap";
      const promptButtonLabel = action.button_label || action.label || "AI prompt";
      const label = isPrompt ? `Copy ${promptButtonLabel} prompt` : "Show action details";
      const sparkle = `<svg class="sparkle" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2l1.45 5.05L18.5 8.5l-5.05 1.45L12 15l-1.45-5.05L5.5 8.5l5.05-1.45L12 2zM5.5 13l.85 2.9 2.9.85-2.9.85L5.5 20.5l-.85-2.9-2.9-.85 2.9-.85L5.5 13zM18 14l.65 2.15 2.15.65-2.15.65L18 19.6l-.65-2.15-2.15-.65 2.15-.65L18 14z"/></svg>`;
      const buttonText = isPrompt ? `<span class="prompt-button-label">${escapeHtml(promptButtonLabel)}</span>` : "";
      const buttonClass = buttonText ? "info has-label" : "info";
      const icon = isPrompt ? `${sparkle}${buttonText}` : "i";
      const promptAttrs = isPrompt && prompt ? ` data-prompt="${prompt}" data-copy-label="${escapeHtml(action.copy_label || action.label || promptButtonLabel)}"` : "";
      return `<span class="${wrapClass}"><button class="${buttonClass}" type="button" aria-label="${label}"${promptAttrs}>${icon}</button><span class="tip">${escapeHtml(action.instruction)}${link}${promptTools}${gateTools}</span></span>`;
    }
    function isReviewHref(href) {
      return Boolean(href && (href.includes("review-queue.md") || href.includes("project-context-proposals.md")));
    }
    function focusHref(href, stage = "") {
      if (!href) return "#";
      if (!href.startsWith("/file")) return href;
      let next = href.includes("mode=focus") ? href : `${href}${href.includes("?") ? "&" : "?"}mode=focus`;
      if (stage && !next.includes("stage=")) next += `${next.includes("?") ? "&" : "?"}stage=${encodeURIComponent(stage)}`;
      return next;
    }
    function gateSummary(round) {
      const stages = round.stages || {};
      const lines = [];
      ["evidence", "patterns", "insights", "recommendations"].forEach(key => {
        const issues = (stages[key] && stages[key].gate_issues) || [];
        issues.slice(0, 4).forEach(issue => lines.push(`- ${stageNames[key] || key} ${issue.id}: ${issue.message}`));
      });
      return lines.length ? lines.join("\n") : "- No visible gate issues in the dashboard payload.";
    }
    function isOpen(id, fallback) { return Object.prototype.hasOwnProperty.call(openState, id) ? openState[id] : fallback; }
    function projectSourceText(project) {
      const total = Number(project.project_context.files_total || 0);
      const processed = Number(project.project_context.files_processed || 0);
      const waiting = Number(project.project_context.files_waiting || 0);
      if (!total) return "No project sources yet";
      const waitingText = waiting ? `${plural(waiting, "source")} waiting to process` : "no new sources waiting";
      return `${plural(total, "source")} total · ${processed} processed · ${waitingText}`;
    }
    function renderProjectPart(title, sub, actions) {
      return `<div class="project-part"><div class="project-part-main"><div class="project-part-title">${title}</div><div class="project-part-sub">${sub}</div></div><div class="project-part-actions">${actions}</div></div>`;
    }
    function renderProject(project) {
      const projectId = `project:${project.id}`;
      const infoId = `project-info:${project.id}`;
      const open = isOpen(projectId, project.status === "yellow" || project.status === "red");
      const infoOpen = isOpen(infoId, false);
      const sourceStatus = project.project_context.files_waiting ? badge("yellow", `${plural(project.project_context.files_waiting, "source")} waiting`) : badge(project.project_context.files_total ? "green" : "gray", project.project_context.files_total ? "up to date" : "empty");
      const sourceActions = `<a class="stage-cta" href="${project.project_context.action.href}">Open sources</a>${sourceStatus}${info(project.project_context.action, "prompt")}`;
      const backgroundPresent = Boolean(project.project_context.background_present);
      const backgroundAction = project.project_context.background_action || {};
      const backgroundStatus = badge(backgroundPresent ? "green" : "gray", backgroundPresent ? "added" : "not added yet");
      const backgroundSub = backgroundPresent ? "Durable context is available for future research rounds" : "No accepted project background has been added yet";
      const backgroundActions = `<a class="stage-cta" href="${backgroundAction.href || "#"}">${backgroundPresent ? "Open background" : "Add background"}</a>${backgroundStatus}${info(backgroundAction)}`;
      const projectReviewState = project.review.pending_items ? `<a class="stage-cta review" href="${focusHref(project.review.action.href)}">Start these reviews</a>${badge("yellow", `${project.review.pending_items} to review`)}` : `<span class="mini-note">No project reviews</span>`;
      const projectParts = [
        renderProjectPart("Project sources", projectSourceText(project), sourceActions),
        renderProjectPart("Project background", backgroundSub, backgroundActions),
        renderProjectPart("Project reviews", "Reusable context decisions for this project", `${projectReviewState}${info(project.review.action)}`),
      ].join("");
      const monitoredRoundCount = project.rounds.filter(round => round.monitored !== false).length;
      const projectMeta = project.last_round ? `${project.rounds.length} round${project.rounds.length === 1 ? "" : "s"} · ${monitoredRoundCount} monitored · last round ${project.last_round}` : "No rounds yet";
      const roundsSub = project.rounds.length ? `${project.rounds.length} round${project.rounds.length === 1 ? "" : "s"} · ${monitoredRoundCount} monitored` : "No research rounds yet";
      return `<article class="project ${open ? "open" : ""}" data-name="${escapeHtml(project.name.toLowerCase())}"><div class="row"><button class="toggle" data-toggle="${projectId}" aria-label="Toggle project">${open ? "&#9662;" : "&#9656;"}</button><div class="project-icon" aria-hidden="true">${projectEmoji(project)}</div><div class="title"><div class="name">${escapeHtml(project.name)}</div><div class="meta">${escapeHtml(projectMeta)}</div></div><div class="badges">${attentionBadges(project.status, projectWaitingTotal(project), projectReviewTotal(project))}${info(newRoundAction(project), "prompt")}</div></div><div class="project-body"><section class="project-info-section ${infoOpen ? "open" : ""}"><div class="project-info-row"><button class="toggle" data-toggle="${infoId}" aria-label="Toggle project info">${infoOpen ? "&#9662;" : "&#9656;"}</button><div><div class="project-info-title">Project info</div><div class="project-info-sub">Sources, background and reusable context reviews</div></div><div class="badges">${sourceStatus}${project.review.pending_items ? badge("yellow", `${project.review.pending_items} to review`) : ""}</div></div><div class="project-stack">${projectParts}</div></section><div class="rounds"><div class="rounds-head"><span></span><div><div class="rounds-title">Research rounds</div><div class="rounds-sub">${escapeHtml(roundsSub)}</div></div><div class="badges">${project.rounds.length ? attentionBadges(project.status, project.rounds.reduce((sum, round) => sum + round.source_files.waiting, 0), project.rounds.reduce((sum, round) => sum + round.review.pending_items, 0)) : ""}</div></div>${project.rounds.map(renderRound).join("") || `<div class="empty">No research rounds yet.</div>`}</div></div></article>`;
    }
    function renderRound(round) {
      const roundId = `round:${round.path}`;
      const monitored = round.monitored !== false;
      const open = isOpen(roundId, monitored && (round.status === "yellow" || round.status === "red"));
      const lens = round.research_lens || { label: "Neutral research lens" };
      const monitoringLabel = monitored ? "Monitoring is on" : "Monitoring is off";
      const toggle = `<div class="round-monitor-cell"><label class="monitor-switch" title="${monitoringLabel}"><input type="checkbox" data-round-monitoring="${escapeHtml(round.path)}" aria-label="${monitoringLabel} for ${escapeHtml(round.name)}" ${monitored ? "checked" : ""}><span class="monitor-switch-track" aria-hidden="true"></span></label></div>`;
      const rowToggle = `<button class="toggle" data-toggle="${roundId}" aria-label="Toggle round">${open ? "&#9662;" : "&#9656;"}</button>`;
      const metaParts = [`${round.source_files.total} sources`, `lens ${lens.label}`, `context ${round.project_context.present ? "present" : "missing"}`, `latest run ${round.latest_run ? round.latest_run.id : "none"}`];
      if (!monitored) metaParts.push("not monitored");
      const body = monitored
        ? `<div class="round-body">${renderRoundReviewLine(round)}<div class="stages">${renderStageGroups(round)}</div></div>`
        : `<div class="round-body"><div class="monitor-note"><strong>Enable monitoring to work on this round.</strong><br>You can still view existing deliverables below.</div>${renderReadonlyDeliverables(round)}</div>`;
      return `<section class="round ${open ? "open" : ""} ${monitored ? "" : "round-muted"}"><div class="row">${rowToggle}<div class="title"><div class="name">${escapeHtml(round.name)}</div><div class="meta">${escapeHtml(metaParts.join(" · "))}</div></div><div class="badges">${monitored ? `${lensBadge(round)}${attentionBadges(round.status, round.source_files.waiting, round.review.pending_items)}` : badge("gray", "not monitored")}</div>${toggle}</div>${body}</section>`;
    }
    function renderRoundReviewLine(round) {
      const action = round.stages.reviews && round.stages.reviews.action;
      const count = round.review.pending_items;
      const patternIssues = (((round.stages || {}).patterns || {}).gate_issues) || [];
      const staleGate = patternIssues.find(issue => issue.id === "PAT-SYNTHESIS-STALE");
      const title = staleGate ? "Next step" : "Round reviews";
      const subtitle = staleGate ? "New evidence has been processed. Run synthesis to see whether Patterns, Insights and Recommendations should change." : "Decisions before this round can feed deliverables or current understanding";
      const state = count ? `<a class="stage-cta review" href="${focusHref(action.href)}">Start review for ${count} ${count === 1 ? "item" : "items"}</a>` : (staleGate ? `<span class="stage-cta review">Run synthesis next</span>` : "");
      return `<div class="round-review-line ${count || staleGate ? "" : "clear"}"><div><div class="round-review-title">${escapeHtml(title)}</div><div class="round-review-sub">${escapeHtml(subtitle)}</div></div><div class="round-review-actions">${renderResearchLensControl(round)}<div>${state}</div></div>${info(action)}</div>`;
    }
    function renderOutputOnly(round) {
      const stage = round.stages && round.stages.deliverables;
      if (!stage) return "";
      const group = { key: "output", title: "Output", keys: ["deliverables"] };
      return `<section class="stage-group">${renderPhaseHeader(round, group)}${renderStage("deliverables", stage, false, round.stages)}</section>`;
    }
    function renderReadonlyDeliverables(round) {
      const stage = round.stages && round.stages.deliverables;
      const items = (stage && Array.isArray(stage.items) ? stage.items : []).filter(item => item.exists);
      if (!items.length) {
        return `<section class="readonly-deliverables"><div class="readonly-deliverables-head"><span>Deliverables</span><span>0 generated</span></div><div class="empty">No deliverables have been generated for this round yet.</div></section>`;
      }
      const rows = items.map(item => {
        const actions = Array.isArray(item.actions)
          ? item.actions.filter(action => !action.prompt).map(action => {
            if (action.copy_path) {
              return `<button class="deliverable-action" type="button" data-copy-file="${escapeHtml(action.copy_path)}" data-copy-mode="${escapeHtml(action.copy_mode || "prompt")}">${escapeHtml(action.label || "Copy")}</button>`;
            }
            const actionHref = String(action.href || "#");
            const opensPdf = actionHref.includes(".pdf");
            return `<a class="deliverable-action" href="${escapeHtml(actionHref)}"${opensPdf ? " target=\"_blank\" rel=\"noreferrer\" data-no-inline=\"true\"" : ""}>${escapeHtml(action.label || "Open")}</a>`;
          }).join("")
          : "";
        const openLink = item.href ? `<a class="deliverable-action" href="${escapeHtml(item.href)}">Open</a>` : "";
        return `<div class="readonly-deliverable"><div><div class="readonly-deliverable-title">${escapeHtml(item.title || item.name)}</div><div class="readonly-deliverable-sub">${dot(item.status || "gray")} ${escapeHtml(item.status_label || "generated")}${item.description ? ` · ${escapeHtml(item.description)}` : ""}</div></div><div class="readonly-deliverable-actions">${openLink}${actions}</div></div>`;
      }).join("");
      return `<section class="readonly-deliverables"><div class="readonly-deliverables-head"><span>Deliverables</span><span>${items.length} generated</span></div>${rows}</section>`;
    }
    function reviewStageHref(stages, key) {
      const reviewAction = stages.reviews && stages.reviews.action;
      if (!reviewAction || !reviewAction.href) return "";
      return focusHref(reviewAction.href, key);
    }
    function phaseStatus(round, group) {
      const stages = round.stages;
      if (group.key === "input") {
        const waiting = Number(stages.sources.waiting || 0);
        return {
          status: waiting ? "yellow" : "green",
          label: waiting ? `${plural(waiting, "source")} waiting` : "up to date",
          action: {
            label: "Run input",
            button_label: "Run input",
            copy_label: "run input",
            instruction: waiting ? "Input has unprocessed source material. Ask Codex to process this round." : "Input is up to date. No source processing is needed right now.",
            prompt: `Process Input for this Research OS round in Codex/Cowork: ${round.path}. First read Research OS/08-looped-learning/active-learnings.md and apply any active Looped Learnings. Read 00-ai-work-files/90-pipeline-settings.yaml and apply source-type rules. ${lensInstruction(round)} Do not call APIs, do not run local stubs, and do not use the backend pipeline. If source files are waiting, read the waiting sources and update Research OS documents directly. If a source is researcher-synthesis, treat it as high-weight directional researcher interpretation for Insights, Recommendations and Current Understanding, but do not convert it into standalone participant Evidence unless explicitly requested. Keep review decisions pending in the web UI. After genuine processing, update .pipeline-state.json for processed source checksums and report what changed and what still needs review.`
          }
        };
      }
      if (group.key === "synthesis") {
        const reviews = ["evidence", "patterns", "insights", "recommendations"].reduce((sum, key) => sum + Number(stages[key].review || 0), 0);
        const gates = ["evidence", "patterns", "insights", "recommendations"].reduce((sum, key) => sum + Number(stages[key].gates || 0), 0);
        const gateItems = [];
        ["evidence", "patterns", "insights", "recommendations"].forEach(key => {
          ((stages[key] && stages[key].gate_issues) || []).forEach(issue => gateItems.push({ stage: key, id: issue.id, message: issue.message }));
        });
        const staleGate = gateItems.find(issue => issue.id === "PAT-SYNTHESIS-STALE");
        const gateText = gateSummary(round);
        return {
          status: (reviews || gates) ? "yellow" : "green",
          label: staleGate ? "new evidence needs synthesis" : (reviews && gates ? `${reviews} review · ${gates} checks` : (reviews ? `${reviews} to review` : (gates ? `${gates} checks need attention` : "up to date"))),
          action: {
            label: "Run synthesis",
            button_label: "Run synthesis",
            copy_label: "run synthesis",
            instruction: staleGate ? "New Evidence has been processed and curated, but it has not been carried into Patterns, Insights or Recommendations yet. Run synthesis next before trusting downstream deliverables." : (reviews || gates ? "Continue synthesis after your review batch. Codex applies completed decisions, continues the next synthesis step, and improves quality gaps where the source material supports it." : "Synthesis is up to date. Use this prompt only to check whether anything changed before continuing downstream."),
            prompt_description: staleGate ? "Codex should incorporate the newly processed Evidence into cross-source synthesis. It should update or add Patterns where supported, then stop at the next review gate so the researcher can review any new or changed Patterns, Insights or Recommendations before output is refreshed." : "Codex applies your completed Evidence, Pattern, Insight or Recommendation review decisions, continues the next appropriate synthesis step, updates Recommendations, and improves quality gaps where the source material supports it. It must not make review decisions for you.",
            quality_gate_path: round.path,
            quality_gates: gateItems,
            prompt: `Continue synthesis after my reviews for this Research OS round in Codex/Cowork: ${round.path}.\n\nFirst read Research OS/08-looped-learning/active-learnings.md and apply any active Looped Learnings.\nRead 00-ai-work-files/90-pipeline-settings.yaml and apply source-type rules. If any source is marked researcher-synthesis, treat it as high-weight directional researcher interpretation for Insights, Recommendations and Current Understanding; do not treat it as standalone participant Evidence unless explicitly requested.\n${lensInstruction(round)}\nRead the review decisions for Evidence, Patterns, Insights and Recommendations.\nApply completed review decisions to the Research OS documents.\nContinue the next appropriate synthesis step based on which reviews are complete:\n- first handle AI-performable Evidence cleanup checks, such as splitting over-compressed observations or repairing traceability, without making researcher review decisions\n- after Evidence reviews: update Patterns\n- after Pattern reviews: update Insights\n- after Insight reviews: update Recommendations\n- after Recommendation reviews: prepare downstream output/current understanding or report what still blocks it\n\nMaintain Recommendations as a living synthesis layer. Each Recommendation should include:\n- What we learned\n- What we should do\n- optional options/tradeoff when multiple routes are supported\n- type/labels when useful\n- based on Evidence, Pattern or Insight IDs\n- confidence and validation/open questions where relevant\n\nRecommendation writing rules:\n- Write like a researcher explaining the implication to another human, not like a compressed summary dump.\n- For What we learned, start with one clear sentence. If there are multiple details, put them in 2-4 bullets.\n- For What we should do, start with one clear recommendation sentence. If there are multiple concrete changes, put them in 2-5 bullets.\n- Avoid long paragraphs that combine rationale, examples, and actions in one line.\n\nAlso improve quality gaps where the source material supports it:\ntraceability, weak support, contradicting evidence, assumptions/open questions, unclear "Helps us understand" fields, over-compressed Evidence observations that Codex can safely split or tighten, and over-compressed Patterns/Insights/Recommendations that do not stand alone.\n\nDo not call APIs.\nDo not run local stubs.\nDo not use the backend pipeline.\nDo not make review decisions for me.\nKeep unresolved items pending in the web UI.\n\nCurrent visible checks needing attention:\n${gateText}\n\nReport what changed, what was not changed, and what still needs review.`
          }
        };
      }
      const synthesisReviews = Number(round.review.pending_items || 0);
      const deliverableReviews = Number(stages.deliverables.review || 0);
      const reviews = synthesisReviews + deliverableReviews;
      const deliverables = Number(stages.deliverables.generated || 0);
      const totalDeliverables = Number(stages.deliverables.total || 0);
      const missingDeliverables = Math.max(totalDeliverables - deliverables, 0);
      const reviewLabel = synthesisReviews
        ? `${plural(synthesisReviews, "synthesis item")} to review`
        : `${plural(deliverableReviews, "deliverable item")} to review`;
      const outputLabel = reviews ? reviewLabel : (missingDeliverables ? `${plural(missingDeliverables, "deliverable")} to prepare` : (deliverables ? `${plural(deliverables, "deliverable")}` : "not started"));
      return {
        status: reviews ? "yellow" : (deliverables ? "green" : "gray"),
        label: outputLabel,
        action: {
          label: "Check output",
          button_label: "Check output",
          copy_label: "check output",
          instruction: reviews ? "Output is waiting for review decisions or deliverable notes before any final artefact should be exported or shared." : "Output has two steps: draft reviewable Markdown, then export or finalize the approved deliverable artefact.",
          prompt: `Check Output for this Research OS round in Codex/Cowork: ${round.path}. First read Research OS/08-looped-learning/active-learnings.md and apply any active Looped Learnings. ${lensInstruction(round)} Do not call APIs, do not run local stubs, and do not use backend deliverable generation. Use the round's actual deliverables folder from status.json or the filesystem; in the clean folder structure this is usually 02-output-deliverables. If synthesis reviews are still open, or if any active deliverable section is not marked Yes/Looks good without comments, tell me what blocks output. History entries in .deliverable-reviews.json are previous review rounds and should not block output. If active deliverable review notes exist, read .deliverable-reviews.json and apply completed notes directly to the Markdown deliverable. Add a history entry for the review round you processed, but preserve sections marked Looks good with no notes unless you changed their content. Sections whose content changes should be reviewed again; unchanged approved sections should stay ready with only an Edit option in the UI. Deliverables must follow this lifecycle: draft reviewable Markdown source -> user reviews Markdown -> iterate until every active section is Looks good with no notes -> export or finalize the approved artefact. If no research summary Markdown exists yet, create only research-summary.md first. Do not generate the other Markdown deliverables in the same pass. After the research summary is reviewed/accepted with every section Yes/Looks good and no comments, use a second explicit prompt to draft the remaining Markdown deliverables: design actions summary, PowerPoint preparation prompt and stakeholder Slack message. After any Markdown deliverable is fully approved, use its explicit export/finalize prompt to make the final artefact, such as PDF for research summary or design brief.`
        }
      };
    }
    function renderPhaseHeader(round, group) {
      const phase = phaseStatus(round, group);
      const promptInfo = info(phase.action, "prompt");
      return `<div class="stage-group-title"><div class="phase-left"><span class="phase-name">${escapeHtml(group.title)}</span><span class="phase-status ${phase.status}">${dot(phase.status)}${escapeHtml(phase.label)}</span>${promptInfo}</div></div>`;
    }
    function renderStageGroups(round) {
      const stages = round.stages;
      return stageGroups.map(group => {
        const rows = group.keys.filter(key => stages[key]).map(key => renderStage(key, stages[key], group.child, stages)).join("");
        return rows ? `<section class="stage-group">${renderPhaseHeader(round, group)}${rows}</section>` : "";
      }).join("");
    }
    function stageDisplayLabel(key, stage) {
      const total = Number(stage.total || 0);
      const processed = Number(stage.processed || 0);
      const itemLabel = stage.item_label || "item";
      const gates = Number(stage.gates || 0);
      if (key === "deliverables") return `${Number(stage.generated || 0)}/${total || 0} generated`;
      if (stage.waiting && ["sources", "representations"].includes(key)) return `${plural(stage.waiting, "source")} waiting`;
      if (key === "patterns" && Array.isArray(stage.gate_issues) && stage.gate_issues.some(issue => issue.id === "PAT-SYNTHESIS-STALE")) return "Run synthesis to update";
      if (stage.review && gates) return `${stage.review} review · ${gates} checks`;
      if (stage.review) return `${stage.review} to review`;
      if (key === "evidence" && stage.gates) return "Run synthesis to update";
      if (stage.gates) return `${stage.gates} ${stage.gates === 1 ? "check" : "checks"} need attention`;
      if (total && ["sources", "representations"].includes(key)) return `${processed}/${total} processed`;
      if (total && ["evidence", "patterns", "insights", "recommendations", "deliverables"].includes(key)) return plural(total, itemLabel);
      if (stage.status === "green") return "Ready";
      return stage.label;
    }
    function progressSegments(stage) {
      const total = Math.max(Number(stage.total || 0), Number(stage.processed || 0) + Number(stage.waiting || 0) + Number(stage.review || 0) + Number(stage.gates || 0));
      if (!total) return [{ status: "gray", width: stage.status === "gray" ? 18 : 100 }];
      const processed = Math.max(Number(stage.processed || 0), 0);
      const waiting = Math.max(Number(stage.waiting || 0), 0);
      const review = Math.max(Number(stage.review || 0), 0);
      const gates = Math.max(Number(stage.gates || 0), 0);
      const remaining = Math.max(total - processed - waiting - review - gates, 0);
      const raw = [
        { status: "green", count: processed },
        { status: "yellow", count: waiting + review + gates },
        { status: "gray", count: remaining }
      ].filter(part => part.count > 0);
      return raw.length ? raw.map(part => ({ status: part.status, width: Math.max((part.count / total) * 100, 4) })) : [{ status: stage.status || "gray", width: 100 }];
    }
    function renderProgress(stage) {
      const segments = progressSegments(stage);
      return `<div class="bar">${segments.map(part => `<div class="fill ${part.status} ${segments.length === 1 ? "only" : ""}" style="width:${part.width}%"></div>`).join("")}</div>`;
    }
    function renderStage(key, stage, child, stages) {
      const action = stage.action || {};
      const href = action.href || "#";
      const labelHref = stage.review ? reviewStageHref(stages, key) : href;
      const label = stageDisplayLabel(key, stage);
      const labelClass = `stage-cta ${stage.review || stage.gates ? "review" : ""}`;
      const labelElement = stage.gates && !stage.review
        ? `<span class="${labelClass}">${escapeHtml(label)}</span>`
        : `<a class="${labelClass}" href="${labelHref}">${escapeHtml(label)}</a>`;
      if (key === "deliverables") {
        const items = Array.isArray(stage.items) ? stage.items : [];
        const docs = items.map(item => {
          const status = item.status || (item.exists ? "yellow" : "gray");
          const statusLabel = item.status_label || (item.exists ? "ready for review" : "not generated");
          const description = item.description ? `<span class="deliverable-desc">${escapeHtml(item.description)}</span>` : "";
          const body = `<strong>${escapeHtml(item.title || item.name)}</strong><span class="doc-status ${escapeHtml(status)}">${dot(status)}${escapeHtml(statusLabel)}</span>${description}`;
          const link = item.href
            ? `<a class="deliverable-link" href="${item.href}">${body}</a>`
            : `<div class="deliverable-link missing" aria-disabled="true">${body}</div>`;
          const actions = Array.isArray(item.actions) && item.actions.length
            ? `<div class="deliverable-actions">${item.actions.map(action => {
              if (action.prompt) {
                return info(action, "prompt");
              }
              if (action.copy_path) {
                return `<button class="deliverable-action" type="button" data-copy-file="${escapeHtml(action.copy_path)}" data-copy-mode="${escapeHtml(action.copy_mode || "prompt")}">${escapeHtml(action.label || "Copy")}</button>`;
              }
              const actionHref = String(action.href || "#");
              const opensPdf = actionHref.includes(".pdf");
              return `<a class="deliverable-action" href="${escapeHtml(actionHref)}"${opensPdf ? " target=\"_blank\" rel=\"noreferrer\" data-no-inline=\"true\"" : ""}>${escapeHtml(action.label || "Open")}</a>`;
            }).join("")}</div>`
            : "";
          return `<div class="deliverable-doc">${link}${actions}</div>`;
        }).join("");
        return `<div class="stage deliverables-stage ${child ? "child" : ""}"><div class="deliverables-head"><div class="deliverables-title">${dot(stage.status)} ${escapeHtml(stageNames[key] || key)}</div><div class="deliverables-meta"><span>${escapeHtml(label)}</span></div></div><div class="deliverable-links">${docs}</div></div>`;
      }
      return `<div class="stage ${child ? "child" : ""}"><a class="stage-link" href="${href}"><div class="stage-name">${dot(stage.status)} ${escapeHtml(stageNames[key] || key)}</div>${renderProgress(stage)}</a><div class="stage-label">${labelElement}</div>${info(stage.action)}</div>`;
    }
    function renderLearningBreakdown(title, values) {
      const rows = Object.entries(values || {}).filter(([, value]) => Number(value) > 0);
      if (!rows.length) return `<section class="learning-section"><div class="learning-section-head"><div class="learning-section-title">${title}</div></div><div class="learning-row"><span>No signals yet</span><strong>0</strong></div></section>`;
      return `<section class="learning-section"><div class="learning-section-head"><div class="learning-section-title">${title}</div></div><div class="learning-list">${rows.map(([key, value]) => `<div class="learning-row"><span>${escapeHtml(learningLabel(key))}</span><strong>${value}</strong></div>`).join("")}</div></section>`;
    }
    function trendText(trend) {
      if (!trend || !trend.direction) return "Need more rounds/projects";
      if (trend.direction === "up") return "More iteration than earlier";
      if (trend.direction === "down") return "Less iteration than earlier";
      if (trend.direction === "flat") return "Similar to earlier";
      return escapeHtml(trend.label || "Need more rounds/projects");
    }
    function feedbackThemeStatus(value) {
      const total = Number((value && value.total) || 0);
      const iterated = Number((value && value.iteration_rate) || 0);
      if (!total) return { label: "No feedback yet", className: "unknown" };
      if (iterated >= 70) return { label: "Frequent iteration notes", className: "attention" };
      if (iterated >= 30) return { label: "Some iteration notes", className: "attention" };
      if (iterated > 0) return { label: "Mostly small notes", className: "flat" };
      return { label: "Confirmation notes", className: "good" };
    }
    function learningDisplayTitle(item) {
      const raw = String((item && item.id) || "Learning").replace(/^LL-/, "");
      const words = raw.replace(/[-_]+/g, " ").trim().split(/\s+/).filter(Boolean);
      const known = {
        ai: "AI",
        api: "API",
        pdf: "PDF",
        ppt: "PowerPoint",
        ui: "UI",
        ux: "UX",
        os: "OS",
        ll: "Looped Learning",
        codex: "Codex",
        cowork: "Cowork",
        slack: "Slack",
        markdown: "Markdown"
      };
      return words.map((word, index) => {
        const lower = word.toLowerCase();
        if (known[lower]) return known[lower];
        return index === 0 ? lower.charAt(0).toUpperCase() + lower.slice(1) : lower;
      }).join(" ");
    }
    function recentLearningList(items, href) {
      const rows = Array.isArray(items) ? items.slice(0, 5) : [];
      if (!rows.length) return `<p>No active learnings yet.</p>`;
      const list = `<ol class="learning-recent-list">${rows.map((item, index) => `<li class="learning-recent-item"><span class="learning-recent-number">${index + 1}</span><div><strong>${escapeHtml(learningDisplayTitle(item))}</strong><p>${escapeHtml(item.rule || "No rule text found.")}</p></div></li>`).join("")}</ol>`;
      const more = href ? `<a class="learning-more-link" href="${escapeHtml(href)}">See more learnings</a>` : "";
      return `${list}${more}`;
    }
    function interpretationCard(interpretation) {
      const item = interpretation || {};
      const details = Array.isArray(item.details) ? item.details : [];
      const labels = ["Volume", "Where", "Theme"];
      const detailHtml = details.length ? `<div class="learning-context-points">${details.map((detail, index) => `<div class="learning-context-point"><span>${escapeHtml(labels[index] || "Context")}</span>${escapeHtml(detail)}</div>`).join("")}</div>` : "";
      const trend = item.trend ? `<div class="learning-context-trend"><span>Trend</span>${escapeHtml(item.trend)}</div>` : "";
      return `<section class="learning-card learning-context-card"><h2>What this means</h2><div class="learning-context-summary">${escapeHtml(item.headline || "Looped Learning explains what your review feedback is teaching Research OS.")}</div>${detailHtml}${trend}</section>`;
    }
    function renderQualityBreakdown(title, values) {
      const rows = Object.entries(values || {}).filter(([, value]) => Number(value && value.total) > 0);
      if (!rows.length) return `<section class="learning-section"><div class="learning-section-head"><div><div class="learning-section-title">${title}</div><div class="mini-sub">No captured review feedback yet.</div></div></div><div class="learning-row"><span>No feedback yet</span><strong>0</strong></div></section>`;
      return `<section class="learning-section"><div class="learning-section-head"><div><div class="learning-section-title">${title}</div><div class="mini-sub">This counts feedback signals, not the amount of text that changed. One small note can count as an iteration signal.</div></div></div><div class="learning-list">${rows.map(([key, value]) => {
        const accepted = Number(value.good_rate || 0);
        const iterated = Number(value.iteration_rate || 0);
        const total = Number(value.total || 0);
        const iterationCount = Number(value.iterated || 0);
        const acceptedCount = Number(value.good || 0);
        const status = feedbackThemeStatus(value);
        return `<div class="learning-row learning-quality-row"><span>${escapeHtml(learningLabel(key))}</span><div class="learning-rate"><div class="learning-rate-bar" title="${acceptedCount} accepted note${acceptedCount === 1 ? "" : "s"}, ${iterationCount} iteration note${iterationCount === 1 ? "" : "s"}"><div class="learning-rate-good" style="width:${accepted}%"></div><div class="learning-rate-iterated" style="width:${iterated}%"></div></div><div class="learning-rate-meta"><span>${total} signal${total === 1 ? "" : "s"} captured</span><span>${iterationCount} iteration note${iterationCount === 1 ? "" : "s"}</span></div></div><strong class="trend ${status.className}">${escapeHtml(status.label)}</strong></div>`;
      }).join("")}</div></section>`;
    }
    function renderLearning(metrics) {
      const reviewQueue = metrics.suggestions_pending ? `<section class="learning-section"><div class="learning-section-head"><div><div class="learning-section-title">Learning review queue</div><div class="mini-sub">Research OS-wide rules inferred from your review notes</div></div><div><a class="stage-cta review" href="${metrics.suggestions_href}">Review learning suggestions</a></div></div></section>` : "";
      const latest = metrics.latest_run || {};
      const latestStamp = latest.timestamp || latest.created_at || "";
      const latestText = latestStamp ? `${escapeHtml(latest.status || "completed")} · ${escapeHtml(new Date(latestStamp).toLocaleString([], { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" }))}` : "No learning loop yet";
      const quality = metrics.quality_overall || {};
      const learningSentence = `We have captured ${Number(metrics.signals || 0)} review-feedback signals. These are notes and decisions, not a percentage of the text that was wrong. They have produced ${Number(metrics.active_learnings || 0)} active Research OS learnings, and ${Number(metrics.suggestions_pending || 0)} suggested learning${Number(metrics.suggestions_pending || 0) === 1 ? "" : "s"} still need${Number(metrics.suggestions_pending || 0) === 1 ? "s" : ""} your review.`;
      const learningPrompt = info({
        label: "Run learning",
        button_label: "Run learning",
        copy_label: "run learning",
        instruction: metrics.signals_waiting ? "New review feedback is waiting to be processed into learning suggestions." : "Looped Learning is up to date. You can still ask Codex to check whether active learnings and suggestions are consistent.",
        prompt: metrics.prompt || ""
      }, "prompt");
      return `<section class="learning-card learning-intro">
        <h2>Looped Learning</h2>
        <p>This page shows what Research OS is learning from your review feedback. It tracks review notes, turns recurring feedback into reusable Research OS-wide suggestions, and shows which active learnings should guide future Codex or Claude synthesis.</p>
      </section>
      <div class="learning-top-grid">
        <section class="learning-card">
          <h2>Learning loop status</h2>
          <p>${escapeHtml(learningSentence)}</p>
          <div class="learning-status-line"><span class="phase-status ${metrics.status || "gray"}">${dot(metrics.status || "gray")}${escapeHtml(metrics.status_label || "not started")}</span>${learningPrompt}</div>
          <div class="trend">Last learning loop: ${latestText}</div>
          <div class="learning-status-metrics">
            <div class="learning-mini-metric"><strong>${metrics.signals || 0}</strong><span>captured feedback signals</span></div>
            <div class="learning-mini-metric"><strong>${quality.iterated || 0}</strong><span>iteration feedback signals</span></div>
            <div class="learning-mini-metric"><strong>${metrics.active_learnings || 0}</strong><span>active learnings</span></div>
            <div class="learning-mini-metric"><strong>${metrics.signals_waiting || 0}</strong><span>signals to process</span></div>
          </div>
        </section>
        ${interpretationCard(metrics.learning_interpretation)}
      </div>
      ${reviewQueue}
      <div class="learning-detail-grid">
        <div class="learning-analysis-stack">
          ${renderQualityBreakdown("Where feedback asks us to improve", metrics.quality_by_stage)}
          ${renderQualityBreakdown("Recurring improvement themes", metrics.quality_by_theme)}
        </div>
        <section class="learning-card">
          <h2>Latest learnings</h2>
          <p>The last Research OS-wide rules that were approved from your review feedback.</p>
          ${recentLearningList(metrics.recent_active_learnings, metrics.active_learnings_href)}
        </section>
      </div>`;
    }
    function onboardingBasics(mode = "tab") {
      const empty = mode === "empty";
      const action = info(newProjectAction(), "prompt");
      const setupAction = info(workspaceSetupAction(), "prompt");
      const miniDashboard = `<div class="onboarding-mini-dashboard" aria-hidden="true">
        <div class="onboarding-mini-head"><div class="onboarding-mini-title">Example round status</div><span class="phase-status yellow">${dot("yellow")}2 to review</span></div>
        <div class="onboarding-stage"><strong>Sources</strong><div class="bar"><span class="fill green only" style="width:100%"></span></div><span class="badge green">${dot("green")}ready</span></div>
        <div class="onboarding-stage"><strong>Evidence</strong><div class="bar"><span class="fill green only" style="width:100%"></span></div><span class="badge green">${dot("green")}curated</span></div>
        <div class="onboarding-stage"><strong>Patterns</strong><div class="bar"><span class="fill yellow" style="width:35%"></span><span class="fill green" style="width:65%"></span></div><span class="badge yellow">${dot("yellow")}review</span></div>
        <div class="onboarding-stage"><strong>Output</strong><div class="bar"><span class="fill gray only" style="width:100%"></span></div><span class="badge gray">${dot("gray")}later</span></div>
      </div>`;
      const introTitle = empty ? "Start with your first research project" : "Research OS basics";
      const introCopy = empty
        ? "Research OS turns source material into traceable research knowledge and then into deliverables. Start by copying the workspace prompt below into Codex or Claude, then create a project for the product area or topic you want to track."
        : "Research OS is a local workspace for turning research sources into evidence, patterns, insights, recommendations and reviewable deliverables. AI helps process and draft; you stay in control of what gets accepted.";
      const introStatus = empty
        ? `<span class="phase-status yellow">${dot("yellow")}Create your first project to begin</span>`
        : `<span class="phase-status green">${dot("green")}Researcher-controlled knowledge pipeline</span>`;
      const introAction = empty ? `<div class="onboarding-actions">${setupAction}${action}</div>` : "";
      const intro = `<section class="onboarding-hero"><div><h2>${introTitle}</h2><p>${introCopy}</p>${introAction}${introStatus}</div>${miniDashboard}</section>`;
      const sidebarHint = empty ? `<section class="onboarding-card onboarding-info-card">
            <h3>Find these basics later</h3>
            <div class="onboarding-sidebar-demo">
              <div class="demo-rail" aria-hidden="true">
                <span class="demo-tab"><span class="rail-icon" style="--icon:url('/assets/icons/flask.svg')"></span></span>
                <span class="demo-tab"><span class="rail-icon" style="--icon:url('/assets/icons/lightbulb.svg')"></span></span>
                <span class="demo-spacer"></span>
                <span class="demo-tab demo-info"><span class="rail-icon" style="--icon:url('/assets/icons/info.svg')"></span></span>
                <span class="demo-tab"><span class="rail-icon" style="--icon:url('/assets/icons/settings.svg')"></span></span>
              </div>
              <div class="demo-arrow">Open the i page in the sidebar whenever you want this guide again.</div>
            </div>
            <p>The dashboard only shows the next action for active work. The i page keeps the basic explanation available without crowding your research rounds.</p>
          </section>` : "";
      return `<div class="onboarding">
        ${intro}
        <div class="onboarding-grid">
          ${sidebarHint}
          <section class="onboarding-card">
            <h3>How the workspace is organized</h3>
            <div class="onboarding-folder-card">
              <div class="onboarding-folder-row"><span class="dot blue"></span><strong>Project</strong><span>long-running topic</span></div>
              <div class="onboarding-folder-row"><span class="dot green"></span><strong>Round</strong><span>one study or cycle</span></div>
              <div class="onboarding-folder-row"><span class="dot yellow"></span><strong>Input</strong><span>source material</span></div>
              <div class="onboarding-folder-row"><span class="dot gray"></span><strong>Output</strong><span>deliverables</span></div>
            </div>
            <p>Projects are long-running product areas or topics. Rounds are individual studies, interview batches, evaluations or synthesis cycles inside a project.</p>
          </section>
          <section class="onboarding-card">
            <h3>What you can put in input folders</h3>
            <div class="onboarding-pill-list">
              <span class="onboarding-pill">project context</span>
              <span class="onboarding-pill">transcripts</span>
              <span class="onboarding-pill">presentations</span>
              <span class="onboarding-pill">PDFs</span>
              <span class="onboarding-pill">research notes</span>
              <span class="onboarding-pill">screenshots</span>
              <span class="onboarding-pill">survey exports</span>
              <span class="onboarding-pill">product docs</span>
            </div>
            <p>Use project input for durable background. Use round input for material from a specific study.</p>
          </section>
          <section class="onboarding-card">
            <h3>How the pipeline works</h3>
            <div class="onboarding-mini-dashboard">
              <div class="onboarding-stage"><strong>Sources</strong><div class="bar"><span class="fill blue only" style="width:100%"></span></div><span>input</span></div>
              <div class="onboarding-stage"><strong>Evidence</strong><div class="bar"><span class="fill green only" style="width:100%"></span></div><span>observed</span></div>
              <div class="onboarding-stage"><strong>Patterns</strong><div class="bar"><span class="fill yellow only" style="width:100%"></span></div><span>review</span></div>
              <div class="onboarding-stage"><strong>Insights</strong><div class="bar"><span class="fill yellow only" style="width:100%"></span></div><span>meaning</span></div>
              <div class="onboarding-stage"><strong>Recs</strong><div class="bar"><span class="fill green only" style="width:100%"></span></div><span>next</span></div>
            </div>
            <p>The AI moves one safe stage at a time. Evidence stays source-faithful; you review the synthesis layers before they feed deliverables.</p>
          </section>
          <section class="onboarding-card">
            <h3>How the purple AI buttons work</h3>
            <div class="onboarding-actions">${info({
              label: "Example AI prompt",
              button_label: "AI prompt",
              copy_label: "example onboarding",
              instruction: "Purple AI buttons copy a ready-made prompt for Codex, Claude or another AI tool.",
              prompt_description: "This is an example only. In the dashboard, each purple button copies a prompt for that exact project, round, stage or deliverable.",
              prompt: "Paste dashboard prompts into Codex or Claude when you want the AI to work on your local Research OS files."
            }, "prompt")}</div>
            <ol>
              <li>Click a purple AI button to copy the right prompt.</li>
              <li>Paste it into Codex, Claude or another AI tool that can access your <code>UX Research</code> folder.</li>
              <li>The AI updates local Research OS files and reports what changed.</li>
              <li>Refresh the dashboard, then review anything marked yellow.</li>
            </ol>
          </section>
          <section class="onboarding-card">
            <h3>What to do now</h3>
            <div class="onboarding-actions">${setupAction}</div>
            <ol>
              <li>Click <strong>Read workspace prompt</strong>, then paste it into Codex, Claude or another AI tool that can access your <code>UX Research</code> folder.</li>
              <li>Create your first project from the dashboard.</li>
              <li>Add project context sources if you have durable background.</li>
              <li>Create a round, add transcripts or notes, then use Run input.</li>
              <li>Review what needs your judgment, then continue synthesis stage by stage.</li>
            </ol>
          </section>
        </div>
      </div>`;
    }
    function formatUpdateTime(value) {
      if (!value) return "Not checked yet";
      const date = new Date(value);
      if (Number.isNaN(date.getTime())) return "Unknown";
      return date.toLocaleString([], { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });
    }
    function renderUpdateCard(update) {
      const item = update || {};
      const hasUpdate = Boolean(item.update_available);
      const statusClass = hasUpdate ? "yellow" : (item.status === "ok" ? "green" : "gray");
      const headline = hasUpdate ? "A new Research OS version is available." : (item.status === "error" ? "Could not check for updates." : "Research OS is up to date.");
      const detail = hasUpdate
        ? "Update from GitHub when you are ready. Your local Projects folder is separate from the Research OS code."
        : (item.status === "error" ? escapeHtml(item.error || "The GitHub check failed. You can try again later.") : `Research OS checks GitHub about every ${escapeHtml(item.check_interval_hours || 12)} hours.`);
      const updateHelp = hasUpdate ? `<p>Run this in Terminal to update Research OS:</p><pre class="update-command">${escapeHtml(item.update_command || "")}</pre>` : "";
      return `<section class="settings-card update-card ${statusClass}">
        <h2>Research OS version</h2>
        <p>${headline} ${detail}</p>
        <div class="update-meta-grid">
          <div class="update-meta-item"><span>Current</span><strong>${escapeHtml(item.current_version || "unknown")}</strong></div>
          <div class="update-meta-item"><span>GitHub</span><strong>${escapeHtml(item.latest_version || "unknown")}</strong></div>
          <div class="update-meta-item"><span>Last checked</span><strong>${escapeHtml(formatUpdateTime(item.checked_at))}</strong></div>
        </div>
        ${updateHelp}
        <div class="update-actions">
          ${item.update_command ? `<button class="settings-save" type="button" data-copy-text="${escapeHtml(item.update_command)}" data-copy-label="update command">Copy update command</button>` : ""}
          <button class="settings-reset" type="button" id="checkUpdatesButton">Check now</button>
          <a class="settings-link" href="${escapeHtml(item.release_notes_url || "https://github.com/Jiptv/Research-OS/blob/main/CHANGELOG.md")}" target="_blank" rel="noreferrer">Read release notes</a>
        </div>
      </section>`;
    }
    function renderSettings(settings) {
      const item = settings || {};
      const exists = value => value ? "exists" : "missing";
      const refreshMinutes = Math.max(1, Math.round(Number(item.refresh_seconds || 900) / 60));
      const lenses = item.research_lenses || [];
      const selectedLens = item.default_research_lens || "neutral";
      const lensOptions = lenses.map(lens => `<option value="${escapeHtml(lens.key)}" ${lens.key === selectedLens ? "selected" : ""}>${escapeHtml(lens.label || lens.key)}</option>`).join("");
      return `<div class="settings-grid">
        ${renderUpdateCard(item.update_status || {})}
        <section class="settings-card">
          <h2>Folders</h2>
          <p>Research OS works from one workspace folder on your Mac. That folder should contain Research OS/ and Projects/ next to each other.</p>
          <form class="settings-form" id="settingsForm">
            <div class="settings-field">
              <label>Research OS folder</label>
              <div class="settings-path-display">${escapeHtml(item.research_os_display_dir || item.research_os_dir || "")}</div>
              <div class="settings-meta">Mac folder, ${exists(item.research_os_exists)}. This is where the dashboard and Research OS code live on your computer.</div>
            </div>
            <div class="settings-field">
              <label for="projectsDir">Projects folder</label>
              <input id="projectsDir" name="projects_dir" type="text" value="${escapeHtml(item.projects_display_dir || item.projects_dir || "")}" autocomplete="off" spellcheck="false">
              <div class="settings-meta">Mac folder for research projects. Keep this next to the Research OS folder, for example in your UX Research workspace.</div>
            </div>
            <label class="settings-toggle" for="backupEnabled">
              <input id="backupEnabled" name="backup_enabled" type="checkbox" ${item.backup_enabled ? "checked" : ""}>
              <span><strong>Show iCloud backup controls</strong><span>Off by default. Turn this on if you want Research OS to show backup status and the Sync to iCloud button on the dashboard.</span></span>
            </label>
            <div class="settings-field">
              <label for="backupDir">Backup destination</label>
              <input id="backupDir" name="backup_dir" type="text" value="${escapeHtml(item.backup_dir || "")}" autocomplete="off" spellcheck="false">
              <div class="settings-meta">Used only when iCloud backup controls are enabled. The backup button syncs both Research OS and Projects into this backup folder.</div>
            </div>
            <div class="settings-field">
              <label for="refreshMinutesInput">Dashboard refresh interval</label>
              <input id="refreshMinutesInput" name="refresh_minutes" type="number" min="1" max="60" step="1" value="${escapeHtml(refreshMinutes)}">
              <div class="settings-meta">Auto-refresh frequency in minutes. Saved range: 1-60 minutes.</div>
            </div>
            <div class="settings-field">
              <label for="defaultResearchLens">Default research lens for new rounds</label>
              <select id="defaultResearchLens" name="default_research_lens">${lensOptions}</select>
              <div class="settings-meta">Used only when creating new rounds. Existing rounds keep their selected lens.</div>
            </div>
            <div class="settings-actions">
              <button class="settings-save" type="submit">Save settings</button>
              <button class="settings-reset" type="button" id="reloadSettings">Reload</button>
              <span class="settings-meta" id="settingsStatus">Settings file: ${escapeHtml(item.settings_display_file || item.settings_file || "")}</span>
            </div>
          </form>
        </section>
      </div>`;
    }
    function setActiveTab(tab) {
      activeTab = tab;
      localStorage.setItem("research-os-dashboard-tab", tab);
      document.querySelectorAll(".rail-tab").forEach(button => button.classList.toggle("active", button.dataset.tab === tab));
      document.getElementById("dashboardPanel").classList.toggle("active", tab === "dashboard");
      document.getElementById("learningPanel").classList.toggle("active", tab === "learning");
      document.getElementById("aboutPanel").classList.toggle("active", tab === "about");
      document.getElementById("settingsPanel").classList.toggle("active", tab === "settings");
    }
    function inlineTitleFromLink(link) {
      const explicit = link.querySelector("strong") || link.querySelector(".review-item-title") || link.querySelector(".stage-name") || link;
      return explicit.textContent.trim().replace(/\s+/g, " ") || "Document";
    }
    function inlineContainerFor(link) {
      const reviewProject = link.closest(".review-project");
      if (reviewProject) return reviewProject;
      return link.closest(".round-body, .project-body") || document.getElementById("overviewView");
    }
	    function openInlineDocument(link, options = {}) {
	      const href = link.getAttribute("href");
	      if (!href || !href.startsWith("/file")) return false;
	      if (link.dataset.noInline === "true" || href.includes(".pdf")) return false;
	      if (href.includes("mode=focus")) return false;
      if (href.includes("review-queue.md") || href.includes("project-context-proposals.md")) return false;
      const container = inlineContainerFor(link);
      const title = inlineTitleFromLink(link);
      container.querySelector(":scope > .inline-viewer")?.remove();
      container.classList.add("document-open");
      const viewer = document.createElement("section");
      viewer.className = "inline-viewer";
      viewer.innerHTML = `<div class="inline-viewer-head"><div class="inline-viewer-title">${escapeHtml(title)}</div><div class="inline-viewer-actions"><a href="${href}">Open full page</a><button type="button">Close</button></div></div><iframe src="${href}" title="${escapeHtml(title)}"></iframe>`;
      viewer.querySelector("button").addEventListener("click", () => {
        viewer.remove();
        container.classList.remove("document-open");
        inlineState = null;
        refresh();
      });
      container.prepend(viewer);
      if (!options.restore) {
        inlineState = { href };
        viewer.scrollIntoView({ block: "nearest" });
      }
      return true;
    }
    function restoreInlineDocument() {
      if (!inlineState) return;
      const link = document.querySelector(`a[href="${CSS.escape(inlineState.href)}"]`);
      if (link) openInlineDocument(link, { restore: true });
    }
    function formatBackupTime(value) {
      if (!value) return "never";
      const date = new Date(value);
      if (Number.isNaN(date.getTime())) return "unknown";
      return date.toLocaleString([], { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });
    }
    function renderBackupStatus(status) {
      const el = document.getElementById("backupStatus");
      const button = document.getElementById("backupButton");
      const state = status.status || "unknown";
      const enabled = status.enabled !== false;
      el.hidden = !enabled;
      button.hidden = !enabled;
      if (!enabled) return;
      el.className = `backup-status ${state === "ok" ? "green" : state === "running" ? "yellow" : state === "error" ? "red" : "gray"}`;
      if (state === "running") {
        el.textContent = `Backup: running · last ${formatBackupTime(status.last_backup_at)}`;
        button.textContent = "Backing up...";
        button.disabled = true;
        return;
      }
      if (state === "error") {
        el.textContent = `Backup: failed · last ${formatBackupTime(status.last_backup_at)}`;
      } else {
        el.textContent = `Last backup: ${formatBackupTime(status.last_backup_at)}`;
      }
      button.textContent = "Sync to iCloud";
      button.disabled = false;
    }
    function renderVersionStatus(update) {
      const button = document.getElementById("versionButton");
      if (!button) return;
      const hasUpdate = Boolean(update && update.update_available);
      button.hidden = !hasUpdate;
      if (hasUpdate) {
        button.textContent = "New version available";
        button.title = `Current: ${(update && update.current_version) || "unknown"} · GitHub: ${(update && update.latest_version) || "unknown"}`;
      }
    }
    async function refreshBackupStatus() {
      try {
        const response = await fetch("/api/backup", { cache: "no-store" });
        renderBackupStatus(await response.json());
      } catch (error) {
        renderBackupStatus({ status: "error", last_backup_at: "", message: "Could not read backup status." });
      }
    }
    async function startBackup() {
      const button = document.getElementById("backupButton");
      button.disabled = true;
      button.textContent = "Starting...";
      try {
        const response = await fetch("/api/backup", { method: "POST" });
        renderBackupStatus(await response.json());
      } catch (error) {
        renderBackupStatus({ status: "error", last_backup_at: "", message: "Could not start backup." });
      }
    }
    function render(payload) {
      lastPayload = payload;
      document.getElementById("refreshMinutes").textContent = Math.max(1, Math.round(payload.refresh_seconds / 60));
      scheduleDashboardRefresh(payload.refresh_seconds);
      setUpdatedText(`Updated ${new Date(payload.generated_at).toLocaleTimeString()}`);
      renderVersionStatus(payload.update_status || (payload.settings && payload.settings.update_status) || {});
      document.getElementById("toolbarActions").innerHTML = info(newProjectAction(), "prompt");
      const q = document.getElementById("search").value.trim().toLowerCase();
      const projects = payload.projects.filter(project => !q || project.name.toLowerCase().includes(q) || project.path.toLowerCase().includes(q));
      document.getElementById("projects").innerHTML = payload.projects.length ? (projects.length ? projects.map(renderProject).join("") : `<div class="empty">No matching projects.</div>`) : onboardingBasics("empty");
      document.getElementById("learningPanel").innerHTML = renderLearning(payload.looped_learning || {});
      document.getElementById("aboutPanel").innerHTML = onboardingBasics("tab");
      document.getElementById("settingsPanel").innerHTML = renderSettings(payload.settings || {});
      setActiveTab(activeTab);
      document.querySelectorAll("[data-toggle]").forEach(button => button.addEventListener("click", () => { const id = button.getAttribute("data-toggle"); const container = button.closest(".project-info-section, .project, .round"); saveOpen(id, !container.classList.contains("open")); render(lastPayload); }));
      function closeTips() {
        document.querySelectorAll(".tip-open").forEach(item => item.classList.remove("tip-open"));
      }
      function showToast(message) {
        const toast = document.getElementById("toast");
        if (!toast) return;
        toast.textContent = message;
        toast.classList.add("show");
        clearTimeout(toast._timer);
        toast._timer = setTimeout(() => toast.classList.remove("show"), 2200);
      }
      function fallbackCopyText(text) {
        const area = document.createElement("textarea");
        area.value = text;
        area.setAttribute("readonly", "");
        area.style.position = "fixed";
        area.style.left = "-9999px";
        area.style.top = "0";
        document.body.appendChild(area);
        area.select();
        let copied = false;
        try {
          copied = document.execCommand("copy");
        } catch (error) {
          copied = false;
        }
        document.body.removeChild(area);
        return copied;
      }
      async function copyPromptText(text) {
        if (fallbackCopyText(text)) return true;
        if (!navigator.clipboard || !navigator.clipboard.writeText) return false;
        try {
          await navigator.clipboard.writeText(text);
          return true;
        } catch (error) {
          return false;
        }
      }
      async function copyText(text) {
        return copyPromptText(text);
      }
      function positionTip(wrap) {
        const tip = wrap.querySelector(".tip");
        if (!tip) return;
        tip.style.left = "16px";
        tip.style.top = "16px";
        const trigger = wrap.getBoundingClientRect();
        const tipWidth = Math.min(tip.offsetWidth || 420, window.innerWidth - 32);
        const tipHeight = Math.min(tip.offsetHeight || 240, window.innerHeight - 32);
        let left = trigger.left;
        if (wrap.closest(".badges, .project-part-actions, .deliverable-actions, .deliverables-meta, .toolbar-actions")) {
          left = trigger.right - tipWidth;
        }
        left = Math.max(16, Math.min(left, window.innerWidth - tipWidth - 16));
        let top = trigger.bottom + 8;
        if (top + tipHeight > window.innerHeight - 16) {
          top = trigger.top - tipHeight - 8;
        }
        top = Math.max(16, Math.min(top, window.innerHeight - tipHeight - 16));
        tip.style.left = `${left}px`;
        tip.style.top = `${top}px`;
      }
      function openTip(wrap) {
        closeTips();
        clearTimeout(wrap._tipCloseTimer);
        wrap.classList.add("tip-open");
        positionTip(wrap);
      }
      function scheduleTipClose(wrap) {
        clearTimeout(wrap._tipCloseTimer);
        wrap._tipCloseTimer = setTimeout(() => {
          if (!wrap.matches(":hover") && !wrap.contains(document.activeElement)) {
            wrap.classList.remove("tip-open");
          }
        }, 180);
      }
      document.querySelectorAll(".info-wrap").forEach(wrap => {
        wrap.addEventListener("pointerenter", () => openTip(wrap));
        wrap.addEventListener("pointerleave", () => scheduleTipClose(wrap));
      });
      document.querySelectorAll(".info").forEach(button => button.addEventListener("click", event => {
        event.preventDefault();
        event.stopPropagation();
        if (button.hasAttribute("data-prompt")) return;
        const wrap = button.closest(".info-wrap");
        const wasOpen = wrap.classList.contains("tip-open");
        closeTips();
        if (!wasOpen) openTip(wrap);
      }));
	      document.querySelectorAll("[data-prompt]").forEach(button => button.addEventListener("click", async event => {
        event.preventDefault();
        event.stopPropagation();
        const prompt = button.getAttribute("data-prompt") || "";
        const label = button.getAttribute("data-copy-label") || "prompt";
        closeTips();
        const copied = await copyPromptText(prompt);
        showToast(copied ? `Copied '${label}' prompt` : "Could not copy prompt");
	      }));
	      document.querySelectorAll("[data-copy-file]").forEach(button => button.addEventListener("click", async event => {
	        event.preventDefault();
	        event.stopPropagation();
	        const label = button.textContent || "Copy prompt";
	        const path = button.getAttribute("data-copy-file") || "";
	        const mode = button.getAttribute("data-copy-mode") || "prompt";
	        try {
	          const response = await fetch(`/api/file-text?path=${encodeURIComponent(path)}&mode=${encodeURIComponent(mode)}`, { cache: "no-store" });
	          const payload = await response.json();
	          if (!response.ok || payload.error) throw new Error(payload.error || "Could not read file");
	          await navigator.clipboard.writeText(payload.text || "");
	          button.textContent = "Copied";
	          setTimeout(() => { button.textContent = label; }, 1200);
	        } catch (error) {
	          button.textContent = "Open and copy";
	          setTimeout(() => { button.textContent = label; }, 1800);
		        }
		      }));
      document.querySelectorAll("[data-copy-text]").forEach(button => button.addEventListener("click", async event => {
        event.preventDefault();
        event.stopPropagation();
        const label = button.getAttribute("data-copy-label") || "text";
        const original = button.textContent || "Copy";
        const copied = await copyText(button.getAttribute("data-copy-text") || "");
        button.textContent = copied ? "Copied" : "Could not copy";
        showToast(copied ? `Copied ${label}` : `Could not copy ${label}`);
        setTimeout(() => { button.textContent = original; }, 1300);
      }));
	      document.querySelectorAll("[data-waive-gates]").forEach(button => button.addEventListener("click", async event => {
	        event.preventDefault();
	        event.stopPropagation();
	        const label = button.textContent || "Accept visible gates";
	        const path = button.getAttribute("data-waive-path") || "";
	        let gates = [];
	        try {
	          gates = JSON.parse(decodeURIComponent(button.getAttribute("data-waive-gates") || "[]"));
	          const response = await fetch("/api/quality-gate-waivers", {
	            method: "POST",
	            headers: { "Content-Type": "application/json" },
	            body: JSON.stringify({ path, gates, reason: "Accepted in the Research OS dashboard." })
	          });
	          const payload = await response.json();
	          if (!response.ok || payload.error) throw new Error(payload.error || "Could not accept quality gates");
	          button.textContent = "Accepted";
	          setTimeout(refresh, 250);
	        } catch (error) {
	          button.textContent = "Could not accept";
	          setTimeout(() => { button.textContent = label; }, 1800);
	        }
	      }));
      document.querySelectorAll("[data-round-lens]").forEach(select => select.addEventListener("change", async event => {
        const path = select.getAttribute("data-round-lens") || "";
        const original = select.dataset.previousValue || "";
        select.disabled = true;
        try {
          const response = await fetch("/api/round-lens", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ path, research_lens: select.value })
          });
          const payload = await response.json();
          if (!response.ok || payload.error) throw new Error(payload.error || "Could not update lens");
          setTimeout(refresh, 150);
        } catch (error) {
          if (original) select.value = original;
          alert(error.message || "Could not update research lens");
          select.disabled = false;
        }
      }));
      document.querySelectorAll("[data-round-lens]").forEach(select => { select.dataset.previousValue = select.value; });
      document.querySelectorAll("[data-round-monitoring]").forEach(input => input.addEventListener("change", async event => {
        event.preventDefault();
        event.stopPropagation();
        const path = input.getAttribute("data-round-monitoring") || "";
        const original = !input.checked;
        input.disabled = true;
        try {
          const response = await fetch("/api/round-monitoring", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ path, monitored: input.checked })
          });
          const payload = await response.json();
          if (!response.ok || payload.error) throw new Error(payload.error || "Could not update monitoring");
          showToast(input.checked ? "Round monitoring is on" : "Round monitoring is off");
          setTimeout(refresh, 150);
        } catch (error) {
          input.checked = original;
          input.disabled = false;
          alert(error.message || "Could not update monitoring");
        }
      }));
      const settingsForm = document.getElementById("settingsForm");
      if (settingsForm) {
        settingsForm.addEventListener("submit", async event => {
          event.preventDefault();
          const status = document.getElementById("settingsStatus");
          const payload = {
            projects_dir: document.getElementById("projectsDir").value.trim(),
            backup_dir: document.getElementById("backupDir").value.trim(),
            backup_enabled: document.getElementById("backupEnabled").checked,
            refresh_seconds: Math.max(1, Number(document.getElementById("refreshMinutesInput").value || 15)) * 60,
            default_research_lens: document.getElementById("defaultResearchLens").value
          };
          if (status) status.textContent = "Saving...";
          try {
            const response = await fetch("/api/settings", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(payload)
            });
            const body = await response.json();
            if (!response.ok || body.error) throw new Error(body.error || "Could not save settings");
            showToast("Settings saved");
            setTimeout(() => refresh(true), 200);
          } catch (error) {
            if (status) status.textContent = error.message || "Could not save settings";
          }
        });
      }
      document.getElementById("reloadSettings")?.addEventListener("click", () => refresh(true));
      document.getElementById("checkUpdatesButton")?.addEventListener("click", async event => {
        event.preventDefault();
        const button = event.currentTarget;
        const label = button.textContent || "Check now";
        button.textContent = "Checking...";
        button.disabled = true;
        try {
          const response = await fetch("/api/update-check", { method: "POST" });
          const payload = await response.json();
          if (!response.ok || payload.error) throw new Error(payload.error || "Could not check for updates");
          showToast(payload.update_available ? "New version available" : "Research OS is up to date");
          setTimeout(() => refresh(true), 150);
        } catch (error) {
          button.textContent = "Could not check";
          showToast(error.message || "Could not check for updates");
          setTimeout(() => { button.textContent = label; button.disabled = false; }, 1600);
        }
      });
	      document.querySelectorAll('a[href^="/file"]').forEach(link => link.addEventListener("click", event => {
        if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
        if (openInlineDocument(link)) event.preventDefault();
      }));
      restoreInlineDocument();
    }
    document.getElementById("backupButton").addEventListener("click", startBackup);
    document.getElementById("versionButton").addEventListener("click", () => {
      setActiveTab("settings");
      setTimeout(() => document.querySelector(".update-card")?.scrollIntoView({ block: "start" }), 50);
    });
    document.querySelectorAll(".rail-tab").forEach(button => button.addEventListener("click", () => setActiveTab(button.dataset.tab)));
    document.addEventListener("click", event => {
      if (!event.target.closest(".info-wrap")) {
        document.querySelectorAll(".tip-open").forEach(item => item.classList.remove("tip-open"));
      }
    });
    document.addEventListener("keydown", event => {
      if (event.key === "Escape") {
        document.querySelectorAll(".tip-open").forEach(item => item.classList.remove("tip-open"));
      }
    });
    async function refresh(force = false) {
      if (document.hidden) {
        return;
      }
      if (hasOpenTip()) {
        return;
      }
      if (inlineState) {
        setDashboardLoading(false);
        setUpdatedText("Auto-refresh paused while viewing");
        return;
      }
      if (dashboardRefreshing) return;
      const isInitialLoad = !lastPayload;
      const refreshButton = document.getElementById("refreshButton");
      dashboardRefreshing = true;
      if (refreshButton) {
        refreshButton.disabled = true;
        const label = refreshButton.querySelector("span");
        if (label) label.textContent = "Refreshing...";
      }
      setDashboardLoading(isInitialLoad);
      if (isInitialLoad) setUpdatedText("Loading...");
      try {
        const response = await fetch(`/api/dashboard${force ? "?force=1" : ""}`, { cache: "no-store" });
        render(await response.json());
      } catch (error) {
        document.getElementById("projects").innerHTML = `<div class="empty">Refresh the page, or restart with ./research-os dashboard.</div>`;
        setUpdatedText("Refresh failed");
      } finally {
        dashboardRefreshing = false;
        if (refreshButton) {
          refreshButton.disabled = false;
          const label = refreshButton.querySelector("span");
          if (label) label.textContent = refreshButton.dataset.label || "Refresh dashboard";
        }
        setDashboardLoading(false);
      }
    }
    document.getElementById("search").addEventListener("input", () => lastPayload && render(lastPayload));
    document.getElementById("refreshButton").addEventListener("click", () => refresh(true));
    refresh();
    refreshBackupStatus();
    scheduleDashboardRefresh(refreshIntervalSeconds);
    setInterval(refreshBackupStatus, 60000);
    document.addEventListener("visibilitychange", () => {
      if (!document.hidden) {
        refresh();
        refreshBackupStatus();
      }
    });
  </script>
</body>
</html>
"""


DASHBOARD_MANIFEST = {
    "name": "Research OS Dashboard",
    "short_name": "Research OS",
    "description": "Local dashboard for Research OS projects, rounds, reviews and processing status.",
    "start_url": "/",
    "scope": "/",
    "display": "standalone",
    "background_color": "var(--bg)",
    "theme_color": "#FBFBFA",
    "icons": [
        {
            "src": "/assets/app-icon.png?v=4",
            "sizes": "512x512",
            "type": "image/png",
            "purpose": "any",
        }
    ],
}


DASHBOARD_ICON_SVG = """<svg width="256" height="256" viewBox="0 0 256 256" fill="none" xmlns="http://www.w3.org/2000/svg">
<g clip-path="url(#clip0_15_111)">
<path d="M204 0H52C23.2812 0 0 23.2812 0 52V204C0 232.719 23.2812 256 52 256H204C232.719 256 256 232.719 256 204V52C256 23.2812 232.719 0 204 0Z" fill="#3D74FF"/>
<path d="M77.1073 198C75.6186 198 74.4006 197.526 73.4533 196.579C72.5059 195.632 72.0323 194.414 72.0323 192.925V60.975C72.0323 59.4863 72.5059 58.2683 73.4533 57.321C74.4006 56.3737 75.6186 55.9 77.1073 55.9H132.323C149.781 55.9 163.518 59.96 173.532 68.08C183.682 76.0647 188.757 87.4327 188.757 102.184C188.757 111.793 186.389 119.913 181.652 126.544C177.051 133.175 170.961 138.183 163.382 141.566L191.396 191.504C191.802 192.316 192.005 193.06 192.005 193.737C192.005 194.82 191.532 195.835 190.584 196.782C189.772 197.594 188.757 198 187.539 198H160.743C158.172 198 156.277 197.391 155.059 196.173C153.841 194.82 152.962 193.602 152.42 192.519L129.278 147.859H108.369V192.925C108.369 194.414 107.896 195.632 106.948 196.579C106.001 197.526 104.783 198 103.294 198H77.1073ZM108.369 119.236H131.917C138.278 119.236 143.015 117.68 146.127 114.567C149.375 111.454 150.999 107.191 150.999 101.778C150.999 96.5 149.443 92.237 146.33 88.989C143.353 85.741 138.549 84.117 131.917 84.117H108.369V119.236Z" fill="white"/>
</g>
<defs>
<clipPath id="clip0_15_111">
<rect width="256" height="256" fill="white"/>
</clipPath>
</defs>
</svg>
"""


class DashboardHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        return

    def send_payload(self, body: bytes, content_type: str) -> None:
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path in {"/", "/dashboard"}:
            self.send_payload(DASHBOARD_HTML.encode("utf-8"), "text/html; charset=utf-8")
            return
        if parsed.path == "/api/dashboard":
            params = urllib.parse.parse_qs(parsed.query)
            if params.get("force", [""])[0] == "1":
                invalidate_dashboard_cache()
            body = json.dumps(build_dashboard_payload(), indent=2).encode("utf-8")
            self.send_payload(body, "application/json; charset=utf-8")
            return
        if parsed.path == "/api/health":
            self.send_json(
                {
                    "status": "ok",
                    "service": "research-os-dashboard",
                    "checked_at": now().isoformat(),
                    "projects_dir": rel(projects_dir()),
                }
            )
            return
        if parsed.path == "/api/backup":
            self.send_json(backup_status())
            return
        if parsed.path == "/api/settings":
            self.send_json(dashboard_settings_payload())
            return
        if parsed.path == "/api/file-text":
            params = urllib.parse.parse_qs(parsed.query)
            path_value = params.get("path", [""])[0]
            mode = params.get("mode", [""])[0]
            try:
                target = resolve_dashboard_file(path_value)
                text = read_text(target)
            except Exception as exc:
                self.send_json({"error": str(exc)}, status=400)
                return
            if mode == "prompt":
                text = copyable_prompt_text(text)
            elif mode == "post-it-notes":
                text = copyable_post_it_text(text)
            self.send_json({"text": text})
            return
        if parsed.path == "/manifest.webmanifest":
            body = json.dumps(DASHBOARD_MANIFEST, indent=2).encode("utf-8")
            self.send_payload(body, "application/manifest+json; charset=utf-8")
            return
        if parsed.path == "/app-icon.svg":
            self.send_payload(DASHBOARD_ICON_SVG.encode("utf-8"), "image/svg+xml; charset=utf-8")
            return
        if parsed.path == "/assets/app-icon.png":
            icon_path = ROOT / "assets" / "app-icon.png"
            if icon_path.exists() and icon_path.is_file():
                self.send_payload(icon_path.read_bytes(), "image/png")
                return
            self.send_error(404)
            return
        if parsed.path.startswith("/assets/icons/"):
            icon_name = Path(urllib.parse.unquote(parsed.path)).name
            icon_path = ROOT / "assets" / "icons" / icon_name
            if icon_path.exists() and icon_path.is_file() and icon_path.suffix.lower() in {".png", ".svg"}:
                content_type = "image/svg+xml; charset=utf-8" if icon_path.suffix.lower() == ".svg" else "image/png"
                self.send_payload(icon_path.read_bytes(), content_type)
                return
            self.send_error(404)
            return
        if parsed.path == "/file":
            params = urllib.parse.parse_qs(parsed.query)
            path_value = params.get("path", [""])[0]
            mode = params.get("mode", [""])[0]
            stage = params.get("stage", [""])[0]
            try:
                target = resolve_dashboard_file(path_value)
            except PermissionError:
                self.send_error(403)
                return
            if target.exists() and target.is_file() and target.suffix.lower() == ".pdf":
                body = dashboard_pdf_page(target).encode("utf-8")
                self.send_payload(body, "text/html; charset=utf-8")
                return
            body = dashboard_file_page(path_value, mode=mode, stage=stage).encode("utf-8")
            self.send_payload(body, "text/html; charset=utf-8")
            return
        if parsed.path == "/raw-file":
            params = urllib.parse.parse_qs(parsed.query)
            path_value = params.get("path", [""])[0]
            try:
                target = resolve_dashboard_file(path_value)
            except PermissionError:
                self.send_error(403)
                return
            if target.exists() and target.is_file() and target.suffix.lower() == ".pdf":
                self.send_payload(target.read_bytes(), "application/pdf")
                return
            self.send_error(404)
            return
        if parsed.path == "/api/reviews":
            params = urllib.parse.parse_qs(parsed.query)
            path_value = params.get("path", [""])[0]
            try:
                target = resolve_dashboard_file(path_value)
                items = expanded_review_items(target)
            except Exception as exc:
                self.send_json({"error": str(exc)}, status=400)
                return
            for item in items:
                item.pop("file_path", None)
            self.send_json({"items": items})
            return
        self.send_error(404)

    def do_POST(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/backup":
            self.send_json(start_backup_to_icloud())
            return
        if parsed.path == "/api/quality-gate-waivers":
            try:
                length = int(self.headers.get("Content-Length", "0"))
                payload = json.loads(self.rfile.read(length).decode("utf-8"))
                round_dir = assert_round(resolve_dashboard_file(payload.get("path", "")))
                reason = str(payload.get("reason", "Accepted in the Research OS dashboard."))
                gates = payload.get("gates", [])
                if not isinstance(gates, list):
                    raise ValueError("Expected a list of quality gates.")
                for gate in gates:
                    if not isinstance(gate, dict):
                        continue
                    waive_quality_gate(
                        round_dir,
                        str(gate.get("stage", "")),
                        str(gate.get("id", "")),
                        str(gate.get("message", "")),
                        reason,
                    )
                invalidate_dashboard_cache()
            except Exception as exc:
                self.send_json({"error": str(exc)}, status=400)
                return
            self.send_json({"status": "ok"})
            return
        if parsed.path == "/api/round-lens":
            try:
                length = int(self.headers.get("Content-Length", "0"))
                payload = json.loads(self.rfile.read(length).decode("utf-8"))
                round_dir = assert_round(resolve_dashboard_file(payload.get("path", "")))
                lens = set_round_research_lens(round_dir, str(payload.get("research_lens", "")))
                invalidate_dashboard_cache()
            except Exception as exc:
                self.send_json({"error": str(exc)}, status=400)
                return
            self.send_json({"status": "ok", "research_lens": lens})
            return
        if parsed.path == "/api/round-monitoring":
            try:
                length = int(self.headers.get("Content-Length", "0"))
                payload = json.loads(self.rfile.read(length).decode("utf-8"))
                round_dir = assert_round(resolve_dashboard_file(payload.get("path", "")))
                monitoring = set_round_monitoring(round_dir, payload.get("monitored") is not False)
                invalidate_dashboard_cache()
            except Exception as exc:
                self.send_json({"error": str(exc)}, status=400)
                return
            self.send_json({"status": "ok", **monitoring})
            return
        if parsed.path == "/api/settings":
            try:
                length = int(self.headers.get("Content-Length", "0"))
                payload = json.loads(self.rfile.read(length).decode("utf-8"))
                settings = save_dashboard_settings(payload)
                Path(settings["projects_dir"]).expanduser().mkdir(parents=True, exist_ok=True)
                if settings.get("backup_enabled"):
                    Path(settings["backup_dir"]).expanduser().mkdir(parents=True, exist_ok=True)
                invalidate_dashboard_cache()
            except Exception as exc:
                self.send_json({"error": str(exc)}, status=400)
                return
            self.send_json({"status": "ok", "settings": dashboard_settings_payload()})
            return
        if parsed.path == "/api/update-check":
            try:
                payload = update_status(force=True)
                invalidate_dashboard_cache()
            except Exception as exc:
                self.send_json({"error": str(exc)}, status=400)
                return
            self.send_json(payload)
            return
        if parsed.path == "/api/review-decision":
            try:
                length = int(self.headers.get("Content-Length", "0"))
                payload = json.loads(self.rfile.read(length).decode("utf-8"))
                target = resolve_dashboard_file(payload.get("path", ""))
                update_review_decision(
                    target,
                    str(payload.get("id", "")),
                    str(payload.get("decision", "")),
                    str(payload.get("researcher", "")),
                    str(payload.get("notes", "")),
                )
                invalidate_dashboard_cache()
            except Exception as exc:
                self.send_json({"error": str(exc)}, status=400)
                return
            self.send_json({"status": "ok"})
            return
        if parsed.path == "/api/artifact-item":
            try:
                length = int(self.headers.get("Content-Length", "0"))
                payload = json.loads(self.rfile.read(length).decode("utf-8"))
                target = resolve_dashboard_file(payload.get("path", ""))
                update_artifact_item(target, str(payload.get("id", "")), str(payload.get("block", "")))
                invalidate_dashboard_cache()
            except Exception as exc:
                self.send_json({"error": str(exc)}, status=400)
                return
            self.send_json({"status": "ok"})
            return
        if parsed.path == "/api/deliverable-review-note":
            try:
                length = int(self.headers.get("Content-Length", "0"))
                payload = json.loads(self.rfile.read(length).decode("utf-8"))
                target = resolve_dashboard_file(payload.get("path", ""))
                update_deliverable_review(
                    target,
                    str(payload.get("section_id", "")),
                    str(payload.get("status", "")),
                    str(payload.get("notes", "")),
                )
                invalidate_dashboard_cache()
            except Exception as exc:
                self.send_json({"error": str(exc)}, status=400)
                return
            self.send_json({"status": "ok"})
            return
        self.send_error(404)


class ThreadedDashboardServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True


def dashboard(args: argparse.Namespace) -> None:
    with ThreadedDashboardServer((args.host, args.port), DashboardHandler) as server:
        url = f"http://{args.host}:{args.port}/"
        print(f"Research OS dashboard running at {url}")
        print("Press Ctrl-C to stop.")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nDashboard stopped.")


def request_deliverable(args: argparse.Namespace) -> None:
    if args.type not in SUPPORTED_DELIVERABLES:
        raise SystemExit(f"Unsupported deliverable type: {args.type}")
    round_dir = assert_round(Path(args.round_dir))
    pipeline = round_file(round_dir, "pipeline")
    text = read_text(pipeline)
    block = f"""deliverables:
  requested:
    - type: {args.type}
      status: requested
      audience: {args.audience}
      scope: {args.scope}
"""
    text = re.sub(r"deliverables:\n  requested: \[\]\n?", block, text)
    if text == read_text(pipeline) and f"type: {args.type}" not in text:
        append_section(pipeline, block)
    write_text(pipeline, text)
    print(f"Requested deliverable: {args.type}")


def requested_deliverables(round_dir: Path) -> list[dict[str, str]]:
    text = read_text(round_file(round_dir, "pipeline"))
    requests = []
    current: dict[str, str] | None = None
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- type:"):
            if current:
                requests.append(current)
            current = {"type": stripped.split(":", 1)[1].strip()}
        elif current and ":" in stripped:
            key, value = stripped.split(":", 1)
            current[key.strip()] = value.strip()
    if current:
        requests.append(current)
    return [item for item in requests if item.get("status") == "requested"]


def deliverable_type_guidance(kind: str) -> str:
    if kind == "research-summary":
        return (
            "Format this as a reviewable research summary. Include the main story, key findings, implications, recommended next steps, "
            "and visible uncertainty or open questions. Keep sections concise enough to review in the web UI, and make every claim traceable to accepted Evidence, Patterns, Insights or Recommendations."
        )
    if kind == "design-actions-summary":
        return (
            "Format this as a Design brief, not a generic design actions summary. "
            "Make it practical for product/design: include what should change and how to start designing it. "
            "Use bold lead phrases in What we learned, priority actions and open questions so the document is scannable. "
            "Add bullet user stories in the format 'As a ..., I want ..., so I can ...' under the priority actions. "
            "If the source material does not support a clear how, explicitly mark that as an open decision for review."
        )
    if kind == "stakeholder-slack-message":
        return (
            "Format this as a ready-to-post Slack message for stakeholders. "
            "Keep it concise, scannable and decision-oriented. Include: a short headline, 2-4 key bullets, "
            "what changed or was learned, what still needs review/uncertainty, and a clear next step or ask. "
            "Avoid report-style sections, long evidence appendices and formal executive-summary language."
        )
    if kind == "powerpoint-preparation-prompt":
        return (
            "Format this as a reusable prompt for creating a research readout deck. Include audience, deck goal, required narrative, slide-by-slide structure, "
            "visual/layout guidance, source material to use, and quality checks. The output should be a prompt someone can copy into Codex/Cowork or a deck-building workflow."
        )
    if kind == "post-it-notes":
        return (
            "Format this as workshop-ready Figma/FigJam post-it notes, not a report. "
            "Group notes by source-derived context labels. Under each context heading, write one note per line. "
            "Each note must start with '+', '-' or '0', include the context label in brackets, and stand on its own by explaining both what happens and why it matters. "
            "Use '+' for positive insight, '-' for negative insight, and '0' for neutral insight, tension, trade-off or condition. "
            "Do not include participant names, source IDs or evidence IDs in the note text. "
            "Do not smooth over contradictions; split positive and negative signals when both matter and optionally add a neutral tension note."
        )
    return "Use the requested deliverable format and keep the output traceable to the source knowledge."


def generate_deliverables(args: argparse.Namespace) -> None:
    round_dir = assert_round(Path(args.round_dir))
    requests = requested_deliverables(round_dir)
    if not requests:
        print("No requested Deliverables found. Nothing generated.")
        return
    for item in requests:
        kind = item["type"]
        output = round_path(round_dir, "deliverables") / f"{kind}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
        project_dir = round_dir.parents[1]
        context = load_context(
            round_dir,
            [
                project_file(project_dir, "context"),
                round_file(round_dir, "overview"),
                round_file(round_dir, "questions"),
                round_path(round_dir, "evidence") / "evidence.md",
                round_path(round_dir, "method") / "method-assessments.md",
                round_path(round_dir, "patterns") / "patterns.md",
                round_path(round_dir, "insights") / "insights.md",
                round_path(round_dir, "reviews") / "review-queue.md",
            ],
        )
        instructions = read_text(AGENTS_DIR / "deliverable-generator-agent.md")
        type_guidance = deliverable_type_guidance(kind)
        prompt = "\n\n".join(
            [
                f"Draft this reviewable Research OS Markdown deliverable in Codex/Cowork, not through the backend: {kind}.",
                f"Write the reviewable Markdown source to: {rel(output)}",
                f"Audience: {item.get('audience', 'unspecified')}",
                f"Scope: {item.get('scope', 'unspecified')}",
                type_guidance,
                f"First read {rel(LOOPED_ACTIVE_FILE)} and apply any active Looped Learnings.",
                research_lens_prompt_block(round_dir, include_content=True),
                "Do not call OpenAI APIs.",
                "Do not run local stub generation.",
                "Use accepted knowledge where available. If using proposed material, clearly label it as proposed.",
                "Do not create new Evidence, Patterns or Insights.",
                "Do not export PDF, PPT, Slack-ready final copy or any other final artefact in this pass. Export/finalize only after the Markdown source is reviewed and approved.",
                *[f"\n--- {name} ---\n{content}" for name, content in sorted(context.items())],
            ]
        )
        handoff = round_path(round_dir, "pipeline_runs") / f"deliverable-handoff-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
        write_text(
            handoff,
            "\n".join(
                [
                    f"# Deliverable Handoff: {kind}",
                    "",
                    "- Status: codex-required",
                    "- Mode: Codex/Cowork handoff",
                    f"- Intended output: {rel(output)}",
                    "",
                    "## Codex Prompt",
                    "```text",
                    prompt.strip(),
                    "```",
                ]
            )
            + "\n",
        )
        print("Backend deliverable generation is disabled. Use this Codex/Cowork prompt instead:")
        print()
        print(prompt.strip())
        print()
        print(f"Handoff logged: {rel(handoff)}")


def round_create(args: argparse.Namespace) -> None:
    project_id = slug(args.project)
    round_date = normalize_date(args.date)
    round_slug = slug(args.name)
    round_id = f"{round_date}-{round_slug}"
    project_dir = projects_dir() / project_id
    rounds_dir = project_path(project_dir, "rounds")
    round_dir = rounds_dir / round_id
    if round_dir.exists() and not args.force:
        raise SystemExit(f"Round already exists: {rel(round_dir)}. Use --force to fill missing files.")

    if not project_dir.exists():
        raise SystemExit(
            f"Project does not exist: {project_id}. "
            f"Create it first with: ./research-os project create --name \"{title_from_slug(project_id)}\""
        )

    create_round_files(round_dir, project_id, round_id, args.name, round_date, args.method)
    print(f"Created round: {rel(round_dir)}")
    print(f"Add sources to: {rel(round_path(round_dir, 'sources'))}")
    print("Process sources from the Research OS dashboard prompt in Codex/Cowork.")


def project_create(args: argparse.Namespace) -> None:
    project_id = slug(args.name)
    project_dir = projects_dir() / project_id
    create_project_files(project_dir, args.name, force=args.force)
    print(f"Created project: {rel(project_dir)}")
    print(f"Add project-level context sources to: {rel(project_path(project_dir, 'sources'))}")
    print(f"Create first round: ./research-os round create --project {project_id} --date 2026-07-29 --name \"Concept Test 01\"")


def project_process_input(args: argparse.Namespace) -> None:
    project_dir = assert_project(Path(args.project_dir))
    ensure_project_input_scaffold(project_dir)
    sources = changed_project_sources(project_dir, args.force)
    run_id = "run-" + datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = project_path(project_dir, "pipeline_runs") / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    if not sources:
        warning = "No new or changed project Sources detected. Use --force to reprocess unchanged Sources."
        write_text(run_dir / "run.md", f"# Project Input Run {run_id}\n\n- Status: no-op\n- Warning: {warning}\n")
        print(warning)
        return

    state = load_project_state(project_dir)
    started = now()
    state["runs"].append({"id": run_id, "created_at": started.isoformat(), "status": "codex-required"})
    save_project_state(project_dir, state)

    prompt = project_codex_processing_prompt(project_dir, sources)
    summary = [
        f"# Project Input Run {run_id}",
        "",
        "- Status: codex-required",
        "- Mode: Codex/Cowork handoff",
        f"- Sources waiting for Codex processing: {len(sources)}",
        f"- Started: {started.isoformat()}",
        f"- Completed: {now().isoformat()}",
        "",
        "## Sources",
        *[f"- {source['id']}: {rel(source['path'])}" for source in sources],
        "",
        "## Codex Prompt",
        "```text",
        prompt.strip(),
        "```",
    ]
    write_text(run_dir / "run.md", "\n".join(summary) + "\n")
    print("Backend project input processing is disabled. Use this Codex/Cowork prompt instead:")
    print()
    print(prompt.strip())
    print()
    print(f"Handoff logged: {rel(run_dir)}")


def project_status(args: argparse.Namespace) -> None:
    project_dir = assert_project(Path(args.project_dir))
    ensure_project_input_scaffold(project_dir)
    state = load_project_state(project_dir)
    pending = changed_project_sources(project_dir, False)
    print(f"Project: {rel(project_dir)}")
    print(f"Processed project sources: {len(state.get('sources', {}))}")
    print(f"New or changed project sources: {len(pending)}")
    if state.get("runs"):
        latest = state["runs"][-1]
        print(f"Latest project input run: {latest['id']} ({latest['status']})")
    else:
        print("Latest project input run: none")


def print_commands(args: argparse.Namespace) -> None:
    round_dir = args.round_dir or "../Projects/new-product-area/02-rounds/2026-07-23-concept-test-01"
    commands = f"""Research OS command menu

Clickable `.command` shortcuts are parked in:
  Command Shortcuts/

Terminal commands:
  Make a new project:
  ./research-os project create --name "New Product Area"

  Process project-level context input:
  Use the Research OS dashboard prompt. The CLI only logs a Codex handoff prompt.

  Make a new round:
  ./research-os round create --project new-product-area --date 2026-07-23 --name "Concept Test 01"

  Process new transcript or source input:
  Use the Research OS dashboard prompt. The CLI only logs a Codex handoff prompt.

  Request and generate deliverables:
  ./research-os deliverable request {round_dir} --type research-summary
  ./research-os deliverable request {round_dir} --type stakeholder-slack-message --audience stakeholders
  ./research-os deliverable generate {round_dir}
"""
    print(commands)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="research-os")
    sub = parser.add_subparsers(dest="area", required=True)

    commands = sub.add_parser("commands")
    commands.add_argument("--round-dir")
    commands.set_defaults(func=print_commands)

    dashboard_parser = sub.add_parser("dashboard")
    dashboard_parser.add_argument("--host", default="127.0.0.1")
    dashboard_parser.add_argument("--port", type=int, default=8765)
    dashboard_parser.set_defaults(func=dashboard)

    project = sub.add_parser("project")
    project_sub = project.add_subparsers(dest="command", required=True)
    project_create_parser = project_sub.add_parser("create")
    project_create_parser.add_argument("--name", required=True)
    project_create_parser.add_argument("--force", action="store_true")
    project_create_parser.set_defaults(func=project_create)
    project_process = project_sub.add_parser("process-input")
    project_process.add_argument("project_dir")
    project_process.add_argument("--force", action="store_true")
    project_process.set_defaults(func=project_process_input)
    project_status_parser = project_sub.add_parser("status")
    project_status_parser.add_argument("project_dir")
    project_status_parser.set_defaults(func=project_status)

    round_parser = sub.add_parser("round")
    round_sub = round_parser.add_subparsers(dest="command", required=True)
    create = round_sub.add_parser("create")
    create.add_argument("--project", required=True)
    create.add_argument("--date", required=True)
    create.add_argument("--name", required=True)
    create.add_argument("--method", default="To be added.")
    create.add_argument("--force", action="store_true")
    create.set_defaults(func=round_create)

    pipeline = sub.add_parser("pipeline")
    pipeline_sub = pipeline.add_subparsers(dest="command", required=True)
    run = pipeline_sub.add_parser("run")
    run.add_argument("round_dir")
    run.add_argument("--force", action="store_true")
    run.set_defaults(func=pipeline_run)
    status = pipeline_sub.add_parser("status")
    status.add_argument("round_dir")
    status.set_defaults(func=pipeline_status)
    review = pipeline_sub.add_parser("review")
    review.add_argument("round_dir")
    review.set_defaults(func=pipeline_review)
    apply = pipeline_sub.add_parser("apply-reviews")
    apply.add_argument("round_dir")
    apply.set_defaults(func=apply_reviews)

    deliverable = sub.add_parser("deliverable")
    deliverable_sub = deliverable.add_subparsers(dest="command", required=True)
    request = deliverable_sub.add_parser("request")
    request.add_argument("round_dir")
    request.add_argument("--type", required=True)
    request.add_argument("--audience", default="product-team")
    request.add_argument("--scope", default="current-round")
    request.set_defaults(func=request_deliverable)
    generate = deliverable_sub.add_parser("generate")
    generate.add_argument("round_dir")
    generate.set_defaults(func=generate_deliverables)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
