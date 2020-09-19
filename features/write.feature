Feature: Writing new entries.

    Scenario: Multiline entry with punctuation
        Given we use the config "basic.yaml"
        When we run "jrnl This is. the title\\n This is the second line"
        And we run "jrnl -n 1"
        Then the output should contain "This is. the title"

    Scenario: Single line entry with punctuation
        Given we use the config "basic.yaml"
        When we run "jrnl This is. the title"
        And we run "jrnl -n 1"
        Then the output should contain "| the title"

    Scenario: Writing an entry from command line
        Given we use the config "basic.yaml"
        When we run "jrnl 23 july 2013: A cold and stormy day. I ate crisps on the sofa."
        Then we should see the message "Entry added"
        When we run "jrnl -n 1"
        Then the output should contain "2013-07-23 09:00 A cold and stormy day."

    Scenario: Writing an empty entry from the editor
        Given we use the config "editor.yaml"
        When we open the editor and enter nothing
        Then we should see the message "[Nothing saved to file]"

    Scenario: Writing an empty entry from the command line
        Given we use the config "basic.yaml"
        When we run "jrnl" and enter nothing
        Then the output should be empty
        And the editor should not have been called

    Scenario: Writing an empty entry from the editor
        Given we use the config "editor.yaml"
        When we run "jrnl" and enter nothing
        Then the output should be empty
        And the editor should have been called

    Scenario: Writing an entry does not print the entire journal
        # https://github.com/jrnl-org/jrnl/issues/87
        Given we use the config "basic.yaml"
        When we run "jrnl 23 july 2013: A cold and stormy day. I ate crisps on the sofa."
        Then we should see the message "Entry added"
        When we run "jrnl -n 1"
        Then the output should not contain "Life is good"

    Scenario: Title with an embedded period
        Given we use the config "basic.yaml"
        When we run "jrnl 04-24-2014: Created a new website - empty.com. Hope to get a lot of traffic."
        Then we should see the message "Entry added"
        When we run "jrnl -1"
        Then the output should be
            """
            2014-04-24 09:00 Created a new website - empty.com.
            | Hope to get a lot of traffic.
            """

    Scenario: Emoji support
        Given we use the config "basic.yaml"
        When we run "jrnl 23 july 2013: 🌞 sunny day. Saw an 🐘"
        Then we should see the message "Entry added"
        When we run "jrnl -n 1"
        Then the output should contain "🌞"
        And the output should contain "🐘"

    Scenario: Writing an entry at the prompt (no editor)
        Given we use the config "basic.yaml"
        When we run "jrnl" and enter "25 jul 2013: I saw Elvis. He's alive."
        Then we should get no error
        And the journal should contain "[2013-07-25 09:00] I saw Elvis."
        And the journal should contain "He's alive."

    Scenario: Writing into Dayone
        Given we use the config "dayone.yaml"
        When we run "jrnl 01 may 1979: Being born hurts."
        And we run "jrnl -until 1980"
        Then the output should be "1979-05-01 09:00 Being born hurts."

    Scenario: Writing into Dayone adds extended metadata
        Given we use the config "dayone.yaml"
        When we run "jrnl 01 may 1979: Being born hurts."
        And we run "jrnl --export json"
        Then "entries" in the json output should have 5 elements
        And the json output should contain entries.0.creator.software_agent
        And the json output should contain entries.0.creator.os_agent
        And the json output should contain entries.0.creator.host_name
        And the json output should contain entries.0.creator.generation_date
        And the json output should contain entries.0.creator.device_agent
        And "entries.0.creator.software_agent" in the json output should contain "jrnl"

    # fails when system time is UTC (as on Travis-CI)
    @skip
    Scenario: Title with an embedded period on DayOne journal
        Given we use the config "dayone.yaml"
        When we run "jrnl 04-24-2014: "Ran 6.2 miles today in 1:02:03. I'm feeling sore because I forgot to stretch.""
        Then we should see the message "Entry added"
        When we run "jrnl -1"
        Then the output should be
            """
            2014-04-24 09:00 Ran 6.2 miles today in 1:02:03.
            | I'm feeling sore because I forgot to stretch.
            """

    Scenario: Opening an folder that's not a DayOne folder should treat as folder journal
        Given we use the config "empty_folder.yaml"
        When we run "jrnl 23 july 2013: Testing folder journal."
        Then we should see the message "Entry added"
        When we run "jrnl -1"
        Then the output should be "2013-07-23 09:00 Testing folder journal."
