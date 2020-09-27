Feature: Importing data

    Scenario Outline: --import allows new entry from stdin
        Given we use the config "<config>.yaml"
        And we use the password "test" if prompted
        When we run "jrnl --import" and pipe "[2020-07-05 15:00] Observe and import."
        Then we flush the output
        When we run "jrnl -c import"
        Then the output should contain "Observe and import"

        Examples: Configs
        | config          |
        | basic_onefile   |
        | basic_encrypted |
        # | basic_folder    | @todo
        # | basic_dayone    | @todo

    Scenario Outline: --import allows new large entry from stdin
        Given we use the config "<config>.yaml"
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
        Then we flush the output
        When we run "jrnl -on 2020-07-05"
        Then the output should contain "2020-07-05 15:00 Observe and import."
        And the output should contain "Lorem ipsum"
        And the output should contain "end of entry."

        Examples: Configs
        | config          |
        | basic_onefile   |
        | basic_encrypted |
        # | basic_folder    | @todo
        # | basic_dayone    | @todo

    Scenario Outline: --import allows multiple new entries from stdin
        Given we use the config "<config>.yaml"
        And we use the password "test" if prompted
        When we run "jrnl --import" and pipe
            """
            [2020-07-05 15:00] Observe and import.
            Lorem ipsum dolor sit amet, consectetur adipiscing elit.

            [2020-07-05 15:01] Twice as nice.
            Sed dignissim sed nisl eu consequat.
            """
        Then we flush the output
        When we run "jrnl -on 2020-07-05"
        Then the output should contain "2020-07-05 15:00 Observe and import."
        And the output should contain "Lorem ipsum"
        And the output should contain "2020-07-05 15:01 Twice as nice."
        And the output should contain "Sed dignissim"

        Examples: Configs
        | config          |
        | basic_onefile   |
        | basic_encrypted |
        # | basic_folder    | @todo
        # | basic_dayone    | @todo

    Scenario: --import allows import new entries from file
        Given we use the config "simple.yaml"
        Then the journal should contain "My first entry."
        And the journal should contain "Life is good."
        But the journal should not contain "I have an @idea"
        And the journal should not contain "I met with"
        When we run "jrnl --import --file features/journals/tags.journal"
        Then the journal should contain "My first entry."
        And the journal should contain "Life is good."
        And the journal should contain "PROFIT!"

    Scenario: --import prioritizes --file over pipe data if both are given
        Given we use the config "simple.yaml"
        Then the journal should contain "My first entry."
        And the journal should contain "Life is good."
        But the journal should not contain "I have an @idea"
        And the journal should not contain "I met with"
        When we run "jrnl --import --file features/journals/tags.journal" and pipe
            """
            [2020-07-05 15:00] I should not exist!
            """
        Then the journal should contain "My first entry."
        And the journal should contain "PROFIT!"
        But the journal should not contain "I should not exist!"

