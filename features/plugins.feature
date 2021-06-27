Feature: Functionality of Importer and Exporter Plugins

    @skip_no_external_plugins
    Scenario Outline: List buildin plugin names in --version 
        Given We use the config "basic_onefile.yaml"
        When We run "jrnl --version"
        Then the output should contain pyproject.toml version
        And the output should contain "<plugin_name> : <version> from jrnl.<source>.<type>.<filename>" 
        And the output should not contain ".contrib."

        Examples:
            | plugin_name | version                  | source  | type     | filename |
            | jrnl        | <pyproject.toml version> | plugins | importer | jrnl     |
            | boxed       | <pyproject.toml version> | plugins | exporter | fancy    |
            | dates       | <pyproject.toml version> | plugins | exporter | dates    |
            | default     | <pyproject.toml version> | plugins | exporter | pretty   |
            | fancy       | <pyproject.toml version> | plugins | exporter | fancy    |
            | json        | <pyproject.toml version> | plugins | exporter | json     |
            | markdown    | <pyproject.toml version> | plugins | exporter | markdown |
            | md          | <pyproject.toml version> | plugins | exporter | markdown |
            | pretty      | <pyproject.toml version> | plugins | exporter | pretty   |
            | short       | <pyproject.toml version> | plugins | exporter | short    |
            | tags        | <pyproject.toml version> | plugins | exporter | tag      |
            | text        | <pyproject.toml version> | plugins | exporter | text     |
            | txt         | <pyproject.toml version> | plugins | exporter | text     |
            | xml         | <pyproject.toml version> | plugins | exporter | xml      |
            | yaml        | <pyproject.toml version> | plugins | exporter | yaml     |

    @skip_only_with_external_plugins
    Scenario Outline: List external plugin names in --version 
        Given We use the config "basic_onefile.yaml"
        When We run "jrnl --version"
        Then the output should contain pyproject.toml version
        And the output should contain "<plugin_name> : <version> from jrnl.<source>.<type>.<filename>"

        Examples:
            | plugin_name | version                  | source  | type     | filename    |
            | jrnl        | <pyproject.toml version> | plugins | importer | jrnl        |
            | json        | v1.0.0                   | contrib | importer | simple_json |
            | boxed       | <pyproject.toml version> | plugins | exporter | fancy       |
            | dates       | <pyproject.toml version> | plugins | exporter | dates       |
            | default     | <pyproject.toml version> | plugins | exporter | pretty      |
            | fancy       | <pyproject.toml version> | plugins | exporter | fancy       |
            | json        | v1.0.0                   | contrib | exporter | custom_json |
            | markdown    | <pyproject.toml version> | plugins | exporter | markdown    |
            | md          | <pyproject.toml version> | plugins | exporter | markdown    |
            | pretty      | <pyproject.toml version> | plugins | exporter | pretty      |
            | rot13       | v1.0.0                   | contrib | exporter | rot13       |
            | short       | <pyproject.toml version> | plugins | exporter | short       |
            | tags        | <pyproject.toml version> | plugins | exporter | tag         |
            | testing     | v0.0.1                   | contrib | exporter | flag        |
            | text        | <pyproject.toml version> | plugins | exporter | text        |
            | txt         | v1.0.0                   | contrib | exporter | rot13       |
            | xml         | <pyproject.toml version> | plugins | exporter | xml         |
            | yaml        | <pyproject.toml version> | plugins | exporter | yaml        |
        
    @skip_only_with_external_plugins
    Scenario Outline: Do not list overridden plugin names in --version 
        Given We use the config "basic_onefile.yaml"
        When We run "jrnl --version"
        Then the output should contain pyproject.toml version
        And the output should not contain "<plugin_name> : <version> from jrnl.<source>.<type>.<filename>"

        Examples:
            | plugin_name | version                  | source  | type     | filename |
            | json        | <pyproject.toml version> | plugins | exporter | json     |
            | txt         | <pyproject.toml version> | plugins | exporter | text     |

    @skip_only_with_external_plugins
    Scenario Outline: Custom JSON Import
        Given we use the config "simple.yaml"
        When we run "jrnl --import ./features/data/simple_import.json"
        Then the journal should contain "My first entry."
        And the journal should contain "Life is good."

    @skip_only_with_external_plugins
    Scenario Outline: Custom JSON Export
        Given we use the config "<config>.yaml"
        And we use the password "test" if prompted
        When we run "jrnl --format json"
        Then we should get no error
        And the output should be parsable as json
        And "entries" in the json output should have 3 elements
        And entry 1 should not have an array "tags"
        And entry 2 should not have an array "tags"
        And entry 3 should not have an array "tags"

        Examples: configs
            | config          |
            | basic_onefile   |
            | basic_encrypted |
            | basic_folder    |
            | basic_dayone    |
