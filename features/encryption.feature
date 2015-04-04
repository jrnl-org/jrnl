    Feature: Encrypted journals
        Scenario: Loading an encrypted journal
            Given we use the config "encrypted.yaml"
            When we run "jrnl -n 1" and enter "bad doggie no biscuit"
            Then we should see the message "Password"
            and the output should contain "2013-06-10 15:40 Life is good"

        Scenario: Decrypting a journal
            Given we use the config "encrypted.yaml"
            When we run "jrnl --decrypt" and enter "bad doggie no biscuit"
            Then the config for journal "default" should have "encrypt" set to "bool:False"
            Then we should see the message "Journal decrypted"
            and the journal should have 2 entries

        Scenario: Encrypting a journal
            Given we use the config "basic.yaml"
            When we run "jrnl --encrypt" and enter "swordfish"
            Then we should see the message "Journal encrypted"
            and the config for journal "default" should have "encrypt" set to "bool:True"
            When we run "jrnl -n 1" and enter "swordfish"
            Then we should see the message "Password"
            and the output should contain "2013-06-10 15:40 Life is good"

        Scenario: Storing a password in Keychain
            Given we use the config "multiple.yaml"
            When we run "jrnl simple --encrypt" and enter "sabertooth"
            When we set the keychain password of "simple" to "sabertooth"
            Then the config for journal "simple" should have "encrypt" set to "bool:True"
            When we run "jrnl simple -n 1"
            Then we should not see the message "Password"
            and the output should contain "2013-06-10 15:40 Life is good"

        Scenario: Upgrading a journal encrypted with jrnl 1.x
            Given we use the config "encrypted_old.json"
            When we run "jrnl -n 1" and enter 
                """
                Y
                bad doggie no biscuit
                bad doggie no biscuit
                """
            Then we should see the message "Password"
            and the output should contain "2013-06-10 15:40 Life is good"
