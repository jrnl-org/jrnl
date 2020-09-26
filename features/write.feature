Feature: Writing new entries.

    Scenario Outline: Multiline entry with punctuation should keep title punctuation 
        Given we use the config "<config_file>.yaml"
        And we use the password "bad doggie no biscuit" if prompted
        When we run "jrnl This is. the title\\n This is the second line"
        And we run "jrnl -n 1"
        Then the output should contain "This is. the title"

        Examples: configs
        | config_file  |
        | simple       |
        | empty_folder |
        | dayone       |
        | encrypted    |

    Scenario Outline: Single line entry with period should be split at period
        Given we use the config "<config_file>.yaml"
        And we use the password "bad doggie no biscuit" if prompted
        When we run "jrnl This is. the title"
        And we run "jrnl -n 1"
        Then the output should contain "| the title"

        Examples: configs
        | config_file  |
        | simple       |
        | empty_folder |
        | dayone       |
        | encrypted    |

    Scenario Outline: Writing an entry from command line should store the entry
        Given we use the config "<config_file>.yaml"
        And we use the password "bad doggie no biscuit" if prompted
        When we run "jrnl 23 july 2013: A cold and stormy day. I ate crisps on the sofa."
        Then we should see the message "Entry added"
        When we run "jrnl -n 1"
        Then the output should contain "2013-07-23 09:00 A cold and stormy day."

        Examples: configs
        | config_file  |
        | simple       |
        | empty_folder |
        | dayone       |
        | encrypted    |

    Scenario Outline: Writing an empty entry from the editor should yield "Nothing saved to file" message
        Given we use the config "<config_file>.yaml"
        When we open the editor and enter nothing
        Then the error output should contain "[Nothing saved to file]"

        Examples: configs
        | config_file         |
        | editor              |
        | editor_empty_folder |
        | dayone              |

    @todo # this might need a new step for editors + encryption
    Scenario: Writing an empty entry from the editor in encrypted journal should yield "Nothing saved to file" message
        Given we use the config "editor_encrypted.yaml"
        #When we open the editor and enter nothing
        #Then we should see the message "[Nothing saved to file]"

    Scenario Outline: Writing an empty entry from the command line with no editor should yield nothing
        Given we use the config "<config_file>.yaml"
        When we run "jrnl" and enter nothing
        Then the output should be empty
        And the error output should contain "Writing Entry; on a blank line"
        And the editor should not have been called

        Examples: configs
        | config_file  |
        | simple        |
        | empty_folder |

    @todo # There is a problem with DayOne behave tests and console input
    Scenario: Writing an empty entry from the command line in DayOne journal

    @todo # Need some steps for encryption + editor
    Scenario: Writing an empty entry from the command line in encrypted journal

    Scenario Outline: Writing an empty entry from the editor should yield nothing
        Given we use the config "<config_file>.yaml"
        And we use the password "bad doggie no biscuit" if prompted
        When we run "jrnl" and enter nothing
        Then the output should be empty
        And the error output should contain "[Nothing saved to file]"
        And the editor should have been called

        Examples: configs
        | config_file         |
        | editor              |
        | editor_empty_folder |
        | dayone              |
        | editor_encrypted    |

    Scenario Outline: Writing an entry does not print the entire journal
        # https://github.com/jrnl-org/jrnl/issues/87
        Given we use the config "<config_file>.yaml"
        And we use the password "bad doggie no biscuit" if prompted
        When we run "jrnl 23 july 2013: A cold and stormy day. I ate crisps on the sofa."
        Then we should see the message "Entry added"
        When we run "jrnl -n 1"
        Then the output should not contain "Life is good"

        Examples: configs
        | config_file         |
        | editor              |
        | editor_empty_folder |
        | dayone              |
        | encrypted           |

    Scenario Outline: Embedded period stays in title
        Given we use the config "<config_file>.yaml"
        And we use the password "bad doggie no biscuit" if prompted
        When we run "jrnl 04-24-2014: Created a new website - empty.com. Hope to get a lot of traffic."
        Then we should see the message "Entry added"
        When we run "jrnl -1"
        Then the output should be
            """
            2014-04-24 09:00 Created a new website - empty.com.
            | Hope to get a lot of traffic.
            """

        Examples: configs
        | config_file  |
        | simple       |
        | empty_folder |
        | dayone       |
        | encrypted    |

    Scenario Outline: Write and read emoji support
        Given we use the config "<config_file>.yaml"
        And we use the password "bad doggie no biscuit" if prompted
        When we run "jrnl 23 july 2013: 🌞 sunny day. Saw an 🐘"
        Then we should see the message "Entry added"
        When we run "jrnl -n 1"
        Then the output should contain "🌞"
        And the output should contain "🐘"

        Examples: configs
        | config_file  |
        | simple       |
        | empty_folder |
        | dayone       |
        | encrypted    |

    Scenario Outline: Writing an entry at the prompt (no editor) should store the entry
        Given we use the config "<config_file>.yaml"
        And we use the password "bad doggie no biscuit" if prompted
        When we run "jrnl" and enter "25 jul 2013: I saw Elvis. He's alive."
        Then we should get no error
        When we run "jrnl -on '2013-07-25'"
        Then the output should contain "2013-07-25 09:00 I saw Elvis."
        And the output should contain "| He's alive."

        Examples: configs
        | config_file  |
        | simple       |
        | empty_folder |
        | encrypted    |

    @todo # Need to test DayOne w/out an editor
    Scenario: Writing an entry at the prompt (no editor) in DayOne journal

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
