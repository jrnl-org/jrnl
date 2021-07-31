Feature: Encrypting and decrypting journals

    Scenario: Decrypting a journal
        Given we use the config "encrypted.yaml"
        When we run "jrnl --decrypt" and enter "bad doggie no biscuit"
        Then we should see the message "Journal decrypted"
        And the config for journal "default" should contain "encrypt: false"
        When we run "jrnl -99 --short"
        Then the output should be
            2013-06-09 15:39 My first entry.
            2013-06-10 15:40 Life is good.


    @todo
    Scenario: Trying to decrypt an already unencrypted journal
        # This should warn the user that the journal is already encrypted
        Given we use the config "simple.yaml"
        When we run "jrnl --decrypt"
        Then the config for journal "default" should contain "encrypt: false"
        When we run "jrnl -99 --short"
        Then the output should be
            2013-06-09 15:39 My first entry.
            2013-06-10 15:40 Life is good.


    @todo
    Scenario: Trying to encrypt an already encrypted journal
    # This should warn the user that the journal is already encrypted


    Scenario: Encrypting a journal
        Given we use the config "simple.yaml"
        When we run "jrnl --encrypt" and enter
            swordfish
            swordfish
            n
        Then we should see the message "Journal encrypted"
        And the config for journal "default" should contain "encrypt: true"
        When we run "jrnl -n 1" and enter "swordfish"
        Then we should be prompted for a password
        And the output should contain "2013-06-10 15:40 Life is good"

    Scenario Outline: Attempt to encrypt a folder or DayOne journal should result in an error
        Given we use the config "<config_file>"
        When we run "jrnl --encrypt"
        Then the error output should contain "can't be encrypted"

        Examples: configs
        | config_file       |
        | empty_folder.yaml |
        | dayone.yaml       |
