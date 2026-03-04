# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from pathlib import Path
from unittest.mock import patch

from jrnl.journals.FolderJournal import Folder
from jrnl.journals.Journal import Journal


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

        with patch("jrnl.journals.Journal.git_auto_commit") as mock_commit:
            journal.write()

        mock_commit.assert_not_called()

    def test_skips_git_commit_when_disabled(self, tmp_path: Path):
        journal_file = tmp_path / "journal.txt"
        journal = Journal(journal=str(journal_file), git=False, encrypt=False)
        journal.new_entry("test entry")

        with patch("jrnl.journals.Journal.git_auto_commit") as mock_commit:
            journal.write()

        mock_commit.assert_not_called()

    def test_skips_git_commit_when_key_absent(self, tmp_path: Path):
        journal_file = tmp_path / "journal.txt"
        journal = Journal(journal=str(journal_file), encrypt=False)
        journal.new_entry("test entry")

        with patch("jrnl.journals.Journal.git_auto_commit") as mock_commit:
            journal.write()

        mock_commit.assert_not_called()


class TestFolderJournalWriteGit:
    def test_journal_git_false_overrides_global_git_enabled(self, tmp_path: Path):
        journal = Folder(
            journal=str(tmp_path), backup_all_jrnls_with_git=True, git=False
        )
        journal.new_entry("test entry")

        with patch("jrnl.journals.FolderJournal.git_auto_commit") as mock_commit:
            journal.write()

        mock_commit.assert_not_called()

    def test_skips_git_commit_when_disabled(self, tmp_path: Path):
        journal = Folder(journal=str(tmp_path), git=False)
        journal.new_entry("test entry")

        with patch("jrnl.journals.FolderJournal.git_auto_commit") as mock_commit:
            journal.write()

        mock_commit.assert_not_called()

    def test_skips_git_commit_when_key_absent(self, tmp_path: Path):
        journal = Folder(journal=str(tmp_path))
        journal.new_entry("test entry")

        with patch("jrnl.journals.FolderJournal.git_auto_commit") as mock_commit:
            journal.write()

        mock_commit.assert_not_called()
