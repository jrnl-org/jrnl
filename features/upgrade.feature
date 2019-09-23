Feature: Upgrading Journals from 1.x.x to 2.x.x

    Scenario: Upgrade and parse journals with square brackets
        Given we use the config "upgrade_from_195.json"
        When we run "jrnl -9" and enter "Y"
        Then the output should contain
            """
            2010-06-10 15:00 A life without chocolate is like a bad analogy.

            2013-06-10 15:40 He said "[this] is the best time to be alive".
            """
        Then the journal should have 2 entries

    Scenario: Upgrading a journal encrypted with jrnl 1.x
        Given we use the config "encrypted_old.json"
        When we run "jrnl -n 1" and enter 
            """
            Y
            bad doggie no biscuit
            bad doggie no biscuit
            """
        Then we should see the message "Password"
        and the output should contain "2013-06-10 15:40 Life is good"
