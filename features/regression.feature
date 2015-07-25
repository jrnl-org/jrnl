Feature: Zapped bugs should stay dead.

    Scenario: Writing an entry does not print the entire journal
        # https://github.com/maebert/jrnl/issues/87
        Given we use the config "basic.yaml"
        When we run "jrnl 23 july 2013: A cold and stormy day. I ate crisps on the sofa."
        Then we should see the message "Entry added"
        When we run "jrnl -n 1"
        Then the output should not contain "Life is good"

    Scenario: Opening an folder that's not a DayOne folder gives a nice error message
        Given we use the config "empty_folder.yaml"
        When we run "jrnl Herro"
        Then we should get an error
        Then we should see the message "is a directory, but doesn't seem to be a DayOne journal either"

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

	Scenario: Upgrade and parse journals with square brackets
		Given we use the config "upgrade_from_195.json"
		When we run "jrnl -2" and enter "Y"
		Then the output should contain
            """
            2010-06-10 15:00 A life without chocolate is like a bad analogy.

            2013-06-10 15:40 He said "[this] is the best time to be alive".
            """

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

    Scenario: DayOne tag searching should work with tags containing a mixture of upper and lower case.
        # https://github.com/maebert/jrnl/issues/354
        Given we use the config "dayone.yaml"
        When we run "jrnl @plAy"
        Then the output should contain
            """
            2013-05-17 11:39 This entry has tags!
            """
