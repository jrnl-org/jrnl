Feature: Multiple journals

    Scenario: Loading a config with two journals
        Given we use the config "multiple.yaml"
        When we run "jrnl -99 --short"
        Then the output should be
            @todo something
        When we run "jrnl work -99 --short"
        Then the output should be
            @todo something

    Scenario: Write to default config by default
        Given we use the config "multiple.yaml"
        When we run "jrnl this goes to default"
        When we run "jrnl -99 --short"
        Then the output should be
            @todo something
        When we run "jrnl work -99 --short"
        Then the output should be
            @todo something

    Scenario: Write to specified journal
        Given we use the config "multiple.yaml"
        When we run "jrnl work a long day in the office"
        When we run "jrnl -99 --short"
        Then the output should be
            @todo something
        When we run "jrnl work -99 --short"
        Then the output should be
            @todo something

    Scenario: Tell user which journal was used
        Given we use the config "multiple.yaml"
        When we run "jrnl work a long day in the office"
        Then we should see the message "Entry added to work journal"

    Scenario: Write to specified journal with a timestamp
        Given we use the config "multiple.yaml"
        When we run "jrnl work 23 july 2012: a long day in the office"
        When we run "jrnl -99 --short"
        Then the output should be
            @todo something
        When we run "jrnl work -99 --short"
        Then the output should be
            @todo something

    Scenario: Write to specified journal without a timestamp but with colon
        Given we use the config "multiple.yaml"
        When we run "jrnl work : a long day in the office"
        Then the output should be
            @todo something
        When we run "jrnl work -99 --short"
        Then the output should be
            @todo something

    Scenario: Write to specified journal without a timestamp but with colon
        Given we use the config "multiple.yaml"
        When we run "jrnl work: a long day in the office"
        When we run "jrnl -99 --short"
        Then the output should be
            @todo something
        When we run "jrnl work -99 --short"
        Then the output should be
            @todo something

   Scenario: Create new journals as required
        Given we use the config "multiple.yaml"
        Then journal "ideas" should not exist
        When we run "jrnl ideas 23 july 2012: sell my junk on ebay and make lots of money"
        When we run "jrnl ideas -99 --short"
        Then the output should be
            @todo something

   Scenario: Don't crash if no default journal is specified
        Given we use the config "bug343.yaml"
        When we run "jrnl a long day in the office"
        Then the output should contain "No default journal configured"

   Scenario: Don't crash if no file exists for a configured encrypted journal
        Given we use the config "multiple.yaml"
        When we run "jrnl new_encrypted Adding first entry" and enter
            these three eyes
            these three eyes
            n
        Then the output should contain "Encrypted journal 'new_encrypted' created"
