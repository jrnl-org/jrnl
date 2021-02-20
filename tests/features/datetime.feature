Feature: Reading and writing to journal with custom date formats

    Scenario: Dates can include a time
        # https://github.com/jrnl-org/jrnl/issues/117
        Given we use the config "simple.yaml"
        When we run "jrnl 2013-11-30 15:42: Project Started."
        Then we should see the message "Entry added"
        When we run "jrnl -999"
        Then the output should contain "2013-11-30 15:42 Project Started."


