Feature: Delete entries from journal
    Scenario Outline: Delete flag allows deletion of single entry
        Given we use the config "<config>.yaml"
        Then the journal should have 3 entries
        When we run "jrnl -n 1"
        Then the output should contain "2019-10-29 11:13 Third entry."
        When we run "jrnl --delete" and enter
            """
            N
            N
            Y
            """
        Then the journal should have 2 entries
        When we run "jrnl -n 1"
        Then the output should contain "2019-10-29 11:11 Second entry."

        Examples: Configs
        | config       |
        | deletion     |
        | empty_folder |
        | dayone_empty |

    Scenario: Backing out of interactive delete does not change journal
        Given we use the config "deletion.yaml"
        Then the journal should have 3 entries
        When we run "jrnl --delete -n 1" and enter
            """
            N
            """
        Then the journal should have 3 entries
        And the journal should contain "[2019-10-29 11:11] First entry."
        And the journal should contain "[2019-10-29 11:11] Second entry."
        And the journal should contain "[2019-10-29 11:13] Third entry."

    Scenario: Delete flag with nonsense input deletes nothing (issue #932)
        Given we use the config "deletion.yaml"
        Then the journal should have 3 entries
        When we run "jrnl --delete asdfasdf"
        Then the journal should have 3 entries
        When we run "jrnl -n 1"
        Then the output should contain "2019-10-29 11:13 Third entry."

    Scenario: Delete flag with tag only deletes tagged entries
        Given we use the config "deletion_filters.yaml"
        Then the journal should have 5 entries
        When we run "jrnl --delete @holidays" and enter
            """
            Y
            Y
            """
        Then the journal should have 3 entries
        And the journal should contain "[2019-10-01 08:00] It's just another day in October."
        And the journal should contain "[2020-03-01 08:00] It's just another day in March."
        And the journal should contain "[2020-05-02 12:10] Writing tests."

    Scenario: Delete flag with multiple tags deletes all entries matching any of the tags
        Given we use the config "deletion_filters.yaml"
        Then the journal should have 5 entries
        When we run "jrnl --delete @holidays @springtime" and enter
            """
            Y
            Y
            Y
            """
        Then the journal should have 2 entries
        And the journal should contain "[2019-10-01 08:00] It's just another day in October."
        And the journal should contain "[2020-03-01 08:00] It's just another day in March."
        But the journal should not contain "[2020-01-01 08:00] Happy New Year!"
        But the journal should not contain "[2020-05-01 09:00] Happy May Day!"
        But the journal should not contain "[2020-05-02 12:10] Writing tests. *"

    Scenario: Delete flag with -and deletes boolean AND of tagged entries
        Given we use the config "deletion_filters.yaml"
        Then the journal should have 5 entries
        When we run "jrnl --delete -and @holidays @springtime" and enter
            """
            Y
            """
        Then the journal should have 4 entries
        And the journal should contain "[2019-10-01 08:00] It's just another day in October."
        And the journal should contain "[2020-01-01 08:00] Happy New Year!"
        And the journal should contain "[2020-03-01 08:00] It's just another day in March."
        And the journal should contain "[2020-05-02 12:10] Writing tests. *"
        But the journal should not contain "[2020-05-01 09:00] Happy May Day!"

    Scenario: Delete flag with -not does not delete entries from given tag
        Given we use the config "deletion_filters.yaml"
        Then the journal should have 5 entries
        When we run "jrnl --delete @holidays -not @springtime" and enter
            """
            Y
            """
        Then the journal should have 4 entries
        And the journal should contain "[2019-10-01 08:00] It's just another day in October."
        And the journal should contain "[2020-03-01 08:00] It's just another day in March."
        And the journal should contain "[2020-05-01 09:00] Happy May Day!"
        And the journal should contain "[2020-05-02 12:10] Writing tests. *"
        But the journal should not contain "[2020-01-01 08:00] Happy New Year!"

    Scenario: Delete flag with -from search operator only deletes entries since that date
        Given we use the config "deletion_filters.yaml"
        Then the journal should have 5 entries
        When we run "jrnl --delete -from 2020-01-02" and enter
            """
            Y
            Y
            Y
            """
        Then the journal should have 2 entries
        And the journal should contain "[2019-10-01 08:00] It's just another day in October."
        And the journal should contain "[2020-01-01 08:00] Happy New Year!"
        And the journal should not contain "[2020-03-01 08:00] It's just another day in March."
        And the journal should not contain "[2020-05-01 09:00] Happy May Day!"
        And the journal should not contain "[2020-05-02 12:10] Writing tests."

    Scenario: Delete flag with -to only deletes entries up to specified date
        Given we use the config "deletion_filters.yaml"
        Then the journal should have 5 entries
        When we run "jrnl --delete -to 2020-01-02" and enter
            """
            Y
            Y
            """
        Then the journal should have 3 entries
        And the journal should contain "[2020-03-01 08:00] It's just another day in March."
        And the journal should contain "[2020-05-01 09:00] Happy May Day!"
        And the journal should contain "[2020-05-02 12:10] Writing tests."
        But the journal should not contain "[2019-10-01 08:00] It's just another day in October."
        But the journal should not contain "[2020-01-01 08:00] Happy New Year!"

    Scenario: Delete flag with -starred only deletes starred entries
        Given we use the config "deletion_filters.yaml"
        Then the journal should have 5 entries
        When we run "jrnl --delete -starred" and enter
            """
            Y
            """
        Then the journal should have 4 entries
        And the journal should contain "[2019-10-01 08:00] It's just another day in October."
        And the journal should contain "[2020-01-01 08:00] Happy New Year!"
        And the journal should contain "[2020-03-01 08:00] It's just another day in March."
        And the journal should contain "[2020-05-01 09:00] Happy May Day!"
        But the journal should not contain "[2020-05-02 12:10] Writing tests. *"

    Scenario: Delete flag with -contains only entries containing expression
        Given we use the config "deletion_filters.yaml"
        Then the journal should have 5 entries
        When we run "jrnl --delete -contains happy" and enter
            """
            Y
            Y
            """
        Then the journal should have 3 entries
        And the journal should contain "[2019-10-01 08:00] It's just another day in October."
        And the journal should contain "[2020-03-01 08:00] It's just another day in March."
        And the journal should contain "[2020-05-02 12:10] Writing tests. *"
        But the journal should not contain "[2020-01-01 08:00] Happy New Year!"
        But the journal should not contain "[2020-05-01 09:00] Happy May Day!"
