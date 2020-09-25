Feature: Encrypting and decrypting journals

    Scenario: Decrypting a journal
        Given we use the config "encrypted.yaml"
        When we run "jrnl --decrypt" and enter "bad doggie no biscuit"
        Then the config for journal "default" should have "encrypt" set to "bool:False"
        And we should see the message "Journal decrypted"
        And the journal should have 2 entries

    @todo
    Scenario: Trying to decrypt an already unencrypted journal
        # This should warn the user that the journal is already encrypted
        Given we use the config "simple.yaml"
        When we run "jrnl --decrypt"
        Then the config for journal "default" should have "encrypt" set to "bool:False"
        And the journal should have 2 entries

    @todo
    Scenario: Trying to encrypt an already encrypted journal
    # This should warn the user that the journal is already encrypted

    Scenario: Encrypting a journal
        Given we use the config "simple.yaml"
        When we run "jrnl --encrypt" and enter
            """
            swordfish
            swordfish
            n
            """
        Then we should see the message "Journal encrypted"
        And the config for journal "default" should have "encrypt" set to "bool:True"
        When we run "jrnl -n 1" and enter "swordfish"
        Then we should be prompted for a password
        And the output should contain "2013-06-10 15:40 Life is good"

