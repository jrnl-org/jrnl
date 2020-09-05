Feature: Loading a journal from a file

    Scenario: Integers in square brackets should not be read as dates
        Given we use the config "brackets.yaml"
        When we run "jrnl -1"
        Then the output should contain "[1] line starting with 1"

    Scenario: Journals with unreadable dates should still be loaded
        Given we use the config "unreadabledates.yaml"
        When we run "jrnl -2"
        Then the output should contain "I've lost track of time."
        And the output should contain "Time has no meaning."

    Scenario: Journals with readable dates AND unreadable dates should still contain all data.
        Given we use the config "mostlyreadabledates.yaml"
        When we run "jrnl -3"
        Then the output should contain "Time machines are possible."
        When we run "jrnl -1"
        Then the output should contain "I'm going to activate the machine."
        And the output should contain "I've crossed so many timelines. Is there any going back?"

