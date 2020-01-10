Feature: Day One 2.0 implementation details.


    Scenario: Loading a Day One 2.0 journal
        Given we use the config "dayone2.yaml"
        When we run "jrnl -n 2"
        Then we should get no error
        and the output should be
            """
            2020-01-10 12:21 Entry Number Two.
            | And a bit of text over here.

            2020-01-10 12:22 Entry Number One.
            """

