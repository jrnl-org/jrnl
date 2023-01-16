# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

Feature: Using templates

    Scenario Outline: Template contents should be used in new entry
        Given we use the config "<config_file>"
        And we use the password "test" if prompted
        When we run "jrnl --config-override template features/templates/basic.template"
        And we run "jrnl -1"
        Then the output should contain "This text is in the basic template"

        Examples: configs
        | config_file          |
        | basic_onefile.yaml   |
        | basic_encrypted.yaml |
        | basic_folder.yaml    |
        | basic_dayone.yaml    |

