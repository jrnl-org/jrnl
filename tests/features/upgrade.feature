Feature: Upgrading Journals from 1.x.x to 2.x.x

    Scenario: Upgrade and parse journals with square brackets
        Given we use the config "upgrade_from_195.json"
        When we run "jrnl -9" and enter "Y"
        Then the journal should have 2 entries
        And the output should contain
        """
        2010-06-10 15:00 A life without chocolate is like a bad analogy.
        """
        And the output should contain
        """
        2013-06-10 15:40 He said "[this] is the best time to be alive".
        """

    Scenario: Upgrading a journal encrypted with jrnl 1.x
        Given we use the config "encrypted_old.json"
        When we run "jrnl -n 1" and enter
        """
        Y
        bad doggie no biscuit
        bad doggie no biscuit
        """
        Then we should be prompted for a password
        And the output should contain "2013-06-10 15:40 Life is good"

    Scenario: Upgrading a config without colors to colors
        Given we use the config "no_colors.yaml"
        When we run "jrnl -n 1"
        Then the config should have "colors" set to
        """
        {
            'date':'none',
            'title':'none',
            'body':'none',
            'tags':'none'
        }
        """

    Scenario: Upgrade and parse journals with little endian date format
        Given we use the config "upgrade_from_195_little_endian_dates.json"
        When we run "jrnl -9" and enter "Y"
        Then the journal should have 2 entries
        And the output should contain
        """
        10.06.2010 15:00 A life without chocolate is like a bad analogy.
        """
        And the output should contain
        """
        10.06.2013 15:40 He said "[this] is the best time to be alive".
        """

    Scenario: Upgrade with missing journal
        Given we use the config "upgrade_from_195_with_missing_journal.json"
        When we run "jrnl -ls" and enter
        """"
        Y
        """
        Then the output should contain "Error: features/journals/missing.journal does not exist."
        And we should get no error

    Scenario: Upgrade with missing encrypted journal
        Given we use the config "upgrade_from_195_with_missing_encrypted_journal.json"
        When we run "jrnl -ls" and enter
        """
        Y
        bad doggie no biscuit
        """
        Then the output should contain "Error: features/journals/missing.journal does not exist."
        And the error output should contain "We're all done"
        And we should get no error
