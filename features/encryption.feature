    Feature: Encrypted journals

        Scenario: Loading an encrypted journal
            Given we use the config "encrypted.json"
            When we run "jrnl -n 1" and enter "bad doggie no biscuit"
            Then we should see the message "Password"
            and the output should contain "2013-06-10 15:40 Life is good"

        Scenario: Decrypting a journal
            Given we use the config "encrypted.json"
            When we run "jrnl --decrypt" and enter "bad doggie no biscuit"
            Then the config for journal "default" should have "encrypt" set to "bool:False"
            Then we should see the message "Journal decrypted"
            and the journal should have 2 entries

        Scenario: Encrypting a journal
            Given we use the config "basic.json"
            When we run "jrnl --encrypt" and enter "swordfish"
            Then we should see the message "Confirm Password:"
            When we enter "swordfish"
            Then we should see the message "Journal encrypted"
            and the config for journal "default" should have "encrypt" set to "bool:True"
            When we run "jrnl -n 1" and enter "swordfish"
            Then we should see the message "Password"
            and the output should contain "2013-06-10 15:40 Life is good"

        Scenario: Loading an encrypted journal with password in config
            Given we use the config "encrypted_with_pw.json"
            When we run "jrnl -n 1"
            Then the output should contain "2013-06-10 15:40 Life is good"

        Scenario: Storing a password in Keychain
            Given we use the config "multiple.json"
            When we run "jrnl simple --encrypt" and enter "sabertooth"
            Then we should see the message "Confirm Password:"
            When we enter "sabertooth"
            and we set the keychain password of "simple" to "sabertooth"
            Then the config for journal "simple" should have "encrypt" set to "bool:True"
            When we run "jrnl simple -n 1"
            Then we should not see the message "Password"
            and the output should contain "2013-06-10 15:40 Life is good"
