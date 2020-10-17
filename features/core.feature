Feature: Functionality of jrnl outside of actually handling journals

    Scenario: Displaying the version number
        Given we use the config "simple.yaml"
        When we run "jrnl --version"
        Then we should get no error
        Then the output should match "^jrnl version v\d+\.\d+\.\d+(-(alpha|beta))?$"

    Scenario: Displaying the version number
        Given we use the config "simple.yaml"
        When we run "jrnl -v"
        Then we should get no error
        Then the output should match "^jrnl version v\d+\.\d+\.\d+(-(alpha|beta))?$"

    Scenario: Running the diagnostic command
        When we run "jrnl --diagnostic"
        Then the output should contain "jrnl"
        And the output should contain "Python"

    @todo
    Scenario: Listing available journals
