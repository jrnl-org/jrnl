Feature: Zapped Dayone bugs stay dead!

    # fails when system time is UTC (as on Travis-CI)
    @skip
    Scenario: DayOne tag searching should work with tags containing a mixture of upper and lower case.
        # https://github.com/jrnl-org/jrnl/issues/354
        Given we use the config "dayone.yaml"
        When we run "jrnl @plAy"
        Then the output should contain
            """
            2013-05-17 11:39 This entry has tags!
            """

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

    @skip_win
    Scenario: Opening an folder that's not a DayOne folder gives a nice error message
        Given we use the config "empty_folder.yaml"
        When we run "jrnl Herro"
        Then we should get an error
        Then we should see the message "is a directory, but doesn't seem to be a DayOne journal either"
