Feature: Searching

    Scenario: Searching for a string
        Given we use the config "basic.yaml"
        When we run "jrnl -S life"
        Then we should get no error
        and the output should be
            """
            2013-06-10 15:40 Life is good.
            | But I'm better.
            """
