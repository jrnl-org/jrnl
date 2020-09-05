Feature: Searching a journal

    Scenario: Displaying entries using -on today should display entries created today.
        Given we use the config "basic.yaml"
        When we run "jrnl today: Adding an entry right now."
        Then we should see the message "Entry added"
        When we run "jrnl -on today"
        Then the output should contain "Adding an entry right now."

    Scenario: Displaying entries using -from day should display correct entries
        Given we use the config "basic.yaml"
        When we run "jrnl yesterday: This thing happened yesterday"
        Then we should see the message "Entry added"
        When we run "jrnl today at 11:59pm: Adding an entry right now."
        Then we should see the message "Entry added"
        When we run "jrnl tomorrow: A future entry."
        Then we should see the message "Entry added"
        When we run "jrnl -from today"
        Then the output should contain "Adding an entry right now."
        And the output should contain "A future entry."
        And the output should not contain "This thing happened yesterday"

    Scenario: Displaying entries using -from and -to day should display correct entries
        Given we use the config "basic.yaml"
        When we run "jrnl yesterday: This thing happened yesterday"
        Then we should see the message "Entry added"
        When we run "jrnl today at 11:59pm: Adding an entry right now."
        Then we should see the message "Entry added"
        When we run "jrnl tomorrow: A future entry."
        Then we should see the message "Entry added"
        When we run "jrnl -from yesterday -to today"
        Then the output should contain "This thing happened yesterday"
        And the output should contain "Adding an entry right now."
        And the output should not contain "A future entry."
