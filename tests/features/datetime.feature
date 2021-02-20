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
