Feature: Tests that don't fit anywhere else

    Scenario: Opening an folder that's not a DayOne folder should treat as folder journal
        Given we use the config "empty_folder.yaml"
        When we run "jrnl 23 july 2013: Testing folder journal."
        Then we should see the message "Entry added"
        When we run "jrnl -1"
        Then the output should be "2013-07-23 09:00 Testing folder journal."

    Scenario: Loading a sample journal
        Given we use the config "basic.yaml"
        When we run "jrnl -2"
        Then we should get no error
        And the output should be
            """
            2013-06-09 15:39 My first entry.
            | Everything is alright

            2013-06-10 15:40 Life is good.
            | But I'm better.
            """

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
