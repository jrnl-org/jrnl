# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import logging
from pathlib import Path

import git

from jrnl.messages import Message
from jrnl.messages import MsgStyle
from jrnl.messages import MsgText
from jrnl.output import print_msg


def git_auto_commit(
    path: Path, message: str = "jrnl CLI: auto-commit", push: bool = False
) -> None:
    """Initialize a git repo if needed, then stage and commit journal changes."""
    path = path.resolve()
    repo_dir = path.parent if path.is_file() else path

    try:
        try:
            repo = git.Repo(repo_dir)
        except git.exc.InvalidGitRepositoryError:
            repo = git.Repo.init(repo_dir)

        # Always add only the journal path — never stage unrelated files that
        # may exist in the same repo. -A ensures deletions are staged too;
        # plain `git add <dir>` stages additions and modifications but skips
        # removals (relevant for folder journals, which delete empty day files).
        # For single files, -A is equivalent to plain git add.
        repo.git.add("-A", path)

        # Check for staged changes; handle new repo (no HEAD) separately
        if repo.head.is_valid():
            has_staged = bool(repo.index.diff("HEAD"))
        else:
            has_staged = bool(repo.index.entries)

        if has_staged:
            repo.index.commit(message)
            logging.debug("git: committed changes in %s", repo_dir)
            print_msg(Message(MsgText.GitCommitted, MsgStyle.NORMAL, {"path": repo_dir}))
            if push:
                _push_to_remote(repo)
        else:
            logging.debug("git: no changes to commit in %s", repo_dir)

    except git.exc.GitCommandNotFound:
        logging.warning("git not found; skipping auto-commit")
    except git.exc.GitCommandError as e:
        logging.warning("git auto-commit failed: %s", e)


def _push_to_remote(repo: git.Repo) -> None:
    """Push to the first configured remote. Logs a warning on failure."""
    if not repo.remotes:
        logging.debug("git: no remotes configured, skipping push")
        return
    try:
        remote = repo.remotes[0]
        remote.push()
        logging.debug("git: pushed to %s", remote.name)
        print_msg(Message(MsgText.GitPushed, MsgStyle.NORMAL, {"url": remote.url}))
    except git.exc.GitCommandError as e:
        logging.warning("git push failed: %s", e)
