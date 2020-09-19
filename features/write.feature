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
