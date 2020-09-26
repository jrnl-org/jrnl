Feature: Delete entries from journal
    Scenario Outline: Delete flag allows deletion of single entry
        Given we use the config "<config>.yaml"
        When we run "jrnl -n 1"
        Then the output should contain "2020-09-24 09:14 The third entry finally"
        When we run "jrnl --delete" and enter
            """
            N
            N
            Y
            """
        Then we flush the output
        When we run "jrnl -99 --short"
        Then the output should be
            """
            2020-08-29 11:11 Entry the first.
            2020-08-31 14:32 A second entry in what I hope to be a long series.
            """

        Examples: Configs
        | config        |
        | basic_onefile |
        # | basic_folder  | @todo
        # | basic_dayone  | @todo

    Scenario Outline: Backing out of interactive delete does not change journal
        Given we use the config "<config>.yaml"
        When we run "jrnl --delete -n 1" and enter
            """
            N
            """
        Then we flush the output
        When we run "jrnl -99 --short"
        Then the output should be
            """
            2020-08-29 11:11 Entry the first.
            2020-08-31 14:32 A second entry in what I hope to be a long series.
            2020-09-24 09:14 The third entry finally after weeks without writing.
            """

        Examples: Configs
        | config        |
        | basic_onefile |
        | basic_folder  |
        | basic_dayone  |


    Scenario Outline: Delete flag with nonsense input deletes nothing (issue #932)
        Given we use the config "<config>.yaml"
        When we run "jrnl --delete asdfasdf"
        Then we flush the output
        When we run "jrnl -99 --short"
        Then the output should be
            """
            2020-08-29 11:11 Entry the first.
            2020-08-31 14:32 A second entry in what I hope to be a long series.
            2020-09-24 09:14 The third entry finally after weeks without writing.
            """

        Examples: Configs
        | config        |
        | basic_onefile |
        | basic_folder  |
        | basic_dayone  |

    Scenario Outline: Delete flag with tag only deletes tagged entries
        Given we use the config "<config>.yaml"
        When we run "jrnl --delete @ipsum" and enter
            """
            Y
            """
        Then we flush the output
        When we run "jrnl -99 --short"
        Then the output should be
            """
            2020-08-31 14:32 A second entry in what I hope to be a long series.
            2020-09-24 09:14 The third entry finally after weeks without writing.
            """

        Examples: Configs
        | config        |
        | basic_onefile |
        # | basic_folder  | @todo
        # | basic_dayone  | @todo


    Scenario Outline: Delete flag with multiple tags deletes all entries matching any of the tags
        Given we use the config "<config>.yaml"
        When we run "jrnl --delete @ipsum @tagthree" and enter
            """
            Y
            Y
            """
        Then we flush the output
        When we run "jrnl -99 --short"
        Then the output should be
            """
            2020-08-31 14:32 A second entry in what I hope to be a long series.
            """

        Examples: Configs
        | config        |
        | basic_onefile |
        # | basic_folder  | @todo
        # | basic_dayone  | @todo

    Scenario Outline: Delete flag with -and deletes boolean AND of tagged entries
        Given we use the config "<config>.yaml"
        When we run "jrnl --delete -and @tagone @tagtwo" and enter
            """
            Y
            """
        Then we flush the output
        When we run "jrnl -99 --short"
        Then the output should be
            """
            2020-08-31 14:32 A second entry in what I hope to be a long series.
            2020-09-24 09:14 The third entry finally after weeks without writing.
            """

        Examples: Configs
        | config        |
        | basic_onefile |
        # | basic_folder  | @todo
        # | basic_dayone  | @todo

    Scenario Outline: Delete flag with -not does not delete entries from given tag
        Given we use the config "<config>.yaml"
        When we run "jrnl --delete @tagone -not @ipsum" and enter
            """
            Y
            """
        Then we flush the output
        When we run "jrnl -99 --short"
        Then the output should be
            """
            2020-08-29 11:11 Entry the first.
            2020-08-31 14:32 A second entry in what I hope to be a long series.
            """

        Examples: Configs
        | config        |
        | basic_onefile |
        # | basic_folder  | @todo
        # | basic_dayone  | @todo

    Scenario Outline: Delete flag with -from search operator only deletes entries since that date
        Given we use the config "<config>.yaml"
        When we run "jrnl --delete -from 2020-09-01" and enter
            """
            Y
            """
        Then we flush the output
        When we run "jrnl -99 --short"
        Then the output should be
            """
            2020-08-29 11:11 Entry the first.
            2020-08-31 14:32 A second entry in what I hope to be a long series.
            """

        Examples: Configs
        | config        |
        | basic_onefile |
        # | basic_folder  | @todo
        # | basic_dayone  | @todo

    Scenario Outline: Delete flag with -to only deletes entries up to specified date
        Given we use the config "<config>.yaml"
        When we run "jrnl --delete -to 2020-08-31" and enter
            """
            Y
            Y
            """
        Then we flush the output
        When we run "jrnl -99 --short"
        Then the output should be
            """
            2020-09-24 09:14 The third entry finally after weeks without writing.
            """

        Examples: Configs
        | config        |
        | basic_onefile |
        # | basic_folder  | @todo
        # | basic_dayone  | @todo


    Scenario Outline: Delete flag with -starred only deletes starred entries
        Given we use the config "<config>.yaml"
        When we run "jrnl --delete -starred" and enter
            """
            Y
            """
        Then we flush the output
        When we run "jrnl -99 --short"
        Then the output should be
            """
            2020-08-29 11:11 Entry the first.
            2020-09-24 09:14 The third entry finally after weeks without writing.
            """

        Examples: Configs
        | config        |
        | basic_onefile |
        # | basic_folder  | @todo
        # | basic_dayone  | @todo

    Scenario Outline: Delete flag with -contains only entries containing expression
        Given we use the config "<config>.yaml"
        When we run "jrnl --delete -contains dignissim" and enter
            """
            Y
            """
        Then we flush the output
        When we run "jrnl -99 --short"
        Then the output should be
            """
            2020-08-31 14:32 A second entry in what I hope to be a long series.
            2020-09-24 09:14 The third entry finally after weeks without writing.
            """

        Examples: Configs
        | config        |
        | basic_onefile |
        # | basic_folder  | @todo
        # | basic_dayone  | @todo

