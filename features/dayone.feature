Feature: Dayone specific implementation details.

    # fails when system time is UTC (as on Travis-CI)
    @skip
    Scenario: Loading a DayOne Journal
        Given we use the config "dayone.yaml"
        When we run "jrnl -from 'feb 2013'"
        Then we should get no error
        and the output should be
            """
            2013-05-17 11:39 This entry has tags!

            2013-06-17 20:38 This entry has a location.

            2013-07-17 11:38 This entry is starred!
            """

    # fails when system time is UTC (as on Travis-CI)
    @skip
    Scenario: Entries without timezone information will be interpreted as in the current timezone
        Given we use the config "dayone.yaml"
        When we run "jrnl -until 'feb 2013'"
        Then we should get no error
        and the output should contain "2013-01-17T18:37Z" in the local time

    @skip
    Scenario: Writing into Dayone
        Given we use the config "dayone.yaml"
        When we run "jrnl 01 may 1979: Being born hurts."
        and we run "jrnl -until 1980"
        Then the output should be
            """
            1979-05-01 09:00 Being born hurts.
            """

    # fails when system time is UTC (as on Travis-CI)
    @skip
    Scenario: Loading tags from a DayOne Journal
        Given we use the config "dayone.yaml"
        When we run "jrnl --tags"
        Then the output should be
            """
            @work                : 1
            @play                : 1
            """

    # fails when system time is UTC (as on Travis-CI)
    @skip
    Scenario: Saving tags from a DayOne Journal
        Given we use the config "dayone.yaml"
        When we run "jrnl A hard day at @work"
        and we run "jrnl --tags"
        Then the output should be
            """
            @work                : 2
            @play                : 1
            """

    # fails when system time is UTC (as on Travis-CI)
    @skip
    Scenario: Filtering by tags from a DayOne Journal
        Given we use the config "dayone.yaml"
        When we run "jrnl @work"
        Then the output should be
            """
            2013-05-17 11:39 This entry has tags!
            """

    # fails when system time is UTC (as on Travis-CI)
    @skip
    Scenario: Exporting dayone to json
        Given we use the config "dayone.yaml"
        When we run "jrnl --export json"
        Then we should get no error
        and the output should be parsable as json
        and the json output should contain entries.0.uuid = "4BB1F46946AD439996C9B59DE7C4DDC1"
