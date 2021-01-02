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

    Scenario: Encrypt journal with no keyring backend and do not store in keyring
        Given we use the config "simple.yaml"
        And we do not have a keyring
        When we run "jrnl test entry"
        And we run "jrnl --encrypt" and enter
        """
        password
        password
        n
        """
        Then we should get no error
        And we should not see the message "Failed to retrieve keyring"

    Scenario: Encrypt journal with no keyring backend and do store in keyring
        Given we use the config "simple.yaml"
        And we do not have a keyring
        When we run "jrnl test entry"
        And we run "jrnl --encrypt" and enter
        """
        password
        password
        y
        """
        Then we should get no error
        And we should not see the message "Failed to retrieve keyring"
        # @todo add step to check contents of keyring

    @todo
    Scenario: Open an encrypted journal with wrong password in keyring
    # This should ask the user for the password after the keyring fails

    @todo
    Scenario: Decrypt journal with password in keyring

    @todo
    Scenario: Decrypt journal without a keyring

    Scenario: Encrypt journal when keyring exists but fails
        Given we use the config "simple.yaml"
        And we have a failed keyring
        When we run "jrnl --encrypt" and enter
        """
        karimpwnz
        karimpwnz
        y
        """
        Then we should see the message "Failed to retrieve keyring" 
        And we should get no error
        And we should be prompted for a password
        And the config for journal "default" should have "encrypt" set to "bool:True"

    Scenario: Decrypt journal when keyring exists but fails
        Given we use the config "encrypted.yaml"
        And we have a failed keyring
        When we run "jrnl --decrypt" and enter "bad doggie no biscuit"
        Then we should see the message "Failed to retrieve keyring"
        And we should get no error
        And we should be prompted for a password
        And we should see the message "Journal decrypted"
        And the config for journal "default" should have "encrypt" set to "bool:False"
        And the journal should have 2 entries

    Scenario: Open encrypted journal when keyring exists but fails
    # This should ask the user for the password after the keyring fails
        Given we use the config "encrypted.yaml"
        And we have a failed keyring
        When we run "jrnl -n 1" and enter "bad doggie no biscuit"
        Then we should see the message "Failed to retrieve keyring"
        And we should get no error 
        And we should be prompted for a password
        And the output should contain "2013-06-10 15:40 Life is good"

    Scenario: Mistyping your password
        Given we use the config "simple.yaml"
        When we run "jrnl --encrypt" and enter
        """
        swordfish
        sordfish
        """
        Then we should be prompted for a password
        And we should see the message "Passwords did not match"
        And the config for journal "default" should not have "encrypt" set
        And the journal should have 2 entries

    Scenario: Mistyping your password, then getting it right
        Given we use the config "simple.yaml"
        When we run "jrnl --encrypt" and enter
        """
        swordfish
        sordfish
        swordfish
        swordfish
        n
        """
        Then we should be prompted for a password
        And we should see the message "Passwords did not match"
        And we should see the message "Journal encrypted"
        And the config for journal "default" should have "encrypt" set to "bool:True"
        When we run "jrnl -n 1" and enter "swordfish"
        Then we should be prompted for a password
        And the output should contain "2013-06-10 15:40 Life is good"
