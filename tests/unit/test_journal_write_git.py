# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import sys
from pathlib import Path
from unittest.mock import patch

from jrnl.journals.FolderJournal import Folder
from jrnl.journals.Journal import Journal

# jrnl/journals/__init__.py re-exports the Journal *class* as
# ``jrnl.journals.Journal``, which shadows the *module* of the same
# name.  ``unittest.mock.patch`` resolves dotted paths via attribute
# lookup, so ``patch("jrnl.journals.Journal.git_pull")`` finds the
# class, not the module.  Grab explicit module references to avoid the
# ambiguity.
_journal_mod = sys.modules["jrnl.journals.Journal"]
_folder_mod = sys.modules["jrnl.journals.FolderJournal"]


class TestJournalOpenGitPull:
    def test_pulls_when_auto_pull_enabled(self, tmp_path: Path):
        journal_file = tmp_path / "journal.txt"
        journal_file.write_text("")
        journal = Journal(
            journal=str(journal_file),
            git=True,
            auto_pull_from_git_remote_before_edit=True,
            encrypt=False,
        )

        with patch.object(_journal_mod, "git_pull") as mock_pull:
            journal.open()

        mock_pull.assert_called_once_with(Path(str(journal_file)))

    def test_skips_pull_when_auto_pull_disabled(self, tmp_path: Path):
        journal_file = tmp_path / "journal.txt"
        journal_file.write_text("")
        journal = Journal(
            journal=str(journal_file),
            git=True,
            auto_pull_from_git_remote_before_edit=False,
            encrypt=False,
        )

        with patch.object(_journal_mod, "git_pull") as mock_pull:
            journal.open()

        mock_pull.assert_not_called()

    def test_skips_pull_when_key_absent(self, tmp_path: Path):
        journal_file = tmp_path / "journal.txt"
        journal_file.write_text("")
        journal = Journal(journal=str(journal_file), git=True, encrypt=False)

        with patch.object(_journal_mod, "git_pull") as mock_pull:
            journal.open()

        mock_pull.assert_not_called()


class TestFolderJournalOpenGitPull:
    def test_pulls_when_auto_pull_enabled(self, tmp_path: Path):
        journal = Folder(
            journal=str(tmp_path),
            git=True,
            auto_pull_from_git_remote_before_edit=True,
        )

        with patch.object(_folder_mod, "git_pull") as mock_pull:
            journal.open()

        mock_pull.assert_called_once_with(Path(str(tmp_path)))

    def test_skips_pull_when_auto_pull_disabled(self, tmp_path: Path):
        journal = Folder(
            journal=str(tmp_path),
            git=True,
            auto_pull_from_git_remote_before_edit=False,
        )

        with patch.object(_folder_mod, "git_pull") as mock_pull:
            journal.open()

        mock_pull.assert_not_called()

    def test_skips_pull_when_key_absent(self, tmp_path: Path):
        journal = Folder(journal=str(tmp_path), git=True)

        with patch.object(_folder_mod, "git_pull") as mock_pull:
            journal.open()

        mock_pull.assert_not_called()


class TestJournalWriteGit:
    def test_journal_git_false_overrides_global_git_enabled(self, tmp_path: Path):
        journal_file = tmp_path / "journal.txt"
        journal = Journal(
            journal=str(journal_file),
            backup_all_jrnls_with_git=True,
            git=False,
            encrypt=False,
        )
        journal.new_entry("test entry")

        with patch.object(_journal_mod, "git_auto_commit") as mock_commit:
            journal.write()

        mock_commit.assert_not_called()

    def test_skips_git_commit_when_disabled(self, tmp_path: Path):
        journal_file = tmp_path / "journal.txt"
        journal = Journal(journal=str(journal_file), git=False, encrypt=False)
        journal.new_entry("test entry")

        with patch.object(_journal_mod, "git_auto_commit") as mock_commit:
            journal.write()

        mock_commit.assert_not_called()

    def test_skips_git_commit_when_key_absent(self, tmp_path: Path):
        journal_file = tmp_path / "journal.txt"
        journal = Journal(journal=str(journal_file), encrypt=False)
        journal.new_entry("test entry")

        with patch.object(_journal_mod, "git_auto_commit") as mock_commit:
            journal.write()

        mock_commit.assert_not_called()


class TestFolderJournalWriteGit:
    def test_journal_git_false_overrides_global_git_enabled(self, tmp_path: Path):
        journal = Folder(
            journal=str(tmp_path),
            backup_all_jrnls_with_git=True,
            git=False,
        )
        journal.new_entry("test entry")

        with patch.object(_folder_mod, "git_auto_commit") as mock_commit:
            journal.write()

        mock_commit.assert_not_called()

    def test_skips_git_commit_when_disabled(self, tmp_path: Path):
        journal = Folder(journal=str(tmp_path), git=False)
        journal.new_entry("test entry")

        with patch.object(_folder_mod, "git_auto_commit") as mock_commit:
            journal.write()

        mock_commit.assert_not_called()

    def test_skips_git_commit_when_key_absent(self, tmp_path: Path):
        journal = Folder(journal=str(tmp_path))
        journal.new_entry("test entry")

        with patch.object(_folder_mod, "git_auto_commit") as mock_commit:
            journal.write()

        mock_commit.assert_not_called()
