Feature: Reading and writing to journal with custom date formats

    Scenario: Dates with time
        # https://github.com/jrnl-org/jrnl/issues/117
        Given we use the config "basic.yaml"
        When we run "jrnl 2013-11-30 15:42: Project Started."
        Then we should see the message "Entry added"
        And the journal should contain "[2013-11-30 15:42] Project Started."

    Scenario: Dates in the future
        # https://github.com/jrnl-org/jrnl/issues/185
        Given we use the config "basic.yaml"
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

            10.06.2013 15:40 Life is good.
            | But I'm better.
            """

    Scenario: Writing an entry from command line with custom date
        Given we use the config "little_endian_dates.yaml"
        When we run "jrnl 2013-07-12: A cold and stormy day. I ate crisps on the sofa."
        Then we should see the message "Entry added"
        When we run "jrnl -n 1"
        Then the output should contain "12.07.2013 09:00 A cold and stormy day."

    Scenario: Filtering for dates with custom date
        Given we use the config "little_endian_dates.yaml"
        When we run "jrnl -on 2013-06-10 --short"
        Then the output should be "10.06.2013 15:40 Life is good."
        When we run "jrnl -on 'june 6 2013' --short"
        Then the output should be "10.06.2013 15:40 Life is good."

    Scenario: Writing an entry at the prompt with custom date
        Given we use the config "little_endian_dates.yaml"
        When we run "jrnl" and enter "2013-05-10: I saw Elvis. He's alive."
        Then we should get no error
        And the journal should contain "[10.05.2013 09:00] I saw Elvis."
        And the journal should contain "He's alive."

    Scenario: Viewing today's entries does not print the entire journal
        # https://github.com/jrnl-org/jrnl/issues/741
        Given we use the config "basic.yaml"
        When we run "jrnl -on today"
        Then the output should not contain "Life is good"
        And the output should not contain "But I'm better."

    Scenario: Create entry using day of the week as entry date.
        Given we use the config "basic.yaml"
        When we run "jrnl monday: This is an entry on a Monday."
        Then we should see the message "Entry added"
        When we run "jrnl -1"
        Then the output should contain "monday at 9am" in the local time
        And the output should contain "This is an entry on a Monday."

    Scenario: Create entry using day of the week abbreviations as entry date.
        Given we use the config "basic.yaml"
        When we run "jrnl fri: This is an entry on a Friday."
        Then we should see the message "Entry added"
        When we run "jrnl -1"
        Then the output should contain "friday at 9am" in the local time

