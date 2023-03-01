# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

Feature: Test combinations of edit, change-time, and delete

    Scenario Outline: --change-time with --edit modifies selected entries
        Given we use the config "<config_file>"
        And we write nothing to the editor if opened
        And we use the password "test" if prompted
        When we run "jrnl --change-time '2022-04-23 10:30' --edit" and enter
            Y
            N
            Y
        Then the error output should contain "No text received from editor. Were you trying to delete all the entries?"
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

    Scenario Outline: --delete with --edit deletes selected entries
        Given we use the config "<config_file>"
        And we append to the editor if opened
        	[2023-02-21 10:32] Here is a new entry
        And we use the password "test" if prompted
        When we run "jrnl --delete --edit" and enter
            Y
            N
            Y
        Then the editor should have been called
        And the error output should contain "3 entries found"
        And the error output should contain "2 entries deleted" 
        And the error output should contain "1 entry added"
        When we run "jrnl -99 --short"
        Then the error output should contain "2 entries found"
        And the output should be
            2020-08-31 14:32 A second entry in what I hope to be a long series.
            2023-02-21 10:32 Here is a new entry
            
        Examples: Configs
        | config_file        |
        | basic_onefile.yaml |
        | basic_folder.yaml  |
        # | basic_dayone.yaml    | @todo

    Scenario Outline: --change-time with --delete affects appropriate entries
        Given we use the config "<config_file>"
        And we use the password "test" if prompted
        # --change-time is asked first, then --delete
        When we run "jrnl --change-time '2022-04-23 10:30' --delete" and enter
            N
            N
            Y
            Y
            N
            N
        Then the error output should contain "3 entries found"
        And the error output should contain "1 entry deleted"
        And the error output should contain "1 entry modified"
        When we run "jrnl -99 --short"
        Then the output should be
            2020-08-31 14:32 A second entry in what I hope to be a long series.
            2022-04-23 10:30 The third entry finally after weeks without writing.

        Examples: Configs
        | config_file        |
        | basic_onefile.yaml |
        | basic_folder.yaml  |
        # | basic_dayone.yaml    | @todo

    Scenario Outline: Combining --change-time and --delete and --edit affects appropriate entries
        Given we use the config "<config_file>"
        And we append to the editor if opened
        	[2023-02-21 10:32] Here is a new entry
        And we use the password "test" if prompted
        # --change-time is asked first, then --delete, then --edit
        When we run "jrnl --change-time '2022-04-23 10:30' --delete --edit" and enter
            N
            Y
            Y
            Y
            Y
            N
        Then the error output should contain "3 entries found"
        And the error output should contain "2 entries deleted"
        And the error output should contain "1 entry modified" # only 1, because the other was deleted
        And the error output should contain "1 entry added" # by edit
        When we run "jrnl -99 --short"
        Then the output should be
            2022-04-23 10:30 The third entry finally after weeks without writing.
            2023-02-21 10:32 Here is a new entry

        Examples: Configs
        | config_file        |
        | basic_onefile.yaml |
        | basic_folder.yaml  |
        # | basic_dayone.yaml    | @todo
