Feature: Multiple journals

    Scenario: Read a journal from an alternate config
        Given the config "basic_onefile.yaml" exists
        And we use the config "multiple.yaml"
        When we run "jrnl --cf basic_onefile.yaml -999"
        Then the output should not contain "My first entry" # from multiple.yaml
        And the output should contain "Lorem ipsum" # from basic_onefile.yaml

    Scenario: Write to default journal by default using an alternate config
        Given the config "multiple.yaml" exists
        And we use the config "basic_onefile.yaml"
        When we run "jrnl --cf multiple.yaml this goes to default"
        And we run "jrnl -1"
        Then the output should not contain "this goes to default"
        When we run "jrnl --cf multiple.yaml -1"
        Then the output should contain "this goes to default"

    Scenario: Write to specified journal using an alternate config
        Given the config "multiple.yaml" exists
        And we use the config "basic_onefile.yaml"
        When we run "jrnl work --cf multiple.yaml a long day in the office"
        And we run "jrnl default --cf multiple.yaml -1"
        Then the output should contain "But I'm better"
        When we run "jrnl work --cf multiple.yaml -1"
        Then the output should contain "a long day in the office"

    Scenario: Tell user which journal was used while using an alternate config
        Given the config "multiple.yaml" exists
        And we use the config "basic_onefile.yaml"
        When we run "jrnl --cf multiple.yaml work a long day in the office"
        Then we should see the message "Entry added to work journal"

    Scenario: Write to specified journal with a timestamp using an alternate config
        Given the config "multiple.yaml" exists
        And we use the config "basic_onefile.yaml"
        When we run "jrnl work --cf multiple.yaml 23 july 2012: a long day in the office"
        And we run "jrnl --cf multiple.yaml -1"
        Then the output should contain "But I'm better"
        When we run "jrnl --cf multiple.yaml work -1"
        Then the output should contain "a long day in the office"
        And the output should contain "2012-07-23"

    Scenario: Write to specified journal without a timestamp but with colon using an alternate config
        Given the config "multiple.yaml" exists
        And we use the config "basic_onefile.yaml"
        When we run "jrnl work --cf multiple.yaml : a long day in the office"
        And we run "jrnl --cf multiple.yaml -1"
        Then the output should contain "But I'm better"
        When we run "jrnl --cf multiple.yaml work -1"
        Then the output should contain "a long day in the office"

    Scenario: Create new journals as required using an alternate config
        Given the config "multiple.yaml" exists
        And we use the config "basic_onefile.yaml"
        When we run "jrnl ideas -1"
        Then the output should be empty
        When we run "jrnl ideas --cf multiple.yaml 23 july 2012: sell my junk on ebay and make lots of money"
        Then the output should contain "Journal 'ideas' created"
        When we run "jrnl ideas --cf multiple.yaml -1"
        Then the output should contain "sell my junk on ebay and make lots of money"

    Scenario: Don't crash if no default journal is specified using an alternate config
        Given the config "bug343.yaml" exists
        And we use the config "basic_onefile.yaml"
        When we run "jrnl --cf bug343.yaml a long day in the office"
        Then we should see the message "No default journal configured"

    Scenario: Don't crash if no file exists for a configured encrypted journal using an alternate config
        Given the config "multiple.yaml" exists
        And we use the config "basic_onefile.yaml"
        When we run "jrnl new_encrypted --cf multiple.yaml Adding first entry" and enter
            these three eyes
            these three eyes
            n
        Then we should see the message "Encrypted journal 'new_encrypted' created"

    Scenario: Don't overwrite main config when encrypting a journal in an alternate config
        Given the config "basic_onefile.yaml" exists
        And we use the config "multiple.yaml"
        When we run "jrnl --cf basic_onefile.yaml --encrypt" and enter
            these three eyes
            these three eyes
            n
        Then we should see the message "Journal encrypted to features/journals/basic_onefile.journal"
        And the config should contain "encrypt: false" # multiple.yaml remains unchanged

    Scenario: Don't overwrite main config when decrypting a journal in an alternate config
        Given the config "editor_encrypted.yaml" exists
        And we use the config "basic_encrypted.yaml"
        When we run "jrnl --cf editor_encrypted.yaml --decrypt"
        Then the config should contain "encrypt: true" # basic_encrypted remains unchanged
