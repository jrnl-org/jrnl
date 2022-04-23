Feature: Change entry times in journal
    Scenario Outline: Change time flag changes single entry timestamp
        Given we use the config "<config_file>"
        And we use the password "test" if prompted
        When we run "jrnl -1"
        Then the output should contain "2020-09-24 09:14 The third entry finally"
        When we run "jrnl -1 --change-time '2022-04-23 10:30'"
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


    Scenario Outline: Change time flag with nonsense input changes nothing
        Given we use the config "<config_file>"
        When we run "jrnl --change-time now asdfasdf"
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
        When we run "jrnl --change-time '2022-04-23 10:30' @ipsum"
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
        When we run "jrnl --change-time '2022-04-23 10:30'  @ipsum @tagthree"
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
        When we run "jrnl --change-time '2022-04-23 10:30' -and @tagone @tagtwo"
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
        When we run "jrnl --change-time '2022-04-23 10:30' @tagone -not @ipsum"
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
        When we run "jrnl --change-time '2022-04-23 10:30' -from 2020-09-01"
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
        When we run "jrnl --change-time '2022-04-23 10:30' -to 2020-08-31"
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
        When we run "jrnl --change-time '2022-04-23 10:30' -starred"
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
        When we run "jrnl --change-time '2022-04-23 10:30'  -contains dignissim"
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
