Feature: Multiple journals

    Scenario: Loading an alternate config with two journals 
        Given we use the config "basic_onefile.yaml"
        Given we use the config "multiple.yaml" # Repeating step to ensure both are copied
        When we run "jrnl --cf basic_onefile.yaml -999"
        Then the output should not contain "My first entry" # from multiple.yaml
        And the output should contain "Lorem ipsum" # from basic_onefile.yaml

    # This test is breaking because multiple.yaml is "upgrading" and overwriting basic_onefile.yaml in the process
    # Backup your personal config before manually reproducing this! It will replace
    # your config file with the upgraded form of multiple.yaml (which is the bug)
    Scenario: Write to default journal by default using an alternate config
        Given we use the config "multiple.yaml"
        Given we use the config "basic_onefile.yaml"
        When we run "jrnl --cf multiple.yaml this goes to default"
        Given we use the config "basic_onefile.yaml"
        When we run "jrnl -1"
        Then the output should not contain "this goes to default"
        When we run "jrnl --cf multiple.yaml -1"
        Then the output should contain "this goes to default"

   # # The rest of these tests haven't changed except for the given steps. Each needs
   # # to be re-worked
   #  Scenario: Write to specified journal using an alternate config
   #      Given we use the config "multiple.yaml"
   #      Given we use the config "basic_onefile.yaml"
   #      When we run "jrnl work --cf features/data/configs/alternate.yaml a long day in the office"
   #      Then journal "default" should have 2 entries
   #      And journal "work" should have 1 entry

   #  Scenario: Tell user which journal was used using an alternate config
   #      Given we use the config "multiple.yaml"
   #      Given we use the config "basic_onefile.yaml"
   #      When we run "jrnl --cf features/data/configs/alternate.yaml work a long day in the office"
   #      Then we should see the message "Entry added to work journal"

   #  Scenario: Write to specified journal with a timestamp using an alternate config
   #      Given we use the config "multiple.yaml"
   #      Given we use the config "basic_onefile.yaml"
   #      When we run "jrnl work --cf features/data/configs/alternate.yaml 23 july 2012: a long day in the office"
   #      Then journal "default" should have 2 entries
   #      And journal "work" should have 1 entry
   #      And journal "work" should contain "2012-07-23"

   #  Scenario: Write to specified journal without a timestamp but with colon using an alternate config
   #      Given we use the config "multiple.yaml"
   #      Given we use the config "basic_onefile.yaml"
   #      When we run "jrnl work --cf features/data/configs/alternate.yaml : a long day in the office"
   #      Then journal "default" should have 2 entries
   #      And journal "work" should have 1 entry
   #      And journal "work" should contain "a long day in the office"

   # Scenario: Create new journals as required using an alternate config
   #      Given we use the config "multiple.yaml"
   #      Given we use the config "basic_onefile.yaml"
   #      Then journal "ideas" should not exist
   #      When we run "jrnl ideas --cf features/data/configs/alternate.yaml 23 july 2012: sell my junk on ebay and make lots of money"
   #      Then journal "ideas" should have 1 entry

   # Scenario: Don't crash if no default journal is specified using an alternate config
   #      Given we use the config "multiple.yaml"
   #      Given we use the config "basic_onefile.yaml"
   #      When we run "jrnl --cf features/data/configs/bug343.yaml a long day in the office"
   #      Then we should see the message "No default journal configured"

   # Scenario: Don't crash if no file exists for a configured encrypted journal using an alternate config
   #      Given we use the config "multiple.yaml"
   #      Given we use the config "basic_onefile.yaml"
   #      When we run "jrnl new_encrypted --cf features/data/configs/alternate.yaml Adding first entry" and enter
   #      """
   #      these three eyes
   #      these three eyes
   #      n
   #      """
   #      Then we should see the message "Encrypted journal 'new_encrypted' created"

