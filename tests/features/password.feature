Feature: Using the installed keyring

    Scenario: Storing a password in keyring
        Given we use the config "multiple.yaml"
        And we have a keyring
        When we run "jrnl simple --encrypt" and enter
            sabertooth
            sabertooth
            Y
        Then the config for journal "simple" should have "encrypt" set to "bool:True"
        When we run "jrnl simple -n 1"
        Then the output should contain "2013-06-10 15:40 Life is good"


    Scenario: Encrypt journal with no keyring backend and do not store in keyring
        Given we use the config "simple.yaml"
        When we run "jrnl test entry"
        And we run "jrnl --encrypt" and enter
            password
            password
            n
        Then we should get no error
        And the output should not contain "Failed to retrieve keyring"

