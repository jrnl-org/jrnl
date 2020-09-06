Feature: Core functionality of jrnl outside of actually handling journals

    Scenario: Displaying the version number
        Given we use the config "basic.yaml"
        When we run "jrnl -v"
        Then we should get no error
        Then the output should contain "version"

    Scenario: --short displays the short version of entries (only the title)
        Given we use the config "basic.yaml"
        When we run "jrnl -on 2013-06-10 --short"
        Then the output should be "2013-06-10 15:40 Life is good."

    Scenario: -s displays the short version of entries (only the title)
        Given we use the config "basic.yaml"
        When we run "jrnl -on 2013-06-10 -s"
        Then the output should be "2013-06-10 15:40 Life is good."

    Scenario: Installation with relative journal and referencing from another folder
        Given we use the config "missingconfig"
        When we run "jrnl hello world" and enter
            """
            test.txt
            n
            """
        And we change directory to "features"
        And we run "jrnl -n 1"
        Then the output should contain "hello world"

    Scenario: --diagnostic runs without exceptions
        When we run "jrnl --diagnostic"
        Then the output should contain "jrnl"
        And the output should contain "Python"

