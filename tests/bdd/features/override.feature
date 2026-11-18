# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

Feature: Implementing Runtime Overrides for Select Configuration Keys

        Scenario: Override configured editor with built-in input === editor:''
        Given we use the config "basic_encrypted.yaml"
        And we use the password "test" if prompted
        When we run "jrnl --config-override editor ''" and type
            """
            This is a journal entry
            """
        Then the stdin prompt should have been called
        And the editor should not have been called
        When we run "jrnl -1"
        Then the output should contain "This is a journal entry"


        Scenario: Postconfig commands with overrides
        Given we use the config "basic_encrypted.yaml"
        And we use the password "test" if prompted
        When we run "jrnl --decrypt --config-override highlight false --config-override editor nano"
        Then the config in memory should contain "highlight: false"
        Then the editor should not have been called


        Scenario: Override configured linewrap with a value of 23
        Given we use the config "simple.yaml"
        And we use the password "test" if prompted
        When we run "jrnl  -2 --config-override linewrap 23 --format fancy"
        Then the standard output should contain
            """
            ┎─────╮2013-06-09 15:39
            ┃ My  ╘═══════════════╕
            """
        And the standard output should contain
            """
            ┠╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤
            ┃ Everything is       │
            ┃ alright             │
            ┖─────────────────────┘
            ┎─────╮2013-06-10 15:40
            ┃ Lif ╘═══════════════╕
            """
        And the standard output should contain
            """
            ┠╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤
            ┃ But I'm better.     │
            ┖─────────────────────┘
            """


        Scenario Outline: Override linewrap that is also set at the journal level
        # https://github.com/jrnl-org/jrnl/issues/1224
        Given we use the config "journal_level_overrides.yaml"
        When we run "jrnl -2 --config-override <key> 23 --format fancy"
        Then we should get no error
        And the standard output should contain
            """
            ┎─────╮2013-06-09 15:39
            ┃ My  ╘═══════════════╕
            """
        And the standard output should contain
            """
            ┠╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤
            ┃ Everything is       │
            ┃ alright             │
            ┖─────────────────────┘
            """
        And the output should be 23 columns wide

        Examples: Override keys
            | key                       |
            | linewrap                  |
            | journals.default.linewrap |


        Scenario Outline: Override linewrap for any journal, whether or not it sets its own
        # https://github.com/jrnl-org/jrnl/issues/1224
        Given we use the config "journal_level_overrides.yaml"
        When we run "jrnl <journal> -1 --config-override linewrap 23 --format fancy"
        Then we should get no error
        And the output should contain "But I'm better."
        And the output should be 23 columns wide

        Examples: Journals
            | journal |
            | default |
            | work    |
            | plain   |


        Scenario: The last override of a key wins over the journal-level value
        # https://github.com/jrnl-org/jrnl/issues/1224
        Given we use the config "journal_level_overrides.yaml"
        When we run "jrnl -1 --config-override linewrap 60 --config-override linewrap 23 --format fancy"
        Then we should get no error
        And the output should be 23 columns wide


        Scenario: The journal-level color is used when there is no override
        Given we use the config "journal_level_overrides.yaml"
        When we run "jrnl -1"
        Then we should get no error
        # red (journals.default.colors.body)
        And the output should match "\x1b\[31mBut I'm better\."


        Scenario: Override a nested color that is also set at the journal level
        # https://github.com/jrnl-org/jrnl/issues/1224
        Given we use the config "journal_level_overrides.yaml"
        When we run "jrnl -1 --config-override colors.body blue"
        Then we should get no error
        # blue (--config-override), not the journal's red
        And the output should match "\x1b\[34mBut I'm better\."
        And the config in memory should contain "colors.body: blue"


        Scenario Outline: Overrides are not saved to the config file by commands that save it
        # https://github.com/jrnl-org/jrnl/issues/1224
        Given we use the config "journal_level_overrides.yaml"
        And we don't have a keyring
        When we run "jrnl --encrypt --config-override <key> <value>" and enter
            """
            swordfish
            swordfish
            n
            """
        Then we should get no error
        And the output should contain "Journal encrypted"
        And the config for journal "default" should contain "encrypt: true"
        And the config for journal "default" should contain "<key>: <journal_value>"
        And the config should contain "<key>: <global_value>"

        Examples: Overrides
            | key         | value | journal_value | global_value |
            | linewrap    | 23    | 80            | 80           |
            | colors.body | blue  | red           | none         |


        Scenario Outline: Journal paths overridden on the command line are not saved to the config file
        # https://github.com/jrnl-org/jrnl/issues/1224
        # docs/advanced.md suggests overriding journals.<name> for a single run
        Given we use the config "journal_level_overrides.yaml"
        And we don't have a keyring
        When we run "jrnl --encrypt --config-override <key> features/journals/elsewhere.journal" and enter
            """
            swordfish
            swordfish
            n
            """
        Then we should get no error
        And the output should contain "Journal encrypted"
        And the config should contain "<key>: features/journals/simple.journal"

        Examples: Journal path keys
            | key                   |
            | journals.plain        |
            | journals.work.journal |


        Scenario: Override color selections with runtime overrides
        Given we use the config "basic_encrypted.yaml"
        And we use the password "test" if prompted
        When we run "jrnl -1 --config-override colors.body blue"
        Then the config in memory should contain "colors.body: blue"

        Scenario: Override color selections with --co alias
        Given we use the config "basic_encrypted.yaml"
        And we use the password "test" if prompted
        When we run "jrnl -1 --co colors.body blue"
        Then the config in memory should contain "colors.body: blue"

        Scenario: Apply multiple config overrides
        Given we use the config "basic_encrypted.yaml"
        And we use the password "test" if prompted
        When we run "jrnl -1 --config-override colors.body green --config-override editor 'nano'"
        Then the config in memory should contain
            """
            editor: nano
            colors:
                title: none
                body: green
                tags: none
                date: none
            """


        Scenario: Override default journal
        Given we use the config "basic_dayone.yaml"
        And we use the password "test" if prompted
        When we run "jrnl --config-override journals.default features/journals/simple.journal 20 Mar 2000: The rain in Spain comes from clouds"
        Then we should get no error
        When we run "jrnl -3 --config-override journals.default features/journals/simple.journal"
        Then the output should be
            """
            2000-03-20 09:00 The rain in Spain comes from clouds

            2013-06-09 15:39 My first entry.
            | Everything is alright

            2013-06-10 15:40 Life is good.
            | But I'm better.
            """


        Scenario: Make an entry into an overridden journal
        Given we use the config "basic_dayone.yaml"
        And we use the password "test" if prompted
        When we run "jrnl --config-override journals.temp features/journals/simple.journal temp Sep 06 1969: @say Ni"
        Then we should get no error
        And the output should contain "Entry added"
        When we run "jrnl --config-override journals.temp features/journals/simple.journal temp -3"
        Then the output should be
            """
            1969-09-06 09:00 @say Ni

            2013-06-09 15:39 My first entry.
            | Everything is alright

            2013-06-10 15:40 Life is good.
            | But I'm better.
            """
