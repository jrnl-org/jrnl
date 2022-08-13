# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

Feature: Implementing Runtime Overrides for Select Configuration Keys

        Scenario: Override configured editor with built-in input === editor:''
        Given we use the config "basic_encrypted.yaml"
        And we use the password "test" if prompted
        When we run "jrnl --config-override editor ''" and type
          This is a journal entry
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
        Then the output should be
            ┎─────╮2013-06-09 15:39
            ┃ My  ╘═══════════════╕
            ┃ fir st  ent ry.     │
            ┠╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤
            ┃ Everything is       │
            ┃ alright             │
            ┖─────────────────────┘
            ┎─────╮2013-06-10 15:40
            ┃ Lif ╘═══════════════╕
            ┃ e is  goo d.        │
            ┠╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤
            ┃ But I'm better.     │
            ┖─────────────────────┘


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
            editor: nano
            colors:
                title: none
                body: green
                tags: none
                date: none


        Scenario: Override default journal
        Given we use the config "basic_dayone.yaml"
        And we use the password "test" if prompted
        When we run "jrnl --config-override journals.default features/journals/simple.journal 20 Mar 2000: The rain in Spain comes from clouds"
        Then we should get no error
        And the output should contain "Entry added"
        When we run "jrnl -3 --config-override journals.default features/journals/simple.journal"
        Then the output should be
            2000-03-20 09:00 The rain in Spain comes from clouds

            2013-06-09 15:39 My first entry.
            | Everything is alright

            2013-06-10 15:40 Life is good.
            | But I'm better.


        Scenario: Make an entry into an overridden journal
        Given we use the config "basic_dayone.yaml"
        And we use the password "test" if prompted
        When we run "jrnl --config-override journals.temp features/journals/simple.journal temp Sep 06 1969: @say Ni"
        Then we should get no error
        And the output should contain "Entry added"
        When we run "jrnl --config-override journals.temp features/journals/simple.journal temp -3"
        Then the output should be
            1969-09-06 09:00 @say Ni

            2013-06-09 15:39 My first entry.
            | Everything is alright

            2013-06-10 15:40 Life is good.
            | But I'm better.
