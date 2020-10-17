Feature: Journals iteracting with the file system in a way that users can see

    Scenario: Adding entries to a Folder journal should generate date files
        Given we use the config "empty_folder.yaml"
        When we run "jrnl 23 July 2013: Testing folder journal."
        Then we should see the message "Entry added"
        When the journal directory is listed
        Then the output should contain "2013/07/23.txt" or "2013\07\23.txt"

    Scenario: Adding multiple entries to a Folder journal should generate multiple date files
        Given we use the config "empty_folder.yaml"
        When we run "jrnl 23 July 2013: Testing folder journal."
        And we run "jrnl 3/7/2014: Second entry of journal."
        Then we should see the message "Entry added"
        When the journal directory is listed
        Then the output should contain "2013/07/23.txt" or "2013\07\23.txt"
        Then the output should contain "2014/03/07.txt" or "2014\03\07.txt"

    Scenario: If the journal and its parent directory don't exist, they should be created
        Given we use the config "missing_directory.yaml"
        Then the journal should not exist
        When we run "jrnl This is a new entry in my journal"
        Then the journal should exist
        When we run "jrnl -n 1"
        Then the output should contain "This is a new entry in my journal"
        And the journal should have 1 entry

    Scenario: If the journal file doesn't exist, then it should be created
        Given we use the config "missing_journal.yaml"
        Then the journal should not exist
        When we run "jrnl This is a new entry in my journal"
        Then the journal should exist
        When we run "jrnl -n 1"
        Then the output should contain "This is a new entry in my journal"
        And the journal should have 1 entry

    Scenario: Creating journal with relative path should update to absolute path
        Given we use the config "missingconfig"
        When we run "jrnl hello world" and enter
        """
        test.txt
        n
        """
        And we change directory to "features"
        And we run "jrnl -n 1"
        Then the output should contain "hello world"
