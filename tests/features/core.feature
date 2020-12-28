Feature: Functionality of jrnl outside of actually handling journals

    Scenario: Displaying the version number
        Given we use the config "simple.yaml"
        When we run "jrnl --version"
        Then we should get no error
        Then the output should match "^jrnl version v\d+\.\d+(\.\d+)?(-(alpha|beta)\d*)?"
