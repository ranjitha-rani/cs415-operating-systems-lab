#!/usr/bin/env python3
"""Stage all changes, commit with message 'changes', and push to GitHub."""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent


def run_git(args: list[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        **kwargs,
    )


def main() -> int:
    status = run_git(["status", "--porcelain"], capture_output=True, text=True)
    if status.returncode != 0:
        print("error: `git status` failed — is this a git repo?", file=sys.stderr)
        return 1

    dirty = bool(status.stdout.strip())

    if dirty:
        add = run_git(["add", "-A"])
        if add.returncode != 0:
            return add.returncode

        commit = run_git(["commit", "-m", "changes"])
        if commit.returncode != 0:
            print("error: `git commit` failed.", file=sys.stderr)
            return commit.returncode
    else:
        print("No file changes to commit.")

    push = run_git(["push"])
    if push.returncode != 0:
        print("error: `git push` failed.", file=sys.stderr)
        return push.returncode

    print("Done: pushed to remote.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
