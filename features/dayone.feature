Feature: Dayone specific implementation details.

    Scenario: Loading a DayOne Journal
        Given we use the config "dayone.yaml"
        When we run "jrnl -from 'feb 2013'"
        Then we should get no error
        And the output should be
            """
            2013-05-17 11:39 This entry has tags!

            2013-06-17 20:38 This entry has a location.

            2013-07-17 11:38 This entry is starred!
            """

    # broken still
    @skip
    Scenario: Entries without timezone information will be interpreted as in the current timezone
        Given we use the config "dayone.yaml"
        When we run "jrnl -until 'feb 2013'"
        Then we should get no error
        And the output should contain "2013-01-17T18:37Z" in the local time

    Scenario: Writing into Dayone
        Given we use the config "dayone.yaml"
        When we run "jrnl 01 may 1979: Being born hurts."
        And we run "jrnl -until 1980"
        Then the output should be "1979-05-01 09:00 Being born hurts."

    Scenario: Loading tags from a DayOne Journal
        Given we use the config "dayone.yaml"
        When we run "jrnl --tags"
        Then the output should be
            """
            @work                : 1
            @play                : 1
            """

    Scenario: Saving tags from a DayOne Journal
        Given we use the config "dayone.yaml"
        When we run "jrnl A hard day at @work"
        And we run "jrnl --tags"
        Then the output should be
            """
            @work                : 2
            @play                : 1
            """

    Scenario: Filtering by tags from a DayOne Journal
        Given we use the config "dayone.yaml"
        When we run "jrnl @work"
        Then the output should be "2013-05-17 11:39 This entry has tags!"

    Scenario: Exporting dayone to json
        Given we use the config "dayone.yaml"
        When we run "jrnl --export json"
        Then we should get no error
        And the output should be parsable as json
        And the json output should contain entries.0.uuid = "4BB1F46946AD439996C9B59DE7C4DDC1"

    Scenario: Writing into Dayone adds extended metadata
        Given we use the config "dayone.yaml"
        When we run "jrnl 01 may 1979: Being born hurts."
        And we run "jrnl --export json"
        Then "entries" in the json output should have 5 elements
        And the json output should contain entries.0.creator.software_agent
        And the json output should contain entries.0.creator.os_agent
        And the json output should contain entries.0.creator.host_name
        And the json output should contain entries.0.creator.generation_date
        And the json output should contain entries.0.creator.device_agent
        And "entries.0.creator.software_agent" in the json output should contain "jrnl"

    # fails when system time is UTC (as on Travis-CI)
    @skip
    Scenario: DayOne tag searching should work with tags containing a mixture of upper and lower case.
        # https://github.com/jrnl-org/jrnl/issues/354
        Given we use the config "dayone.yaml"
        When we run "jrnl @plAy"
        Then the output should contain "2013-05-17 11:39 This entry has tags!"

    # fails when system time is UTC (as on Travis-CI)
    @skip
    Scenario: Title with an embedded period on DayOne journal
        Given we use the config "dayone.yaml"
        When we run "jrnl 04-24-2014: "Ran 6.2 miles today in 1:02:03. I'm feeling sore because I forgot to stretch.""
        Then we should see the message "Entry added"
        When we run "jrnl -1"
        Then the output should be
            """
            2014-04-24 09:00 Ran 6.2 miles today in 1:02:03.
            | I'm feeling sore because I forgot to stretch.
            """

    Scenario: Loading entry with ambiguous time stamp
        #https://github.com/jrnl-org/jrnl/issues/153
        Given we use the config "bug153.yaml"
        When we run "jrnl -1"
        Then we should get no error
        And the output should be
            """
            2013-10-27 03:27 Some text.
            """

    Scenario: Empty DayOne entry bodies should not error
        # https://github.com/jrnl-org/jrnl/issues/780
        Given we use the config "bug780.yaml"
        When we run "jrnl --short"
        Then we should get no error

