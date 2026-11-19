# Copyright © 2012-2023 jrnl contributors
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
            """
            2013-06-09 15:39 My first entry.
            2013-06-10 15:40 Life is good.
            """


    Scenario: Trying to decrypt an already unencrypted journal
        Given we use the config "simple.yaml"
        When we run "jrnl --decrypt"
        Then the error output should contain "is not encrypted"
        When we run "jrnl -99 --short"
        Then the output should be
            """
            2013-06-09 15:39 My first entry.
            2013-06-10 15:40 Life is good.
            """


    Scenario: Trying to encrypt an already encrypted journal
        Given we use the config "encrypted.yaml"
        When we run "jrnl --encrypt" and enter "bad doggie no biscuit"
        Then the output should contain "already encrypted. Create a new password."
        Then we should be prompted for a password

    Scenario Outline: Encrypting a journal
        Given we use the config "simple.yaml"
        When we run "jrnl --encrypt" and enter
            """
            swordfish
            swordfish
            n
            """
        Then we should get no error
        And the output should contain "Journal encrypted"
        And the config for journal "default" should contain "encrypt: true"
        When we run "jrnl -n 1" and enter "swordfish"
        Then we should be prompted for a password
        And the output should contain "2013-06-10 15:40 Life is good"

    Scenario: Encrypt journal twice and get prompted each time
        Given we use the config "simple.yaml"
        And we don't have a keyring
        When we run "jrnl --encrypt" and enter
            """
            swordfish
            swordfish
            y
            """
        Then we should get no error
        And the output should contain "Journal encrypted"
        When we run "jrnl --encrypt" and enter
            """
            swordfish
            tuna
            tuna
            y
            """
        Then we should get no error
        And the output should contain "Journal default is already encrypted. Create a new password."
        And we should be prompted for a password
        And the config for journal "default" should contain "encrypt: true"

    Scenario: Encrypt journal twice and get prompted each time with keyring
        Given we use the config "simple.yaml"
        And we have a keyring
        When we run "jrnl --encrypt" and enter
            """
            swordfish
            swordfish
            y
            """
        Then we should get no error
        And the output should contain "Journal encrypted"
        When we run "jrnl --encrypt" and enter
            """
            tuna
            tuna
            y
            """
        Then we should get no error
        And the output should contain "Journal default is already encrypted. Create a new password."
        And we should be prompted for a password
        And the config for journal "default" should contain "encrypt: true"

    Scenario: Re-encrypting a v2 journal should upgrade to v3
        Given we use the config "encrypted_v2_journal_legacy_config.yaml"
        When we run "jrnl --encrypt" and enter
            """
            bad doggie no biscuit
            newpassword
            newpassword
            y
            """
        Then we should get no error
        And the output should contain "Journal default is already encrypted. Create a new password."
        And the config for journal "default" should contain "encrypt: true"
        And the journal file should be encrypted with jrnlv3

    Scenario: Decrypting a v3 encrypted journal
        Given we use the config "encrypted_v3.yaml"
        And we use the password "good doggie extra biscuit" if prompted
        When we run "jrnl --decrypt"
        Then the output should contain "Journal decrypted"
        And the config for journal "default" should contain "encrypt: false"
        When we run "jrnl -99 --short"
        Then the output should be
            """
            2013-06-09 15:39 My first entry.
            2013-06-10 15:40 Life is good.
            """

    Scenario: Decrypting a v3 journal with a legacy (pre-base64) header still works (back compat)
        Given we use the config "encrypted_v3_legacy_header.yaml"
        And we use the password "good doggie extra biscuit" if prompted
        When we run "jrnl --decrypt"
        Then the output should contain "Journal decrypted"
        And the config for journal "default" should contain "encrypt: false"
        When we run "jrnl -99 --short"
        Then the output should be
            """
            2013-06-09 15:39 My first entry.
            2013-06-10 15:40 Life is good.
            """

    Scenario: Writing to a v3 journal with a legacy header upgrades it to a base64-encoded header
        Given we use the config "encrypted_v3_legacy_header.yaml"
        And we use the password "good doggie extra biscuit" if prompted
        When we run "jrnl today I triggered the header upgrade"
        Then we should get no error
        And the journal file should be encrypted with jrnlv3
        And the jrnlv3 journal file header should be base64-encoded

    Scenario: Decrypting a v2 journal with v3 encryption set as the default still works (back compat)
        Given we use the config "encrypted.yaml"
        And we use the password "bad doggie no biscuit" if prompted
        When we run "jrnl -99 --short"
        Then the output should be
            """
            2013-06-09 15:39 My first entry.
            2013-06-10 15:40 Life is good.
            """

    Scenario: Writing to a v2 journal upgrades it to v3 and preserves entry content
        Given we use the config "encrypted_v2_journal_legacy_config.yaml"
        And we use the password "bad doggie no biscuit" if prompted
        When we run "jrnl today I triggered the upgrade"
        Then we should get no error
        And the output should contain
            """
            Successfully upgraded "default" from v2 to v3 encryption.
            """
        And the journal file should be encrypted with jrnlv3
        And the config should contain "encrypt: true"
        When we run "jrnl --format json"
        Then we should get no error
        And the output should be valid JSON
        Given we parse the output as JSON
        Then "entries" in the parsed output should have 3 elements
        And "entries.0.title" in the parsed output should be
            """
            My first entry.
            """
        And "entries.0.body" in the parsed output should be
            """
            Everything is alright
            """
        And "entries.1.title" in the parsed output should be
            """
            Life is good.
            """
        And "entries.1.body" in the parsed output should be
            """
            But I'm better.
            """
        And "entries.2.title" in the parsed output should be
            """
            today I triggered the upgrade
            """
        And "entries.2.body" in the parsed output should have 0 elements

    Scenario: Writing to a v1 journal upgrades it to v3 and preserves entry content
        Given we use the config "encrypted_v1_journal_legacy_config.yaml"
        And we use the password "bad doggie no biscuit" if prompted
        When we run "jrnl today I triggered the upgrade"
        Then we should get no error
        And the output should contain
            """
            Successfully upgraded "default" from v1 to v3 encryption.
            """
        And the journal file should be encrypted with jrnlv3
        And the config should contain "encrypt: true"
        When we run "jrnl --format json"
        Then we should get no error
        And the output should be valid JSON
        Given we parse the output as JSON
        Then "entries" in the parsed output should have 3 elements
        And "entries.0.title" in the parsed output should be
            """
            My first entry.
            """
        And "entries.0.body" in the parsed output should be
            """
            Everything is alright
            """
        And "entries.1.title" in the parsed output should be
            """
            Life is good.
            """
        And "entries.1.body" in the parsed output should be
            """
            But I'm better.
            """
        And "entries.2.title" in the parsed output should be
            """
            today I triggered the upgrade
            """
        And "entries.2.body" in the parsed output should have 0 elements

    Scenario: v1 journal with per-journal encrypt key upgrades to v3 and updates config at journal level
        Given we use the config "encrypted_v1_journal_per_journal_encrypt.yaml"
        And we use the password "bad doggie no biscuit" if prompted
        When we run "jrnl today I triggered the upgrade"
        Then we should get no error
        And the output should contain
            """
            Successfully upgraded "default" from v1 to v3 encryption.
            """
        And the journal file should be encrypted with jrnlv3
        And the config for journal "default" should contain "encrypt: true"
        And the config should not contain "encrypt: true"

    Scenario: Missing encrypt key in config does not crash
        Given we use the config "missing_encrypt_key.yaml"
        When we run "jrnl -n 1"
        Then we should get no error

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
