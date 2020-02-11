Feature: Day One 2.0 implementation details.


    Scenario: Loading a Day One 2.0 journal
        Given we use the config "basic.yaml"
        When we run "jrnl --import dayone2 features/data/journals/dayone2.json"
        Then we should get no error
        and the output should contain "Journal exported to"

    Scenario: Day One 2.0 schema validation fails
        Given we use the config "basic.yaml"
        When we run "jrnl --import dayone2 features/data/journals/not_dayone2.json"
        Then we should get no error
        and the output should contain "not the expected Day One 2 format."

    Scenario: Converted journal is added to config
        Given we use the config "basic.yaml"
        When we run "jrnl --import dayone2 features/data/journals/dayone2.json"
        When we run "jrnl -ls"
        Then the output should contain "dayone2.txt"
        And the output should contain "default"

    Scenario: Converted journal is validated
        Given we use the config "basic.yaml"
        When we run "jrnl --import dayone2 features/data/journals/dayone2.json"
        When we run "jrnl dayone2 -n 10"
        Then the output should contain
            """
            10-01-2020 12:21 Entry Number Two.
            | With some body.

            10-01-2020 12:22 Entry Number One.
            """