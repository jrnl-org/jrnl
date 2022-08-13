# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

Feature: Functionality of jrnl outside of actually handling journals

    Scenario: Displaying the version number
        Given we use the config "simple.yaml"
        When we run "jrnl --version"
        Then we should get no error
        Then the output should match "^jrnl v\d+\.\d+(\.\d+)?(-(alpha|beta)\d*)?"

    Scenario: Running the diagnostic command
        Given we use the config "simple.yaml"
        When we run "jrnl --diagnostic"
        Then the output should contain "jrnl"
        And the output should contain "Python"
        And the output should contain "OS"

    @todo
    Scenario: Listing available journals

