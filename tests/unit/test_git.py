# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import logging
from pathlib import Path
from unittest.mock import MagicMock
from unittest.mock import patch

import git
import pytest

from jrnl.exception import JrnlException
from jrnl.git import git_auto_commit
from jrnl.git import git_pull


@pytest.fixture()
def git_author_env(monkeypatch):
    """Ensure git has author/committer info so commits succeed in any environment."""
    monkeypatch.setenv("GIT_AUTHOR_NAME", "Test")
    monkeypatch.setenv("GIT_AUTHOR_EMAIL", "test@test.com")
    monkeypatch.setenv("GIT_COMMITTER_NAME", "Test")
    monkeypatch.setenv("GIT_COMMITTER_EMAIL", "test@test.com")


class TestGitCommitFileJournal:
    def test_initializes_repo_and_commits(self, tmp_path: Path, git_author_env):
        journal_file = tmp_path / "journal.txt"
        journal_file.write_text("first entry")

        git_auto_commit(journal_file)

        repo = git.Repo(tmp_path)
        commits = list(repo.iter_commits())
        assert len(commits) == 1
        assert commits[0].message == "jrnl CLI: auto-commit"

    def test_commits_subsequent_changes(self, tmp_path: Path, git_author_env):
        journal_file = tmp_path / "journal.txt"
        journal_file.write_text("first entry")
        git_auto_commit(journal_file)

        journal_file.write_text("second entry")
        git_auto_commit(journal_file)

        repo = git.Repo(tmp_path)
        assert len(list(repo.iter_commits())) == 2

    def test_skips_commit_when_no_changes(self, tmp_path: Path, git_author_env):
        journal_file = tmp_path / "journal.txt"
        journal_file.write_text("unchanged")
        git_auto_commit(journal_file)
        git_auto_commit(journal_file)  # second call with same content

        repo = git.Repo(tmp_path)
        assert len(list(repo.iter_commits())) == 1

    def test_uses_existing_repo(self, tmp_path: Path, git_author_env):
        """Preserves existing commit history instead of reinitializing the repo."""
        # Set up a pre-existing repo with one commit made outside of git_auto_commit
        repo = git.Repo.init(tmp_path)
        existing_file = tmp_path / "existing.txt"
        existing_file.write_text("pre-existing content")
        repo.git.add(str(existing_file))
        repo.index.commit("pre-existing commit")

        journal_file = tmp_path / "journal.txt"
        journal_file.write_text("journal entry")
        git_auto_commit(journal_file)

        repo = git.Repo(tmp_path)
        assert len(list(repo.iter_commits())) == 2


class TestGitCommitFolderJournal:
    def test_initializes_repo_and_commits_directory(
        self, tmp_path: Path, git_author_env
    ):
        journal_dir = tmp_path / "journal"
        journal_dir.mkdir()
        (journal_dir / "entry.txt").write_text("entry")

        git_auto_commit(journal_dir)

        repo = git.Repo(journal_dir)
        assert len(list(repo.iter_commits())) == 1


class TestGitPush:
    def test_push_skipped_when_push_false(self, tmp_path: Path, git_author_env):
        journal_file = tmp_path / "journal.txt"
        journal_file.write_text("entry")

        with patch("jrnl.git._push_to_remote") as mock_push:
            git_auto_commit(journal_file, push=False)

        mock_push.assert_not_called()

    def test_push_called_after_commit_when_push_true(
        self, tmp_path: Path, git_author_env
    ):
        journal_file = tmp_path / "journal.txt"
        journal_file.write_text("entry")

        with patch("jrnl.git._push_to_remote") as mock_push:
            git_auto_commit(journal_file, push=True)

        mock_push.assert_called_once()

    def test_push_not_called_when_no_changes(self, tmp_path: Path, git_author_env):
        journal_file = tmp_path / "journal.txt"
        journal_file.write_text("entry")
        git_auto_commit(journal_file)  # first commit

        with patch("jrnl.git._push_to_remote") as mock_push:
            git_auto_commit(journal_file, push=True)  # no changes

        mock_push.assert_not_called()

    def test_push_skipped_when_no_remote(self, tmp_path: Path, git_author_env, caplog):
        journal_file = tmp_path / "journal.txt"
        journal_file.write_text("entry")
        git_auto_commit(journal_file)  # set up repo with a commit

        repo = git.Repo(tmp_path)
        with caplog.at_level(logging.DEBUG):
            from jrnl.git import _push_to_remote

            _push_to_remote(repo)

        assert "no remotes configured" in caplog.text

    def test_push_warns_on_failure(self, caplog):
        mock_remote = MagicMock()
        mock_remote.push.side_effect = git.exc.GitCommandError("push", 128)
        mock_repo = MagicMock()
        mock_repo.remotes = [mock_remote]

        with caplog.at_level(logging.WARNING):
            from jrnl.git import _push_to_remote

            _push_to_remote(mock_repo)

        assert "git push failed" in caplog.text


