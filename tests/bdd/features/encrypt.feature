# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

Feature: Encrypting and decrypting journals

    Scenario: Decrypting a journal
        Given we use the config "encrypted.yaml"
        And we use the password "bad doggie no biscuit" if prompted
        When we run "jrnl --decrypt"
        Then the output should contain "Journal decrypted"
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


    Scenario: Trying to encrypt an already encrypted journal
        Given we use the config "encrypted.yaml"
        When we run "jrnl --encrypt" and enter "bad doggie no biscuit"
        Then the output should contain "already encrypted. Create a new password."
        Then we should be prompted for a password

    Scenario Outline: Encrypting a journal
        Given we use the config "simple.yaml"
        When we run "jrnl --encrypt" and enter
            swordfish
            swordfish
            n
        Then we should get no error
        And the output should contain "Journal encrypted"
        And the config for journal "default" should contain "encrypt: true"
        When we run "jrnl -n 1" and enter "swordfish"
        Then we should be prompted for a password
        And the output should contain "2013-06-10 15:40 Life is good"


    Scenario Outline: Running jrnl with encrypt: true on unencryptable journals
        Given we use the config "<config_file>"
        When we run "jrnl --config-override encrypt true here is a new entry"
        Then the error output should contain "journal can't be encrypted"

        Examples: configs
        | config_file       |
        | basic_folder.yaml |
        | basic_dayone.yaml |


    Scenario Outline: Attempt to encrypt a folder or DayOne journal should result in an error
        Given we use the config "<config_file>"
        When we run "jrnl --encrypt"
        Then the error output should contain "can't be encrypted"

        Examples: configs
        | config_file       |
        | basic_folder.yaml |
        | basic_dayone.yaml |
