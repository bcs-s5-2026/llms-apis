#!/usr/bin/env python3
"""
Hook: log-prompt-history.sh
Event: UserPromptSubmit
Purpose: Append the user prompt to prompts_history.md and JOURNAL.md,
then commit the files to the local git repository.

This file intentionally keeps the original .sh name for existing hook references,
but it is implemented in Python for cross-platform compatibility.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Internal version (increment on each edit): X.YZ
VERSION = "1.02"

# Toggle local transcript copy (original filename is preserved).
ENABLE_LOCAL_TRANSCRIPT_COPY = False

# Destination folder under repo root when transcript copy is enabled.
LOCAL_TRANSCRIPT_COPY_DIR = Path("tmp") / "transcripts"


def get_repo_root(script_dir: Path) -> Path:
  try:
    output = subprocess.check_output(
      ["git", "-C", str(script_dir), "rev-parse", "--show-toplevel"],
      stderr=subprocess.DEVNULL,
      text=True,
    ).strip()
    if output:
      return Path(output)
  except Exception:
    pass
  return Path.cwd()


def parse_payload(stdin_text: str) -> dict:
  try:
    payload = json.loads(stdin_text)
    if isinstance(payload, dict):
      return payload
  except Exception:
    pass
  return {}


def get_user_identity(repo_root: Path) -> str:
  for key in ["user.email", "user.name"]:
    try:
      value = subprocess.check_output(
        ["git", "-C", str(repo_root), "config", key],
        stderr=subprocess.DEVNULL,
        text=True,
      ).strip()
      if value:
        return value
    except Exception:
      pass

  return "default_user"


def sanitize_prompt(prompt: str) -> str:
  return " ".join(prompt.splitlines()).strip() or "unknown"


def ensure_history_file(history_file: Path) -> None:
  if history_file.exists():
    return

  history_file.write_text(
    "# Prompts History\n\n"
    "Automatically captured prompt log. Entries are appended in chronological order (oldest first).\n\n",
    encoding="utf-8",
  )


def append_entry(history_file: Path, entry: str) -> None:
  with history_file.open("a", encoding="utf-8") as handle:
    handle.write(entry)


def ensure_journal_file(journal_file: Path) -> None:
  if journal_file.exists():
    return

  journal_file.write_text(
    "# This Journal gets updated automatically by the Journal Logger Agent\n",
    encoding="utf-8",
  )


def maybe_copy_transcript(transcript_path: Path, repo_root: Path) -> None:
  if not ENABLE_LOCAL_TRANSCRIPT_COPY:
    return

  if not transcript_path.is_file():
    return

  destination_dir = repo_root / LOCAL_TRANSCRIPT_COPY_DIR
  destination_dir.mkdir(parents=True, exist_ok=True)
  destination_path = destination_dir / transcript_path.name
  shutil.copy2(transcript_path, destination_path)


def safe_git_commit(repo_root: Path, files_to_add: list[Path], timestamp: str) -> None:
  try:
    for file_path in files_to_add:
      subprocess.run(
        ["git", "-C", str(repo_root), "add", str(file_path)],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
      )
    subprocess.run(
      [
        "git",
        "-C",
        str(repo_root),
        "commit",
        "-m",
        f"chore: log prompt [{timestamp}]",
        "--no-verify",
        "-q",
      ],
      check=False,
      stdout=subprocess.DEVNULL,
      stderr=subprocess.DEVNULL,
    )
  except Exception:
    pass


def main() -> int:
  try:
    script_dir = Path(__file__).resolve().parent
    repo_root = get_repo_root(script_dir)
    history_file = repo_root / "prompts_history.md"
    journal_file = repo_root / "JOURNAL.md"

    stdin_text = sys.stdin.read()
    payload = parse_payload(stdin_text)

    prompt = sanitize_prompt(str(payload.get("prompt", "unknown")))
    transcript_path_raw = str(payload.get("transcript_path", "")).strip()
    transcript_path = Path(transcript_path_raw) if transcript_path_raw else Path()

    timestamp_history = datetime.now().strftime("%d-%m-%Y %H:%M")
    timestamp_journal = datetime.now().strftime("%d-%m-%Y %H:%M")
    user_identity = get_user_identity(repo_root)

    maybe_copy_transcript(transcript_path, repo_root)
    ensure_history_file(history_file)
    ensure_journal_file(journal_file)

    history_entry = (
      f"### {timestamp_history}\n"
      f"- **Prompt**: {prompt}\n\n"
    )

    journal_entry = (
      "\n### **New Interaction**\n"
      f"- **Hook Version**: {VERSION}\n"
      f"- **Date**: {timestamp_journal}\n"
      # f"- **User**: {user_identity}\n"
      f"- **Prompt**: {prompt}\n"
    )

    append_entry(history_file, history_entry)
    append_entry(journal_file, journal_entry)
    safe_git_commit(repo_root, [history_file, journal_file], timestamp_history)
  except Exception:
    # Non-blocking hook by design.
    return 0

  return 0


if __name__ == "__main__":
  sys.exit(main())
