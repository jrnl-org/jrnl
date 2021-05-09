Feature: Functionality of Importer and Exporter Plugins

    @skip_no_external_plugins
    Scenario Outline: List buildin plugin names in --version 
        Given We use the config "basic_onefile.yaml"
        When We run "jrnl --version"
        Then the output should contain pyproject.toml version
        And The output should contain "<plugin_name> : <version> from jrnl.<source>.<type>.<filename>" 
        And the output should not contain ".contrib."

        Examples:
            | plugin_name | version     | source  | type     | filename |
            | jrnl        | v2.8.1      | plugins | importer | jrnl     |
            | boxed       | v2.8.1      | plugins | exporter | fancy    |
            | dates       | v2.8.1      | plugins | exporter | dates    |
            | default     | v2.8.1      | plugins | exporter | pretty   |
            | fancy       | v2.8.1      | plugins | exporter | fancy    |
            | json        | v2.8.1      | plugins | exporter | json     |
            | markdown    | v2.8.1      | plugins | exporter | markdown |
            | md          | v2.8.1      | plugins | exporter | markdown |
            | pretty      | v2.8.1      | plugins | exporter | pretty   |
            | short       | v2.8.1      | plugins | exporter | short    |
            | tags        | v2.8.1      | plugins | exporter | tag      |
            | text        | v2.8.1      | plugins | exporter | text     |
            | txt         | v2.8.1      | plugins | exporter | text     |
            | xml         | v2.8.1      | plugins | exporter | xml      |
            | yaml        | v2.8.1      | plugins | exporter | yaml     |

    @skip_only_with_external_plugins
    Scenario Outline: List external plugin names in --version 
        Given We use the config "basic_onefile.yaml"
        When We run "jrnl --version"
        Then the output should contain pyproject.toml version
        And The output should contain "<plugin_name> : <version> from jrnl.<source>.<type>.<filename>" 
        Examples:
            | plugin_name | version     | source  | type     | filename |
            | jrnl        | v2.8.1      | plugins | importer | jrnl     |
            | json        | v1.0.0      | contrib | importer | json     |
            | boxed       | v2.8.1      | plugins | exporter | fancy    |
            | dates       | v2.8.1      | plugins | exporter | dates    |
            | default     | v2.8.1      | plugins | exporter | pretty   |
            | fancy       | v2.8.1      | plugins | exporter | fancy    |
            | json        | v1.0.0      | contrib | exporter | json     |
            | markdown    | v2.8.1      | plugins | exporter | markdown |
            | md          | v2.8.1      | plugins | exporter | markdown |
            | pretty      | v2.8.1      | plugins | exporter | pretty   |
            | rot13       | v1.0.0      | contrib | exporter | rot13    |
            | short       | v2.8.1      | plugins | exporter | short    |
            | tags        | v2.8.1      | plugins | exporter | tag      |
            | testing     | v0.0.1      | contrib | exporter | testing  |
            | text        | v2.8.1      | plugins | exporter | text     |
            | txt         | v1.0.0      | contrib | exporter | rot13    |
            | xml         | v2.8.1      | plugins | exporter | xml      |
            | yaml        | v2.8.1      | plugins | exporter | yaml     |
        
    @skip_only_with_external_plugins
    Scenario Outline: Do not list overridden plugin names in --version 
        Given We use the config "basic_onefile.yaml"
        When We run "jrnl --version"
        Then the output should contain pyproject.toml version
        And the output should not contain "<plugin_name> : <version> from jrnl.<source>.<type>.<filename>"

        Examples:
            | plugin_name | version     | source  | type     | filename |
            | json        | v2.8.1      | plugins | exporter | json     |
            | txt         | v2.8.1      | plugins | exporter | text     |
