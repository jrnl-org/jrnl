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


