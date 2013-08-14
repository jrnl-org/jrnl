Feature: Zapped bugs should stay dead.

    Scenario: Writing an entry does not print the entire journal
        Given we use the config "basic.json"
        When we run "jrnl 23 july 2013: A cold and stormy day. I ate crisps on the sofa."
        Then we should see the message "Entry added"
        When we run "jrnl -n 1"
        Then the output should not contain "Life is good"
