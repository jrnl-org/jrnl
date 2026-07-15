# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

Feature: Importing data

    Scenario: Importing into a v1 journal upgrades it to v3 and persists the config change
        Given we use the config "encrypted_v1_journal_legacy_config.yaml"
        And we use the password "bad doggie no biscuit" if prompted
        When we run "jrnl --import" and pipe "[2020-07-05 15:00] Observe and import."
        Then the journal file should be encrypted with jrnlv3
        And the config should contain "encrypt: true"
        When we run "jrnl --format json"
        Then we should get no error
        And the output should be valid JSON
        Given we parse the output as JSON
        Then "entries" in the parsed output should have 3 elements
        And "entries.0.title" in the parsed output should be
            """
            My first entry.
            """
        And "entries.1.title" in the parsed output should be
            """
            Life is good.
            """
        And "entries.2.title" in the parsed output should be
            """
            Observe and import.
            """

    Scenario Outline: --import allows new entry from stdin
        Given we use the config "<config_file>"
        And we use the password "test" if prompted
        When we run "jrnl --import" and pipe "[2020-07-05 15:00] Observe and import."
        When we run "jrnl -9 --short"
        Then the output should contain "Observe and import"

        Examples: Configs
        | config_file          |
        | basic_onefile.yaml   |
        | basic_encrypted.yaml |
        | basic_folder.yaml    |
        # | basic_dayone.yaml    | @todo

    Scenario Outline: --import allows new large entry from stdin
        Given we use the config "<config_file>"
        And we use the password "test" if prompted
        When we run "jrnl --import" and pipe
            """
            [2020-07-05 15:00] Observe and import.
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent malesuada quis
            est ac dignissim. Aliquam dignissim rutrum pretium. Phasellus pellentesque augue
            et venenatis facilisis. Suspendisse potenti. Sed dignissim sed nisl eu consequat.
            Aenean ante ex, elementum ut interdum et, mattis eget lacus. In commodo nulla nec
            tellus placerat, sed ultricies metus bibendum. Duis eget venenatis erat. In at
            dolor dui end of entry.
            """
        When we run "jrnl -on 2020-07-05"
        Then the output should contain "2020-07-05 15:00 Observe and import."
        And the output should contain "Lorem ipsum"
        And the output should contain "end of entry."

        Examples: Configs
        | config_file          |
        | basic_onefile.yaml   |
        | basic_encrypted.yaml |
        | basic_folder.yaml    |
        # | basic_dayone.yaml    | @todo

    Scenario Outline: --import allows multiple new entries from stdin
        Given we use the config "<config_file>"
        And we use the password "test" if prompted
        When we run "jrnl --import" and pipe
            """
            [2020-07-05 15:00] Observe and import.
            Lorem ipsum dolor sit amet, consectetur adipiscing elit.

            [2020-07-05 15:01] Twice as nice.
            Sed dignissim sed nisl eu consequat.
            """
        When we run "jrnl -on 2020-07-05"
        Then the output should contain "2020-07-05 15:00 Observe and import."
        And the output should contain "Lorem ipsum"
        And the output should contain "2020-07-05 15:01 Twice as nice."
        And the output should contain "Sed dignissim"

        Examples: Configs
        | config_file          |
        | basic_onefile.yaml   |
        | basic_encrypted.yaml |
        | basic_folder.yaml    |
        # | basic_dayone.yaml    | @todo

    Scenario: --import allows import new entries from file
        Given we use the config "simple.yaml"
        When we run "jrnl -99"
        Then the output should contain "My first entry."
        And the output should contain "Life is good."
        But the output should not contain "I have an @idea"
        And the output should not contain "I met with"
        When we run "jrnl --import --file features/journals/tags.journal"
        And we run "jrnl -99"
        Then the output should contain "My first entry."
        And the output should contain "Life is good."
        And the output should contain "PROFIT!"

    Scenario: --import prioritizes --file over pipe data if both are given
        Given we use the config "simple.yaml"
        When we run "jrnl -99"
        Then the output should contain "My first entry."
        And the output should contain "Life is good."
        But the output should not contain "I have an @idea"
        And the output should not contain "I met with"
        When we run "jrnl --import --file features/journals/tags.journal" and pipe
            """
            [2020-07-05 15:00] I should not exist!
            """
        And we run "jrnl -99"
        Then the output should contain "My first entry."
        And the output should contain "PROFIT!"
        But the output should not contain "I should not exist!"

