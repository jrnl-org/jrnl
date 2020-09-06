Feature: Using the installed keyring

    Scenario: Storing a password in keyring
        Given we use the config "multiple.yaml"
        And we have a keyring
        When we run "jrnl simple --encrypt" and enter
            """
            sabertooth
            sabertooth
            y
            """
        Then the config for journal "simple" should have "encrypt" set to "bool:True"
        When we run "jrnl simple -n 1"
        Then the output should contain "2013-06-10 15:40 Life is good"
        But the output should not contain "Password"

    Scenario: Encrypt journal with no keyring backend and do not store in keyring
        Given we use the config "basic.yaml"
        And we do not have a keyring
        When we run "jrnl test entry"
        And we run "jrnl --encrypt" and enter
            """
            password
            password
            n
            """
        Then we should get no error

    Scenario: Encrypt journal with no keyring backend and do store in keyring
        Given we use the config "basic.yaml"
        And we do not have a keyring
        When we run "jrnl test entry"
        And we run "jrnl --encrypt" and enter
            """
            password
            password
            y
            """
        Then we should get no error

    @todo
    Scenario: Open an encrypted journal with wrong password in keyring
    # This should ask the user for the password after the keyring fails

    @todo
    Scenario: Open encrypted journal when keyring exists but fails
    # This should ask the user for the password after the keyring fails
