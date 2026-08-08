# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

Feature: Git auto-commit on journal writes

    Scenario Outline: Writing an entry creates a git commit with per-journal git key
        Given git author info is configured
        And we use the config "<config_file>"
        When we run "jrnl 23 july 2013: A cold and stormy day."
        Then we should get no error
        And the journal should have 1 git commit

        Examples: Journal types
        | config_file              |
        | git_file_journal.yaml    |
        | git_folder_journal.yaml  |

    Scenario Outline: Writing an entry creates a git commit with global backup_all_jrnls_with_git key
        Given git author info is configured
        And we use the config "<config_file>"
        When we run "jrnl 23 july 2013: A cold and stormy day."
        Then we should get no error
        And the journal should have 1 git commit

        Examples: Journal types
        | config_file                    |
        | git_global_file_journal.yaml   |
        | git_global_folder_journal.yaml |

    Scenario Outline: Writing an entry pushes to remote when auto_push_to_git_remote_after_edit is enabled
        Given git author info is configured
        And we use the config "<config_file>"
        And a local git remote is configured for the journal
        When we run "jrnl 23 july 2013: A cold and stormy day."
        Then we should get no error
        And the git remote should have 1 git commit

        Examples: Journal types
        | config_file                  |
        | git_push_file_journal.yaml   |
        | git_push_folder_journal.yaml |

    Scenario Outline: Writing an entry pulls from remote when auto_pull_from_git_remote_before_edit is enabled
        Given git author info is configured
        And we use the config "<config_file>"
        And a local git remote is configured for the journal
        When we run "jrnl 23 july 2013: seed entry."
        Then we should get no error
        Given the git remote has a new commit
        When we run "jrnl 24 july 2013: A cold and stormy day."
        Then we should get no error
        And the journal should have 3 git commits

        Examples: Journal types
        | config_file                  |
        | git_pull_file_journal.yaml   |
        | git_pull_folder_journal.yaml |

    Scenario Outline: No git commit is made when git is not enabled
        Given we use the config "<config_file>"
        When we run "jrnl 23 july 2013: A cold and stormy day."
        Then we should get no error
        And the journal directory should have no git repo

        Examples: Journal types
        | config_file       |
        | simple.yaml       |
        | basic_folder.yaml |
