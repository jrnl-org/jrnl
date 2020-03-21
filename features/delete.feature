Feature: Delete entries from journal

    Scenario: --delete flag allows deletion of single entry
        Given we use the config "deletion.yaml"
        When we run "jrnl -n 1"
        Then the output should contain
        """
        2019-10-29 11:13 Third entry.
        """
        When we run "jrnl --delete" and enter
        """
        N
        N
        Y
        """
        When we run "jrnl -n 1"
        Then the output should contain
        """
        2019-10-29 11:11 Second entry.
        """
