# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

Feature: Preventing concurrent processes from clobbering each other's changes

    Scenario: Writing to a journal that's locked by another process fails fast
        Given we use the config "basic_onefile.yaml"
        And the "default" journal is locked by another process
        When we run "jrnl This is a new entry"
        Then we should get an error
        And the error output should contain "currently locked"

    Scenario: Editing a journal that's locked by another process fails fast
        Given we use the config "basic_onefile.yaml"
        And the "default" journal is locked by another process
        When we run "jrnl -n 1 --edit"
        Then we should get an error
        And the error output should contain "currently locked"

    Scenario: Searching a journal that's locked by another process still works
        Given we use the config "basic_onefile.yaml"
        And the "default" journal is locked by another process
        When we run "jrnl -n 1"
        Then we should get no error
        And the error output should not contain "currently locked"
