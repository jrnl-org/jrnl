Feature: DayOne Ingetration

    Scenario: Loading a DayOne Journal
        Given we use the config "dayone.json"
        When we run "jrnl -until now"
        Then we should get no error
        and the output should be
            """
            2013-05-17 11:39 This entry has tags!

            2013-06-17 20:38 This entry has a location.

            2013-07-17 11:38 This entry is starred!

            2013-08-17 11:37 This is a DayOne entry.
            """

