# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

Feature: Starring entries

    Scenario Outline: Starring an entry will mark it in the journal file
        Given we use the config "<config_file>"
        When we run "jrnl 20 july 2013 *: Best day of my life!"
        Then we should get no error
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
        And we use the password "bad doggie no biscuit" if prompted
        When we run "jrnl 20 july 2013 *: Best day of my life!"
        Then we should get no error
        When we run "jrnl -on 2013-07-20 -starred" and enter "bad doggie no biscuit"
        Then the output should contain "2013-07-20 09:00 Best day of my life!"
