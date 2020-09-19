Feature: Writing new entries.

    Scenario Outline: Multiline entry with punctuation
        Given we use the config <config_file>
        When we run "jrnl This is. the title\\n This is the second line"
        And we run "jrnl -n 1"
        Then the output should contain "This is. the title"

        Examples: configs
        | config_file         |
        | "basic.yaml"        |
        | "empty_folder.yaml" |
        | "dayone.yaml"       |

    Scenario: Multiline entry with punctuation in encrypted journal
        Given we use the config "encrypted.yaml"
        When we run "jrnl This is. the title\\n This is the second line" and enter "bad doggie no biscuit"
        And we run "jrnl -n 1" and enter "bad doggie no biscuit"
        Then the output should contain "This is. the title"

    Scenario Outline: Single line entry with punctuation
        Given we use the config <config_file>
        When we run "jrnl This is. the title"
        And we run "jrnl -n 1"
        Then the output should contain "| the title"

        Examples: configs
        | config_file         |
        | "basic.yaml"        |
        | "empty_folder.yaml" |
        | "dayone.yaml"       |

    Scenario: Single line entry with punctuation in encrypted journal
        Given we use the config "encrypted.yaml"
        When we run "jrnl This is. the title" and enter "bad doggie no biscuit"
        And we run "jrnl -n 1" and enter "bad doggie no biscuit"
        Then the output should contain "| the title"

    Scenario Outline: Writing an entry from command line
        Given we use the config <config_file>
        When we run "jrnl 23 july 2013: A cold and stormy day. I ate crisps on the sofa."
        Then we should see the message "Entry added"
        When we run "jrnl -n 1"
        Then the output should contain "2013-07-23 09:00 A cold and stormy day."

        Examples: configs
        | config_file         |
        | "basic.yaml"        |
        | "empty_folder.yaml" |
        | "dayone.yaml"       |

    Scenario: Writing an entry from command line in encrypted journal
        Given we use the config "encrypted.yaml"
        When we run "jrnl 23 july 2013: A cold and stormy day. I ate crisps on the sofa." and enter "bad doggie no biscuit"
        Then we should see the message "Entry added"
        When we run "jrnl -n 1" and enter "bad doggie no biscuit"
        Then the output should contain "2013-07-23 09:00 A cold and stormy day."

    Scenario Outline: Writing an empty entry from the editor
        Given we use the config <config_file>
        When we open the editor and enter nothing
        Then we should see the message "[Nothing saved to file]"

        Examples: configs
        | config_file                |
        | "editor.yaml"              |
        | "editor_empty_folder.yaml" |
        | "dayone.yaml"              |

    @todo # this might need a new step for editors + encryption
    Scenario: Writing an empty entry from the editor in encrypted journal
        Given we use the config "editor_encrypted.yaml"
        #When we open the editor and enter nothing
        #Then we should see the message "[Nothing saved to file]"

    Scenario: Writing an empty entry from the command line
        Given we use the config "basic.yaml"
        When we run "jrnl" and enter nothing
        Then the output should be empty
        And the editor should not have been called

    @todo # There is a problem with DayOne behave tests and console input
    Scenario: Writing an empty entry from the command line in DayOne journal

    Scenario: Writing an empty entry from the command line in folder journal
        Given we use the config "empty_folder.yaml"
        When we run "jrnl" and enter nothing
        Then the output should be empty
        And the editor should not have been called

    @todo # Need some steps for encryption + editor
    Scenario: Writing an empty entry from the command line in encrypted journal

    Scenario Outline: Writing an empty entry from the editor
        Given we use the config <config_file>
        When we run "jrnl" and enter nothing
        Then the output should be empty
        And the editor should have been called

        Examples: configs
        | config_file                |
        | "editor.yaml"              |
        | "editor_empty_folder.yaml" |
        | "dayone.yaml"              |

    Scenario: Writing an empty entry from the editor in encrypted journal
        Given we use the config "editor_encrypted.yaml"
        When we run "jrnl" and enter "bad doggie no biscuit"
        Then the editor should have been called

    Scenario Outline: Writing an entry does not print the entire journal
        # https://github.com/jrnl-org/jrnl/issues/87
        Given we use the config <config_file>
        When we run "jrnl 23 july 2013: A cold and stormy day. I ate crisps on the sofa."
        Then we should see the message "Entry added"
        When we run "jrnl -n 1"
        Then the output should not contain "Life is good"

        Examples: configs
        | config_file         |
        | "basic.yaml"        |
        | "empty_folder.yaml" |
        | "dayone.yaml"       |

    Scenario: Writing an entry in encrypted journal does not print the entire journal
        Given we use the config "encrypted.yaml"
        When we run "jrnl 23 july 2013: A cold and stormy day. I ate crisps on the sofa." and enter "bad doggie no biscuit"
        Then we should see the message "Entry added"
        When we run "jrnl -n 1" and enter "bad doggie no biscuit"
        Then the output should not contain "Life is good"

    Scenario Outline: Embedded period stays in title
        Given we use the config <config_file>
        When we run "jrnl 04-24-2014: Created a new website - empty.com. Hope to get a lot of traffic."
        Then we should see the message "Entry added"
        When we run "jrnl -1"
        Then the output should be
            """
            2014-04-24 09:00 Created a new website - empty.com.
            | Hope to get a lot of traffic.
            """

        Examples: configs
        | config_file         |
        | "basic.yaml"        |
        | "empty_folder.yaml" |
        | "dayone.yaml"       |

    Scenario: Embedded period stays in title in encrypted journal
        Given we use the config "encrypted.yaml"
        When we run "jrnl 04-24-2014: Created a new website - empty.com. Hope to get a lot of traffic." and enter "bad doggie no biscuit"
        Then we should see the message "Entry added"
        When we run "jrnl -1" and enter "bad doggie no biscuit"
        Then the output should contain
            """
            2014-04-24 09:00 Created a new website - empty.com.
            | Hope to get a lot of traffic.
            """

    Scenario Outline: Write and read emoji support
        Given we use the config <config_file>
        When we run "jrnl 23 july 2013: 🌞 sunny day. Saw an 🐘"
        Then we should see the message "Entry added"
        When we run "jrnl -n 1"
        Then the output should contain "🌞"
        And the output should contain "🐘"

        Examples: configs
        | config_file         |
        | "basic.yaml"        |
        | "empty_folder.yaml" |
        | "dayone.yaml"       |

    Scenario: Write and read emoji support in encrypted journal
        Given we use the config "encrypted.yaml"
        When we run "jrnl 23 july 2013: 🌞 sunny day. Saw an 🐘" and enter "bad doggie no biscuit"
        Then we should see the message "Entry added"
        When we run "jrnl -n 1" and enter "bad doggie no biscuit"
        Then the output should contain "🌞"
        And the output should contain "🐘"

    Scenario: Writing an entry at the prompt (no editor)
        Given we use the config "basic.yaml"
        When we run "jrnl" and enter "25 jul 2013: I saw Elvis. He's alive."
        Then we should get no error
        And the journal should contain "[2013-07-25 09:00] I saw Elvis."
        And the journal should contain "He's alive."

    Scenario: Writing an entry at the prompt (no editor) in folder journal
        Given we use the config "empty_folder.yaml"
        When we run "jrnl" and enter "25 jul 2013: I saw Elvis. He's alive."
        Then we should get no error
        When we run "jrnl -on '2013-07-25'"
        Then the output should contain "2013-07-25 09:00 I saw Elvis."
        And the output should contain "| He's alive."

    @todo # Need to test DayOne w/out an editor
    Scenario: Writing an entry at the prompt (no editor) in DayOne journal

    Scenario: Writing an entry at the prompt (no editor) in encrypted journal
        Given we use the config "encrypted.yaml"
        When we run "jrnl" and enter
            """
            bad doggie no biscuit
            25 jul 2013: I saw Elvis. He's alive.
            """
        Then we should get no error
        When we run "jrnl -on '2013-07-25'" and enter "bad doggie no biscuit"
        Then the output should contain "2013-07-25 09:00 I saw Elvis."
        And the output should contain "| He's alive."

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
