Feature: DayOne Ingetration

    Scenario: Loading a DayOne Journal
        Given we use the config "dayone.json"
        When we run "jrnl -from 'feb 2013'"
        Then we should get no error
        and the output should be
            """
            2013-05-17 11:39 This entry has tags!

            2013-06-17 20:38 This entry has a location.

            2013-07-17 11:38 This entry is starred!
            """

    Scenario: Entries without timezone information will be intepreted in the current timezone
        Given we use the config "dayone.json"
        When we run "jrnl -until 'feb 2013'"
        Then we should get no error
        and the output should contain "2013-01-17T18:37Z" in the local time

    Scenario: Writing into Dayone
        Given we use the config "dayone.json"
        When we run "jrnl 01 may 1979: Being born hurts."
        and we run "jrnl -until 1980"
        Then the output should be
            """
            1979-05-01 09:00 Being born hurts.
            """

    Scenario: Loading tags from a DayOne Journal
        Given we use the config "dayone.json"
        When we run "jrnl --tags"
        Then the output should be
            """
            work                 : 1
            play                 : 1
            """

    Scenario: Saving tags from a DayOne Journal
        Given we use the config "dayone.json"
        When we run "jrnl A hard day at @work"
        and we run "jrnl --tags"
        Then the output should be
            """
            work                 : 2
            play                 : 1
            """
