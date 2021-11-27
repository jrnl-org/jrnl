Feature: Starring entries

    Scenario Outline: Starring an entry will mark it in the journal file
        Given we use the config "<config_file>"
        When we run "jrnl 20 july 2013 *: Best day of my life!"
        Then the output should contain "Entry added"
        When we run "jrnl -on 2013-07-20 -starred"
        Then the output should contain "2013-07-20 09:00 Best day of my life!"

        Examples: configs
        | config_file       |
        | simple.yaml       |
        | empty_folder.yaml |
        | dayone.yaml       |

    Scenario Outline: Filtering by starred entries will show only starred entries
        Given we use the config "<config_file>"
        When we run "jrnl -starred"
        Then the output should be empty
        When we run "jrnl 20 july 2013 *: Best day of my life!"
        When we run "jrnl -starred"
        Then the output should be "2013-07-20 09:00 Best day of my life!"

        Examples: configs
        | config_file       |
        | simple.yaml       |
        | empty_folder.yaml |
        | dayone_empty.yaml |

    Scenario: Starring an entry will mark it in an encrypted journal
        Given we use the config "encrypted.yaml"
        When we run "jrnl 20 july 2013 *: Best day of my life!" and enter "bad doggie no biscuit"
        Then the output should contain "Entry added"
        When we run "jrnl -on 2013-07-20 -starred" and enter "bad doggie no biscuit"
        Then the output should contain "2013-07-20 09:00 Best day of my life!"
