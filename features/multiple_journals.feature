Feature: Multiple journals

    Scenario: Loading a config with two journals
        Given we use the config "multiple.yaml"
        Then journal "default" should have 2 entries
        and journal "work" should have 0 entries

    Scenario: Write to default config by default
        Given we use the config "multiple.yaml"
        When we run "jrnl this goes to default"
        Then journal "default" should have 3 entries
        and journal "work" should have 0 entries

    Scenario: Write to specified journal
        Given we use the config "multiple.yaml"
        When we run "jrnl work a long day in the office"
        Then journal "default" should have 2 entries
        and journal "work" should have 1 entry

    Scenario: Tell user which journal was used
        Given we use the config "multiple.yaml"
        When we run "jrnl work a long day in the office"
        Then we should see the message "Entry added to work journal"

    Scenario: Write to specified journal with a timestamp
        Given we use the config "multiple.yaml"
        When we run "jrnl work 23 july 2012: a long day in the office"
        Then journal "default" should have 2 entries
        and journal "work" should have 1 entry
        and journal "work" should contain "2012-07-23"

   Scenario: Create new journals as required
        Given we use the config "multiple.yaml"
        Then journal "ideas" should not exist
        When we run "jrnl ideas 23 july 2012: sell my junk on ebay and make lots of money"
        Then journal "ideas" should have 1 entry

   Scenario: Don't crash if no default journal is specified
        Given we use the config "bug343.yaml"
        When we run "jrnl a long day in the office"
        Then we should see the message "No default journal configured"
