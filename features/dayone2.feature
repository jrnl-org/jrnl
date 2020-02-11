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

    Scenario: Verify conversion to jrnl
        Given we use the config "basic.yaml"
        When we run "jrnl --import dayone2 features/data/journals/dayone2.json"
        When we run "jrnl -ls"
        Then the output should be
            """
            2013-06-09 15:39 My first entry.
            | Everything is alright

            2013-06-10 15:40 Life is good.
            | But I'm better.
            """