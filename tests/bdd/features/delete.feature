# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

Feature: Delete entries from journal
    Scenario Outline: Delete flag allows deletion of single entry
        Given we use the config "<config_file>"
        And we use the password "test" if prompted
        When we run "jrnl -1"
        Then the output should contain "2020-09-24 09:14 The third entry finally"
        When we run "jrnl --delete" and enter
            N
            N
            Y
        Then the error output should contain "1 entry deleted"
        When we run "jrnl -99 --short"
        Then the output should be
            2020-08-29 11:11 Entry the first.
            2020-08-31 14:32 A second entry in what I hope to be a long series.

        Examples: Configs
        | config_file          |
        | basic_onefile.yaml   |
        | basic_encrypted.yaml |
        | basic_folder.yaml    |
        # | basic_dayone.yaml  | @todo


    Scenario Outline: Backing out of interactive delete does not change journal
        Given we use the config "<config_file>"
        When we run "jrnl --delete -n 1" and enter
            N
        Then the error output should not contain "deleted"
        When we run "jrnl -99 --short"
        Then the output should be
            2020-08-29 11:11 Entry the first.
            2020-08-31 14:32 A second entry in what I hope to be a long series.
            2020-09-24 09:14 The third entry finally after weeks without writing.

        Examples: Configs
        | config_file        |
        | basic_onefile.yaml |
        | basic_folder.yaml  |
        | basic_dayone.yaml  |


    Scenario Outline: Delete flag with nonsense input deletes nothing (issue #932)
        Given we use the config "<config_file>"
        When we run "jrnl --delete asdfasdf"
        Then the error output should contain "No entries to delete"
        When we run "jrnl -99 --short"
        Then the output should be
            2020-08-29 11:11 Entry the first.
            2020-08-31 14:32 A second entry in what I hope to be a long series.
            2020-09-24 09:14 The third entry finally after weeks without writing.

        Examples: Configs
        | config_file        |
        | basic_onefile.yaml |
        | basic_folder.yaml  |
        | basic_dayone.yaml  |


    Scenario Outline: Delete flag with tag only deletes tagged entries
        Given we use the config "<config_file>"
        When we run "jrnl --delete @ipsum" and enter
            Y
        Then the error output should contain "1 entry deleted"
        When we run "jrnl -99 --short"
        Then the output should be
            2020-08-31 14:32 A second entry in what I hope to be a long series.
            2020-09-24 09:14 The third entry finally after weeks without writing.

        Examples: Configs
        | config_file        |
        | basic_onefile.yaml |
        | basic_folder.yaml  |
        # | basic_dayone.yaml  | @todo


    Scenario Outline: Delete flag with multiple tags deletes all entries matching any of the tags
        Given we use the config "<config_file>"
        When we run "jrnl --delete @ipsum @tagthree" and enter
            Y
            Y
        Then the error output should contain "2 entries deleted"
        When we run "jrnl -99 --short"
        Then the output should be
            2020-08-31 14:32 A second entry in what I hope to be a long series.

        Examples: Configs
        | config_file        |
        | basic_onefile.yaml |
        | basic_folder.yaml  |
        # | basic_dayone.yaml  | @todo


    Scenario Outline: Delete flag with -and deletes boolean AND of tagged entries
        Given we use the config "<config_file>"
        When we run "jrnl --delete -and @tagone @tagtwo" and enter
            Y
        Then the error output should contain "1 entry deleted"
        When we run "jrnl -99 --short"
        Then the output should be
            2020-08-31 14:32 A second entry in what I hope to be a long series.
            2020-09-24 09:14 The third entry finally after weeks without writing.

        Examples: Configs
        | config_file        |
        | basic_onefile.yaml |
        | basic_folder.yaml  |
        # | basic_dayone.yaml  | @todo


    Scenario Outline: Delete flag with -not does not delete entries from given tag
        Given we use the config "<config_file>"
        When we run "jrnl --delete @tagone -not @ipsum" and enter
            Y
        Then the error output should contain "1 entry deleted"
        When we run "jrnl -99 --short"
        Then the output should be
            2020-08-29 11:11 Entry the first.
            2020-08-31 14:32 A second entry in what I hope to be a long series.

        Examples: Configs
        | config_file        |
        | basic_onefile.yaml |
        | basic_folder.yaml  |
        # | basic_dayone.yaml  | @todo


    Scenario Outline: Delete flag with -from search operator only deletes entries since that date
        Given we use the config "<config_file>"
        When we run "jrnl --delete -from 2020-09-01" and enter
            Y
        Then the error output should contain "1 entry deleted"
        When we run "jrnl -99 --short"
        Then the output should be
            2020-08-29 11:11 Entry the first.
            2020-08-31 14:32 A second entry in what I hope to be a long series.

        Examples: Configs
        | config_file        |
        | basic_onefile.yaml |
        | basic_folder.yaml  |
        # | basic_dayone.yaml  | @todo


    Scenario Outline: Delete flag with -to only deletes entries up to specified date
        Given we use the config "<config_file>"
        When we run "jrnl --delete -to 2020-08-31" and enter
            Y
            Y
        Then the error output should contain "2 entries deleted"
        When we run "jrnl -99 --short"
        Then the output should be
            2020-09-24 09:14 The third entry finally after weeks without writing.

        Examples: Configs
        | config_file        |
        | basic_onefile.yaml |
        | basic_folder.yaml  |
        # | basic_dayone.yaml  | @todo


    Scenario Outline: Delete flag with -starred only deletes starred entries
        Given we use the config "<config_file>"
        When we run "jrnl --delete -starred" and enter
            Y
        Then the error output should contain "1 entry deleted"
        When we run "jrnl -99 --short"
        Then the output should be
            2020-08-29 11:11 Entry the first.
            2020-09-24 09:14 The third entry finally after weeks without writing.

        Examples: Configs
        | config_file        |
        | basic_onefile.yaml |
        | basic_folder.yaml  |
        # | basic_dayone.yaml  | @todo


    Scenario Outline: Delete flag with -contains only entries containing expression
        Given we use the config "<config_file>"
        When we run "jrnl --delete -contains dignissim" and enter
            Y
        Then the error output should contain "1 entry deleted"
        When we run "jrnl -99 --short"
        Then the output should be
            2020-08-31 14:32 A second entry in what I hope to be a long series.
            2020-09-24 09:14 The third entry finally after weeks without writing.

        Examples: Configs
        | config_file        |
        | basic_onefile.yaml |
        | basic_folder.yaml  |
        # | basic_dayone.yaml  | @todo
