Feature: Basic reading and writing to a journal

    Scenario: Loading a sample journal
        Given we use "basic.json"
        When we run "jrnl -n 2"
        Then we should get no error
        Then the output should be
            """
            2013-06-09 15:39 My first entry.
            | Everything is alright

            2013-06-10 15:40 Life is good.
            | But I'm better.
            """
