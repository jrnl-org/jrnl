Feature: Zapped bugs should stay dead.

    Scenario: Writing an entry does not print the entire journal
        # https://github.com/maebert/jrnl/issues/87
        Given we use the config "basic.yaml"
        When we run "jrnl 23 july 2013: A cold and stormy day. I ate crisps on the sofa."
        Then we should see the message "Entry added"
        When we run "jrnl -n 1"
        Then the output should not contain "Life is good"

    Scenario: Date with time should be parsed correctly
        # https://github.com/maebert/jrnl/issues/117
        Given we use the config "basic.yaml"
        When we run "jrnl 2013-11-30 15:42: Project Started."
        Then we should see the message "Entry added"
        and the journal should contain "[2013-11-30 15:42] Project Started."

    Scenario: Date in the future should be parsed correctly
        # https://github.com/maebert/jrnl/issues/185
        Given we use the config "basic.yaml"
        When we run "jrnl 26/06/2019: Planet? Earth. Year? 2019."
        Then we should see the message "Entry added"
        and the journal should contain "[2019-06-26 09:00] Planet?"

    Scenario: Loading entry with ambiguous time stamp
        #https://github.com/maebert/jrnl/issues/153
        Given we use the config "bug153.yaml"
        When we run "jrnl -1"
        Then we should get no error
        and the output should be
            """
            2013-10-27 03:27 Some text.
            """

    Scenario: Title with an embedded period.
        Given we use the config "basic.yaml"
        When we run "jrnl 04-24-2014: Created a new website - empty.com. Hope to get a lot of traffic."
        Then we should see the message "Entry added"
        When we run "jrnl -1"
        Then the output should be
            """
            2014-04-24 09:00 Created a new website - empty.com.
            | Hope to get a lot of traffic.
            """

    Scenario: Integers in square brackets should not be read as dates 
        Given we use the config "brackets.yaml"
        When we run "jrnl -1"
        Then the output should contain "[1] line starting with 1"

    Scenario: Journals with unreadable dates should still be viewable 
        Given we use the config "unreadabledates.yaml"
        When we run "jrnl -2"
        Then the output should contain "I've lost track of time."
        Then the output should contain "Time has no meaning."

    Scenario: Journals with readable dates AND unreadable dates should still contain all data.
        Given we use the config "mostlyreadabledates.yaml"
        When we run "jrnl -3"
        Then the output should contain "Time machines are possible."
        When we run "jrnl -1"
        Then the output should contain "I'm going to activate the machine."
        Then the output should contain "I've crossed so many timelines. Is there any going back?"

