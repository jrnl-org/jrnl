Feature: Loading the default journal type

    Scenario: Loading a sample journal
        Given we use the config "basic.yaml"
        When we run "jrnl -2"
        Then we should get no error
        And the output should be
            """
            2013-06-09 15:39 My first entry.
            | Everything is alright

            2013-06-10 15:40 Life is good.
            | But I'm better.
            """

    Scenario: Printing a journal that has multiline entries
        Given we use the config "multiline.yaml"
        When we run "jrnl -n 1"
        Then we should get no error
        And the output should be
            """
            2013-06-09 15:39 Multiple line entry.
            | This is the first line.
            | This line doesn't have any ending punctuation
            |
            | There is a blank line above this.
            """

    Scenario: Integers in square brackets should not be read as dates
        Given we use the config "brackets.yaml"
        When we run "jrnl -1"
        Then the output should contain "[1] line starting with 1"


    Scenario: If the journal and it's parent directory don't exist, they should be created
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
