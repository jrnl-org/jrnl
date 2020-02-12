Feature: Import jrnl file


    Scenario: Importing a jrnl file
        Given we use the config "basic.yaml"
        When we run "jrnl --import jrnl features/data/journals/tags.journal"
        Then we should see the message "[2 imported to default journal]"
