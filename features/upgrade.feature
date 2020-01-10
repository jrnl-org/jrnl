Feature: Upgrading Journals from 1.x.x to 2.x.x

    @skip_win
    Scenario: Upgrade and parse journals with square brackets
        Given we use the config "upgrade_from_195.json"
        When we run "jrnl -9" and enter "Y"
        Then the output should contain
            """
            2010-06-10 15:00 A life without chocolate is like a bad analogy.

            2013-06-10 15:40 He said "[this] is the best time to be alive".
            """
        Then the journal should have 2 entries

    @skip_win
    Scenario: Upgrading a journal encrypted with jrnl 1.x
        Given we use the config "encrypted_old.json"
        When we run "jrnl -n 1" and enter
            """
            Y
            bad doggie no biscuit
            bad doggie no biscuit
            """
        Then the output should contain "Password"
        and the output should contain "2013-06-10 15:40 Life is good"

    @skip_win
    Scenario: Upgrade and parse journals with little endian date format
        Given we use the config "upgrade_from_195_little_endian_dates.json"
        When we run "jrnl -9" and enter "Y"
        Then the output should contain
            """
            10.06.2010 15:00 A life without chocolate is like a bad analogy.

            10.06.2013 15:40 He said "[this] is the best time to be alive".
            """
        Then the journal should have 2 entries

    @skip_win
    Scenario: Successful upgrade with missing journal
        Given we use the config "upgrade_from_195_with_missing_journal.json"
        When we run "jrnl -ls" and enter "Y Y"
        Then we should see the message "Journal 'missing' created"
        Then we should see the message "We're all done here"

    @skip_win
    Scenario: Aborted upgrade with missing journal
        Given we use the config "upgrade_from_195_with_missing_journal.json"
        When we run "jrnl -ls" and enter "Y N"
        Then we should see the message "jrnl NOT upgraded, exiting."