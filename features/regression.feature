Feature: Zapped bugs should stay dead.

    Scenario: Writing an entry does not print the entire journal
        # https://github.com/maebert/jrnl/issues/87
        Given we use the config "basic.json"
        When we run "jrnl 23 july 2013: A cold and stormy day. I ate crisps on the sofa."
        Then we should see the message "Entry added"
        When we run "jrnl -n 1"
        Then the output should not contain "Life is good"

    Scenario: Opening an folder that's not a DayOne folder gives a nice error message
        Given we use the config "empty_folder.json"
        When we run "jrnl Herro"
        Then we should get an error
        Then we should see the message "is a directory, but doesn't seem to be a DayOne journal either"
