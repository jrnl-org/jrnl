Feature: Multiple journals

    Scenario: Loading an alternate config with two journals 
        Given we use the config "multiple.yaml"
        When we run "jrnl --cf features/data/configs/alternate.yaml"
        Then journal "default" should have 2 entries
        And journal "work" should have 0 entries

    Scenario: Write to default journal by default using an alternate config
        Given we use the config "multiple.yaml"
        When we run "jrnl --cf features/data/configs/alternate.yaml this goes to default"
        Then journal "default" should have 3 entries
        And journal "work" should have 0 entries

    Scenario: Write to specified journal using an alternate config
        Given we use the config "multiple.yaml"
        When we run "jrnl work --cf features/data/configs/alternate.yaml a long day in the office"
        Then journal "default" should have 2 entries
        And journal "work" should have 1 entry

    Scenario: Tell user which journal was used using an alternate config
        Given we use the config "multiple.yaml"
        When we run "jrnl --cf features/data/configs/alternate.yaml work a long day in the office"
        Then we should see the message "Entry added to work journal"

    Scenario: Write to specified journal with a timestamp using an alternate config
        Given we use the config "multiple.yaml"
        When we run "jrnl work --cf features/data/configs/alternate.yaml 23 july 2012: a long day in the office"
        Then journal "default" should have 2 entries
        And journal "work" should have 1 entry
        And journal "work" should contain "2012-07-23"

    Scenario: Write to specified journal without a timestamp but with colon using an alternate config
        Given we use the config "multiple.yaml"
        When we run "jrnl work --cf features/data/configs/alternate.yaml : a long day in the office"
        Then journal "default" should have 2 entries
        And journal "work" should have 1 entry
        And journal "work" should contain "a long day in the office"

   Scenario: Create new journals as required using an alternate config
        Given we use the config "multiple.yaml"
        Then journal "ideas" should not exist
        When we run "jrnl ideas --cf features/data/configs/alternate.yaml 23 july 2012: sell my junk on ebay and make lots of money"
        Then journal "ideas" should have 1 entry

   Scenario: Don't crash if no default journal is specified using an alternate config
        Given we use the config "multiple.yaml"
        When we run "jrnl --cf features/data/configs/bug343.yaml a long day in the office"
        Then we should see the message "No default journal configured"

   Scenario: Don't crash if no file exists for a configured encrypted journal using an alternate config
        Given we use the config "multiple.yaml"
        When we run "jrnl new_encrypted --cf features/data/configs/alternate.yaml Adding first entry" and enter
        """
        these three eyes
        these three eyes
        n
        """
        Then we should see the message "Encrypted journal 'new_encrypted' created"

