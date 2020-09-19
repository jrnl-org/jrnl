Feature: Core functionality of jrnl outside of actually handling journals

    Scenario: Displaying the version number
        Given we use the config "basic.yaml"
        When we run "jrnl -v"
        Then we should get no error
        Then the output should contain "version"

    Scenario: --diagnostic runs without exceptions
        When we run "jrnl --diagnostic"
        Then the output should contain "jrnl"
        And the output should contain "Python"

    @todo
    Scenario: --list outputs to user without exceptions
