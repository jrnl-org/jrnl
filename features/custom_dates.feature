Feature: Reading and writing to journal with custom date formats

    Scenario: Loading a sample journal
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

    Scenario: Writing an entry from command line
        Given we use the config "little_endian_dates.yaml"
        When we run "jrnl 2013-07-12: A cold and stormy day. I ate crisps on the sofa."
        Then we should see the message "Entry added"
        When we run "jrnl -n 1"
        Then the output should contain "12.07.2013 09:00 A cold and stormy day."

    Scenario: Filtering for dates
        Given we use the config "little_endian_dates.yaml"
        When we run "jrnl -on 2013-06-10 --short"
        Then the output should be "10.06.2013 15:40 Life is good."
        When we run "jrnl -on 'june 6 2013' --short"
        Then the output should be "10.06.2013 15:40 Life is good."

    Scenario: Writing an entry at the prompt
        Given we use the config "little_endian_dates.yaml"
        When we run "jrnl" and enter
        """
        2013-05-10: I saw Elvis. He's alive.
        """
        Then we should get no error
        And the journal should contain "[10.05.2013 09:00] I saw Elvis."
        And the journal should contain "He's alive."