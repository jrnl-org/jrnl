Feature: Functionality of jrnl outside of actually handling journals

    Scenario: Displaying the version number
        Given we use the config "simple.yaml"
        When we run "jrnl --version"
        Then we should get no error
        Then the output should match "^jrnl version v\d+\.\d+(\.\d+)?(-(alpha|beta)\d*)?"

    Scenario: Displaying the version number
        Given we use the config "simple.yaml"
        When we run "jrnl -v"
        Then we should get no error
        Then the output should match "^jrnl version v\d+\.\d+(\.\d+)?(-(alpha|beta)\d*)?"

    Scenario: Running the diagnostic command
        When we run "jrnl --diagnostic"
        Then the output should contain "jrnl"
        And the output should contain "Python"

    Scenario Outline: List plugin names in --version 
        Given We use the config "basic_onefile.yaml"
        When We run "jrnl --version"
        Then the output should contain pyproject.toml version
        And The output should contain "<plugin_name> : <version> from jrnl.plugins.exporter.<plugin_source>_exporter" 
        Examples:
            | plugin_name | plugin_source | version |
            | md  | markdown | v2.7.2-beta  |
            | testing | testing | v0.0.1 | 

    @todo
    Scenario: Listing available journals
