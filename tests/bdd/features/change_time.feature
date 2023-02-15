# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

Feature: Change entry times in journal
    Scenario Outline: Change time flag changes single entry timestamp
        Given we use the config "<config_file>"
        And we use the password "test" if prompted
        When we run "jrnl -1"
        Then the output should contain "2020-09-24 09:14 The third entry finally"
        When we run "jrnl -1 --change-time '2022-04-23 10:30'" and enter
            Y
        When we run "jrnl -99 --short"
        Then the output should be
            2020-08-29 11:11 Entry the first.
            2020-08-31 14:32 A second entry in what I hope to be a long series.
            2022-04-23 10:30 The third entry finally after weeks without writing.

        Examples: Configs
        | config_file          |
        | basic_onefile.yaml   |
        | basic_encrypted.yaml |
        | basic_folder.yaml    |
        # | basic_dayone.yaml    | @todo

    Scenario Outline: Change flag changes prompted entries
        Given we use the config "<config_file>"
        And we use the password "test" if prompted
        When we run "jrnl -1"
        Then the output should contain "2020-09-24 09:14 The third entry finally"
        When we run "jrnl --change-time '2022-04-23 10:30'" and enter
            Y
            N
            Y
        When we run "jrnl -99 --short"
        Then the output should be
            2020-08-31 14:32 A second entry in what I hope to be a long series.
            2022-04-23 10:30 Entry the first.
            2022-04-23 10:30 The third entry finally after weeks without writing.

        Examples: Configs
        | config_file          |
        | basic_onefile.yaml   |
        | basic_encrypted.yaml |
        | basic_folder.yaml    |
        # | basic_dayone.yaml  | @todo


    Scenario Outline: Change time flag with nonsense input changes nothing
        Given we use the config "<config_file>"
        When we run "jrnl --change-time now asdfasdf"
        Then the output should contain "No entries to modify"
        And the error output should not contain "entries modified"
        And the error output should not contain "entries deleted"
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


    Scenario Outline: Change time flag with tag only changes tagged entries
        Given we use the config "<config_file>"
        When we run "jrnl --change-time '2022-04-23 10:30' @ipsum" and enter
            Y
        When we run "jrnl -99 --short"
        Then the output should be
            2020-08-31 14:32 A second entry in what I hope to be a long series.
            2020-09-24 09:14 The third entry finally after weeks without writing.
            2022-04-23 10:30 Entry the first.

        Examples: Configs
        | config_file        |
        | basic_onefile.yaml |
        | basic_folder.yaml  |
        # | basic_dayone.yaml  | @todo


    Scenario Outline: Change time flag with multiple tags changes all entries matching any of the tags
        Given we use the config "<config_file>"
        When we run "jrnl --change-time '2022-04-23 10:30'  @ipsum @tagthree" and enter
            Y
            Y
        When we run "jrnl -99 --short"
        Then the output should be
            2020-08-31 14:32 A second entry in what I hope to be a long series.
            2022-04-23 10:30 Entry the first.
            2022-04-23 10:30 The third entry finally after weeks without writing.

        Examples: Configs
        | config_file        |
        | basic_onefile.yaml |
        | basic_folder.yaml  |
        # | basic_dayone.yaml  | @todo


    Scenario Outline: Change time flag with -and changes boolean AND of tagged entries
        Given we use the config "<config_file>"
        When we run "jrnl --change-time '2022-04-23 10:30' -and @tagone @tagtwo" and enter
            Y
        When we run "jrnl -99 --short"
        Then the output should be
            2020-08-31 14:32 A second entry in what I hope to be a long series.
            2020-09-24 09:14 The third entry finally after weeks without writing.
            2022-04-23 10:30 Entry the first.

        Examples: Configs
        | config_file        |
        | basic_onefile.yaml |
        | basic_folder.yaml  |
        # | basic_dayone.yaml  | @todo


    Scenario Outline: Change time flag with -not does not change entries from given tag
        Given we use the config "<config_file>"
        When we run "jrnl --change-time '2022-04-23 10:30' @tagone -not @ipsum" and enter
            Y
        When we run "jrnl -99 --short"
        Then the output should be
            2020-08-29 11:11 Entry the first.
            2020-08-31 14:32 A second entry in what I hope to be a long series.
            2022-04-23 10:30 The third entry finally after weeks without writing.

        Examples: Configs
        | config_file        |
        | basic_onefile.yaml |
        | basic_folder.yaml  |
        # | basic_dayone.yaml  | @todo


    Scenario Outline: Change time flag with -from search operator only changes entries since that date
        Given we use the config "<config_file>"
        When we run "jrnl --change-time '2022-04-23 10:30' -from 2020-09-01" and enter
            Y
        When we run "jrnl -99 --short"
        Then the output should be
            2020-08-29 11:11 Entry the first.
            2020-08-31 14:32 A second entry in what I hope to be a long series.
            2022-04-23 10:30 The third entry finally after weeks without writing.

        Examples: Configs
        | config_file        |
        | basic_onefile.yaml |
        | basic_folder.yaml  |
        # | basic_dayone.yaml  | @todo


    Scenario Outline: Change time flag with -to only changes entries up to specified date
        Given we use the config "<config_file>"
        When we run "jrnl --change-time '2022-04-23 10:30' -to 2020-08-31" and enter
            Y
            Y
        When we run "jrnl -99 --short"
        Then the output should be
            2020-09-24 09:14 The third entry finally after weeks without writing.
            2022-04-23 10:30 Entry the first.
            2022-04-23 10:30 A second entry in what I hope to be a long series.

        Examples: Configs
        | config_file        |
        | basic_onefile.yaml |
        | basic_folder.yaml  |
        # | basic_dayone.yaml  | @todo


    Scenario Outline: Change time flag with -starred only changes starred entries
        Given we use the config "<config_file>"
        When we run "jrnl --change-time '2022-04-23 10:30' -starred" and enter
            Y
        When we run "jrnl -99 --short"
        Then the output should be
            2020-08-29 11:11 Entry the first.
            2020-09-24 09:14 The third entry finally after weeks without writing.
            2022-04-23 10:30 A second entry in what I hope to be a long series.

        Examples: Configs
        | config_file        |
        | basic_onefile.yaml |
        | basic_folder.yaml  |
        # | basic_dayone.yaml  | @todo


    Scenario Outline: Change time flag with -contains only changes entries containing expression
        Given we use the config "<config_file>"
        When we run "jrnl --change-time '2022-04-23 10:30'  -contains dignissim" and enter
            Y
        Then the error output should contain "1 entry modified"
        When we run "jrnl -99 --short"
        Then the output should be
            2020-08-31 14:32 A second entry in what I hope to be a long series.
            2020-09-24 09:14 The third entry finally after weeks without writing.
            2022-04-23 10:30 Entry the first.

        Examples: Configs
        | config_file        |
        | basic_onefile.yaml |
        | basic_folder.yaml  |
        # | basic_dayone.yaml  | @todo


    Scenario Outline: Change time flag with no enties specified changes nothing
        Given we use the config "<config_file>"
        And we use the password "test" if prompted
        When we run "jrnl --change-time" and enter
            N
            N
            N
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


    Scenario Outline: --change-time with --edit modifies selected entries
        Given we use the config "<config_file>"
        And we write nothing to the editor if opened
        And we use the password "test" if prompted
        When we run "jrnl --change-time '2022-04-23 10:30' --edit" and enter
            Y
            N
            Y
        Then the error output should contain "No entry to save"
        And the editor should have been called
        When we run "jrnl -99 --short"
        Then the output should be
            2020-08-31 14:32 A second entry in what I hope to be a long series.
            2022-04-23 10:30 Entry the first.
            2022-04-23 10:30 The third entry finally after weeks without writing.

        Examples: Configs
        | config_file        |
        | basic_onefile.yaml |
        | basic_folder.yaml  |
        # | basic_dayone.yaml    | @todo
