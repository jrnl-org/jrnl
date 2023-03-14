# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

Feature: Using templates

    Scenario Outline: Template contents should be used in new entry
        Given we use the config "<config_file>"
        And we use the password "test" if prompted
        And we append to the editor if opened
            This is an addition to a templated entry
        When we run "jrnl --config-override template features/templates/basic.template"
        And we run "jrnl -1"
        Then the output should contain "This text is in the basic template"
        Then the output should contain "This is an addition to a templated entry"

        Examples: configs
        | config_file          |
        | basic_onefile.yaml   |
        | basic_encrypted.yaml |
        | basic_folder.yaml    |
        | basic_dayone.yaml    |

    Scenario Outline: Templated entry should not be saved if template is unchanged
        Given we use the config "<config_file>"
        And we use the password "test" if prompted
        When we run "jrnl --config-override template features/templates/basic.template"
        Then the output should contain "No entry to save, because the template was not changed"

        Examples: configs
        | config_file          |
        | basic_onefile.yaml   |
        | basic_encrypted.yaml |
        | basic_folder.yaml    |
        | basic_dayone.yaml    |

    Scenario Outline: --template nonexistent_file should throw an error
        Given we use the config "<config_file>"
        And we use the password "test" if prompted
        When we run "jrnl --template this_template_does_not_exist.template"
        Then we should get an error
        Then the error output should contain "Unable to find a template file based on the passed arg"

        Examples: configs
        | config_file          |
        | basic_onefile.yaml   |
        | basic_encrypted.yaml |
        | basic_folder.yaml    |
        | basic_dayone.yaml    |

    Scenario Outline: --template local_filepath should be used in new entry
        Given we use the config "<config_file>"
        And we use the password "test" if prompted
        When we run "jrnl --template features/templates/basic.template"
        Then the output should contain "No entry to save, because the template was not changed"

        Examples: configs
        | config_file          |
        | basic_onefile.yaml   |
        | basic_encrypted.yaml |
        | basic_folder.yaml    |
        | basic_dayone.yaml    |

    Scenario Outline: --template file_in_XDG_templates_dir should be used in new entry
        Given we use the config "<config_file>"
        And we use the password "test" if prompted
        And we copy the template "basic.template" to the default templates folder
        When we run "jrnl --template basic.template"
        Then the output should contain "No entry to save, because the template was not changed"


        Examples: configs
        | config_file          |
        | basic_onefile.yaml   |
        | basic_encrypted.yaml |
        | basic_folder.yaml    |
        | basic_dayone.yaml    |
        | basic_dayone.yaml    |
