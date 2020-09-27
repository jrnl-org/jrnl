Feature: Reading and writing to journal with custom date formats

    Scenario: Dates can include a time
        # https://github.com/jrnl-org/jrnl/issues/117
        Given we use the config "simple.yaml"
        When we run "jrnl 2013-11-30 15:42: Project Started."
        Then we should see the message "Entry added"
        And the journal should contain "[2013-11-30 15:42] Project Started."

    Scenario: Dates can be in the future
        # https://github.com/jrnl-org/jrnl/issues/185
        Given we use the config "simple.yaml"
        When we run "jrnl 26/06/2099: Planet? Earth. Year? 2099."
        Then we should see the message "Entry added"
        And the journal should contain "[2099-06-26 09:00] Planet?"

    Scenario: Loading a sample journal with custom date
        Given we use the config "little_endian_dates.yaml"
        When we run "jrnl -n 2"
        Then we should get no error
        And the output should be
        """
        09.06.2013 15:39 My first entry.
        | Everything is alright

        10.07.2013 15:40 Life is good.
        | But I'm better.
        """

    Scenario Outline: Writing an entry from command line with custom date
        Given we use the config "<config>.yaml"
        When we run "jrnl <input>"
        Then we should see the message "Entry added"
        When we run "jrnl -n 1"
        Then the output should contain "<output>"

        Examples: Day-first Dates
        | config              | input                        | output                            |
        | little_endian_dates | 2020-09-19: My first entry.  | 19.09.2020 09:00 My first entry.  |
        | little_endian_dates | 2020-08-09: My second entry. | 09.08.2020 09:00 My second entry. |
        | little_endian_dates | 2020-02-29: Test.            | 29.02.2020 09:00 Test.            |
        | little_endian_dates | 2019-02-29: Test.            | 2019-02-29: Test.                 |
        | little_endian_dates | 2020-08-32: Test.            | 2020-08-32: Test.                 |
        | little_endian_dates | 2032-02-01: Test.            | 01.02.2032 09:00 Test.            |
        | little_endian_dates | 2020-01-01: Test.            | 01.01.2020 09:00 Test.            |
        | little_endian_dates | 2020-12-31: Test.            | 31.12.2020 09:00 Test.            |

    Scenario Outline: Searching for dates with custom date
        Given we use the config "<config>.yaml"
        When we run "jrnl -on '<input>' --short"
        Then the output should be "<output>"

        Examples: Day-first Dates
        | config              | input        | output                           |
        | little_endian_dates | 2013-07-10   | 10.07.2013 15:40 Life is good.   |
        | little_endian_dates | june 9 2013  | 09.06.2013 15:39 My first entry. |
        | little_endian_dates | july 10 2013 | 10.07.2013 15:40 Life is good.   |
        | little_endian_dates | june 2013    | 09.06.2013 15:39 My first entry. |
        | little_endian_dates | july 2013    | 10.07.2013 15:40 Life is good.   |
        # @todo month alone with no year should work
        # | little_endian_dates | june         | 09.06.2013 15:39 My first entry. |
        # | little_endian_dates | july         | 10.07.2013 15:40 Life is good.   |

    Scenario: Writing an entry at the prompt with custom date
        Given we use the config "little_endian_dates.yaml"
        When we run "jrnl" and enter "2013-05-10: I saw Elvis. He's alive."
        Then we should get no error
        And the journal should contain "[10.05.2013 09:00] I saw Elvis."
        And the journal should contain "He's alive."

    Scenario: Viewing today's entries does not print the entire journal
        # https://github.com/jrnl-org/jrnl/issues/741
        Given we use the config "simple.yaml"
        When we run "jrnl -on today"
        Then the output should not contain "Life is good"
        And the output should not contain "But I'm better."

    Scenario Outline: Create entry using day of the week as entry date.
        Given we use the config "simple.yaml"
        When we run "jrnl <day>: This is an entry on a <day>."
        Then we should see the message "Entry added"
        When we run "jrnl -1"
        Then the output should contain "<day> at 9am" in the local time
        And the output should contain "This is an entry on a <day>."

        Examples: Days of the week
        | day       |
        | Monday    |
        | Tuesday   |
        | Wednesday |
        | Thursday  |
        | Friday    |
        | Saturday  |
        | Sunday    |
        | sunday    |
        | sUndAy    |

    Scenario Outline: Create entry using day of the week abbreviations as entry date.
        Given we use the config "simple.yaml"
        When we run "jrnl <day>: This is an entry on a <weekday>."
        Then we should see the message "Entry added"
        When we run "jrnl -1"
        Then the output should contain "<weekday> at 9am" in the local time

        Examples: Days of the week
        | day | weekday   |
        | mon | Monday    |
        | tue | Tuesday   |
        | wed | Wednesday |
        | thu | Thursday  |
        | fri | Friday    |
        | sat | Saturday  |
        | sun | Sunday    |

    Scenario: Journals with unreadable dates should still be loaded
        Given we use the config "unreadabledates.yaml"
        When we run "jrnl -2"
        Then the output should contain "I've lost track of time."
        And the output should contain "Time has no meaning."

    Scenario: Journals with readable dates AND unreadable dates should still contain all data.
        Given we use the config "mostlyreadabledates.yaml"
        When we run "jrnl -3"
        Then the output should contain "Time machines are possible."
        Then the output should contain "I'm going to activate the machine."
        And the output should contain "I've crossed so many timelines. Is there any going back?"
        And the journal should have 3 entries

    Scenario: Update near-valid dates after journal is edited
        Given we use the config "mostlyreadabledates.yaml"
        When we run "jrnl 2222-08-19: I have made it exactly one month into the future."
        Then the journal should contain "[2019-07-01 14:23] Entry subject"

    Scenario: Integers in square brackets should not be read as dates
        Given we use the config "brackets.yaml"
        When we run "jrnl -1"
        Then the output should contain "[1] line starting with 1"

    # broken still
    @skip
    Scenario: Dayone entries without timezone information are interpreted in current timezone
        Given we use the config "dayone.yaml"
        When we run "jrnl -until 'feb 2013'"
        Then we should get no error
        And the output should contain "2013-01-17T18:37Z" in the local time

    Scenario: Loading entry with ambiguous time stamp in timezone-aware journal (like Dayone)
        #https://github.com/jrnl-org/jrnl/issues/153
        Given we use the config "bug153.yaml"
        When we run "jrnl -1"
        Then we should get no error
        And the output should be
        """
        2013-10-27 03:27 Some text.
        """
