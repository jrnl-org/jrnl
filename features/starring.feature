Feature: Starring entries

    Scenario: Starring an entry will mark it in the journal file
        Given we use the config "basic.yaml"
        When we run "jrnl 20 july 2013 *: Best day of my life!"
        Then we should see the message "Entry added"
        and the journal should contain "[2013-07-20 09:00] Best day of my life! *"

    Scenario: Filtering by starred entries
        Given we use the config "basic.yaml"
        When we run "jrnl -starred"
        Then the output should be
            """
            """
        When we run "jrnl 20 july 2013 *: Best day of my life!"
        When we run "jrnl -starred"
        Then the output should be
            """
            2013-07-20 09:00 Best day of my life!
            """
