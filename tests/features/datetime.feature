Feature: Reading and writing to journal with custom date formats

    Scenario: Dates can include a time
        # https://github.com/jrnl-org/jrnl/issues/117
        Given we use the config "simple.yaml"
        When we run "jrnl 2013-11-30 15:42: Project Started."
        Then we should see the message "Entry added"
        When we run "jrnl -999"
        Then the output should contain "2013-11-30 15:42 Project Started."


    Scenario: Dates can be in the future
        # https://github.com/jrnl-org/jrnl/issues/185
        Given we use the config "simple.yaml"
        When we run "jrnl 26/06/2099: Planet? Earth. Year? 2099."
        Then we should see the message "Entry added"
        When we run "jrnl -999"
        Then the output should contain "2099-06-26 09:00 Planet?"


    Scenario: Loading a sample journal with custom date
        Given we use the config "little_endian_dates.yaml"
        When we run "jrnl -n 2"
        Then we should get no error
        When we run "jrnl -n 999"
        Then the output should be
            09.06.2013 15:39 My first entry.
            | Everything is alright

            10.07.2013 15:40 Life is good.
            | But I'm better.


    Scenario Outline: Writing an entry from command line with custom date
        Given we use the config "<config_file>"
        When we run "jrnl <command>"
        Then we should see the message "Entry added"
        When we run "jrnl -n 1"
        Then the output should contain "<output>"

        Examples: Day-first Dates
        | config_file              | command                      | output                            |
        | little_endian_dates.yaml | 2020-09-19: My first entry.  | 19.09.2020 09:00 My first entry.  |
        | little_endian_dates.yaml | 2020-08-09: My second entry. | 09.08.2020 09:00 My second entry. |
        | little_endian_dates.yaml | 2020-02-29: Test.            | 29.02.2020 09:00 Test.            |
        | little_endian_dates.yaml | 2019-02-29: Test.            | 2019-02-29: Test.                 |
        | little_endian_dates.yaml | 2020-08-32: Test.            | 2020-08-32: Test.                 |
        | little_endian_dates.yaml | 2032-02-01: Test.            | 01.02.2032 09:00 Test.            |
        | little_endian_dates.yaml | 2020-01-01: Test.            | 01.01.2020 09:00 Test.            |
        | little_endian_dates.yaml | 2020-12-31: Test.            | 31.12.2020 09:00 Test.            |


    Scenario Outline: Searching for dates with custom date
        Given we use the config "<config_file>"
        When we run "jrnl <command>"
        Then the output should be "<output>"

        Examples: Day-first Dates
        | config_file              | command                    | output                           |
        | little_endian_dates.yaml | -on '2013-07-10' --short   | 10.07.2013 15:40 Life is good.   |
        | little_endian_dates.yaml | -on 'june 9 2013' --short  | 09.06.2013 15:39 My first entry. |
        | little_endian_dates.yaml | -on 'july 10 2013' --short | 10.07.2013 15:40 Life is good.   |
        | little_endian_dates.yaml | -on 'june 2013' --short    | 09.06.2013 15:39 My first entry. |
        | little_endian_dates.yaml | -on 'july 2013' --short    | 10.07.2013 15:40 Life is good.   |
        # @todo month alone with no year should work
        # | little_endian_dates.yaml | -on 'june' --short         | 09.06.2013 15:39 My first entry. |
        # | little_endian_dates.yaml | -on 'july' --short         | 10.07.2013 15:40 Life is good.   |


    Scenario: Writing an entry at the prompt with custom date
        Given we use the config "little_endian_dates.yaml"
        When we run "jrnl" and enter "2013-05-10: I saw Elvis. He's alive."
        Then we should get no error
        When we run "jrnl -999"
        Then the output should contain "10.05.2013 09:00 I saw Elvis."
        And the output should contain "He's alive."


    Scenario: Viewing today's entries does not print the entire journal
        # see: https://github.com/jrnl-org/jrnl/issues/741
        Given we use the config "simple.yaml"
        When we run "jrnl -on today"
        Then the output should not contain "Life is good"
        And the output should not contain "But I'm better."


    Scenario Outline: Create entry using day of the week as entry date.
        Given we use the config "simple.yaml"
        When we run "jrnl <command>"
        Then we should see the message "Entry added"
        When we run "jrnl -1"
        Then the output should contain "<output>"
        Then the output should contain the date "<date>"

        Examples: Days of the week
        | command                         | output               | date             |
        | Monday: entry on a monday       | entry on a monday    | monday at 9am    |
        | Tuesday: entry on a tuesday     | entry on a tuesday   | tuesday at 9am   |
        | Wednesday: entry on a wednesday | entry on a wednesday | wednesday at 9am |
        | Thursday: entry on a thursday   | entry on a thursday  | thursday at 9am  |
        | Friday: entry on a friday       | entry on a friday    | friday at 9am    |
        | Saturday: entry on a saturday   | entry on a saturday  | saturday at 9am  |
        | Sunday: entry on a sunday       | entry on a sunday    | sunday at 9am    |
        | sunday: entry on a sunday       | entry on a sunday    | sunday at 9am    |
        | sUndAy: entry on a sunday       | entry on a sunday    | sunday at 9am    |


    Scenario Outline: Create entry using day of the week as entry date.
        Given we use the config "simple.yaml"
        When we run "jrnl <command>"
        Then we should see the message "Entry added"
        When we run "jrnl -1"
        Then the output should contain "<output>"
        Then the output should contain the date "<date>"

        Examples: Days of the week
        | command                   | output               | date             |
        | Mon: entry on a monday    | entry on a monday    | monday at 9am    |
        | Tue: entry on a tuesday   | entry on a tuesday   | tuesday at 9am   |
        | Wed: entry on a wednesday | entry on a wednesday | wednesday at 9am |
        | Thu: entry on a thursday  | entry on a thursday  | thursday at 9am  |
        | Fri: entry on a friday    | entry on a friday    | friday at 9am    |
        | Sat: entry on a saturday  | entry on a saturday  | saturday at 9am  |
        | Sun: entry on a sunday    | entry on a sunday    | sunday at 9am    |
        | sun: entry on a sunday    | entry on a sunday    | sunday at 9am    |
        | sUn: entry on a sunday    | entry on a sunday    | sunday at 9am    |


    Scenario: Journals with unreadable dates should still be loaded
        Given we use the config "unreadabledates.yaml"
        When we run "jrnl -2"
        Then the output should contain "I've lost track of time."
        And the output should contain "Time has no meaning."


    Scenario: Journals with readable dates AND unreadable dates should still contain all data.
        Given we use the config "mostlyreadabledates.yaml"
        When we run "jrnl --short"
        Then the output should be
            2019-07-01 14:23 The third entry
            2019-07-18 14:23 The first entry
            2019-07-19 14:23 The second entry


    Scenario: Update near-valid dates after journal is edited
        Given we use the config "mostlyreadabledates.yaml"
        When we run "jrnl 2222-08-19: I have made it exactly one month into the future."
        When we run "jrnl -2"
        Then the output should contain "2019-07-19 14:23 The second entry"


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
            2013-10-27 03:27 Some text.