class TestGitPull:
    def test_pull_skipped_when_no_repo(self, tmp_path: Path):
        journal_file = tmp_path / "journal.txt"
        journal_file.write_text("entry")

        # Should not raise — just returns silently
        git_pull(journal_file)

    def test_pull_skipped_when_no_remote(self, tmp_path: Path, git_author_env, caplog):
        journal_file = tmp_path / "journal.txt"
        journal_file.write_text("entry")
        git_auto_commit(journal_file)

        with caplog.at_level(logging.DEBUG):
            git_pull(journal_file)

        assert "no remotes configured" in caplog.text

    def test_pull_fetches_remote(self, tmp_path: Path, git_author_env):
        journal_file = tmp_path / "journal.txt"
        journal_file.write_text("entry")
        git_auto_commit(journal_file)

        mock_ref = MagicMock()
        mock_ref.name = "origin/master"
        mock_remote = MagicMock()
        mock_remote.name = "origin"
        mock_remote.refs = [mock_ref]
        mock_remote.url = "https://example.com/repo.git"

        mock_repo = MagicMock(spec=git.Repo)
        mock_repo.remotes = [mock_remote]
        mock_repo.active_branch.name = "master"
        # Same commit = already up to date
        mock_commit = MagicMock()
        mock_repo.head.is_valid.return_value = True
        mock_repo.head.commit = mock_commit
        mock_repo.commit.return_value = mock_commit

        with patch("jrnl.git.git.Repo", return_value=mock_repo):
            git_pull(journal_file)

        mock_remote.fetch.assert_called_once()

    def test_pull_fast_forwards_when_behind(self, tmp_path: Path, git_author_env):
        journal_file = tmp_path / "journal.txt"
        journal_file.write_text("entry")
        git_auto_commit(journal_file)

        mock_ref = MagicMock()
        mock_ref.name = "origin/master"
        mock_remote = MagicMock()
        mock_remote.name = "origin"
        mock_remote.refs = [mock_ref]
        mock_remote.url = "https://example.com/repo.git"

        local_commit = MagicMock()
        remote_commit = MagicMock()

        mock_repo = MagicMock(spec=git.Repo)
        mock_repo.remotes = [mock_remote]
        mock_repo.active_branch.name = "master"
        mock_repo.head.is_valid.return_value = True
        mock_repo.head.commit = local_commit
        mock_repo.commit.return_value = remote_commit
        mock_repo.is_ancestor.return_value = True

        with patch("jrnl.git.git.Repo", return_value=mock_repo):
            git_pull(journal_file)

        mock_repo.head.reset.assert_called_once_with(
            remote_commit, index=True, working_tree=True
        )

    def test_pull_raises_when_diverged(self, tmp_path: Path, git_author_env):
        journal_file = tmp_path / "journal.txt"
        journal_file.write_text("entry")
        git_auto_commit(journal_file)

        mock_ref = MagicMock()
        mock_ref.name = "origin/master"
        mock_remote = MagicMock()
        mock_remote.name = "origin"
        mock_remote.refs = [mock_ref]
        mock_remote.url = "https://example.com/repo.git"

        local_commit = MagicMock()
        remote_commit = MagicMock()

        mock_repo = MagicMock(spec=git.Repo)
        mock_repo.remotes = [mock_remote]
        mock_repo.active_branch.name = "master"
        mock_repo.head.is_valid.return_value = True
        mock_repo.head.commit = local_commit
        mock_repo.commit.return_value = remote_commit
        mock_repo.is_ancestor.return_value = False

        with patch("jrnl.git.git.Repo", return_value=mock_repo):
            with pytest.raises(JrnlException):
                git_pull(journal_file)

    def test_pull_raises_on_fetch_error(self, tmp_path: Path, git_author_env):
        journal_file = tmp_path / "journal.txt"
        journal_file.write_text("entry")
        git_auto_commit(journal_file)

        mock_remote = MagicMock()
        mock_remote.fetch.side_effect = git.exc.GitCommandError("fetch", 128)
        mock_repo = MagicMock(spec=git.Repo)
        mock_repo.remotes = [mock_remote]
        mock_repo.head.is_valid.return_value = True

        with patch("jrnl.git.git.Repo", return_value=mock_repo):
            with pytest.raises(JrnlException):
                git_pull(journal_file)

    def test_pull_skipped_when_path_does_not_exist(self, tmp_path: Path):
        nonexistent = tmp_path / "nope" / "journal.txt"

        # Should not raise
        git_pull(nonexistent)

    def test_pull_handles_directory_path(self, tmp_path: Path, git_author_env, caplog):
        journal_dir = tmp_path / "journal"
        journal_dir.mkdir()
        (journal_dir / "entry.txt").write_text("entry")
        git_auto_commit(journal_dir)

        with caplog.at_level(logging.DEBUG):
            git_pull(journal_dir)

        assert "no remotes configured" in caplog.text


class TestGitCommitErrorHandling:
    def test_warns_when_git_not_installed(self, tmp_path: Path, caplog):
        journal_file = tmp_path / "journal.txt"
        journal_file.write_text("entry")

        with patch("git.Repo", side_effect=git.exc.GitCommandNotFound("git", 2)):
            with caplog.at_level(logging.WARNING):
                git_auto_commit(journal_file)  # must not raise

        assert "git not found" in caplog.text

    def test_warns_on_git_command_error(self, tmp_path: Path, caplog):
        journal_file = tmp_path / "journal.txt"
        journal_file.write_text("entry")

        with patch("git.Repo", side_effect=git.exc.GitCommandError("add", 128)):
            with caplog.at_level(logging.WARNING):
                git_auto_commit(journal_file)  # must not raise

        assert "git auto-commit failed" in caplog.text
