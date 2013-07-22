    Feature: Multiple journals

        Scenario: Loading an encrypted journal
            Given we use the config "encrypted.json"
            When we run "jrnl -n 1" and enter "bad doggie no biscuit"
            Then we should see the message "Password"
            and the output should contain "2013-06-10 15:40 Life is good"

        Scenario: Decrypting a journal
            Given we use the config "encrypted.json"
            When we run "jrnl --decrypt" and enter "bad doggie no biscuit"
            Then we should see the message "Journal decrypted"
            and the journal should have 2 entries
            and the config should have "encrypt" set to "bool:False"

        Scenario: Encrypting a journal
            Given we use the config "basic.json"
            When we run "jrnl --encrypt" and enter "swordfish"
            Then we should see the message "Journal encrypted"
            and the config should have "encrypt" set to "bool:True"
            When we run "jrnl -n 1" and enter "swordfish"
            Then we should see the message "Password"
            and the output should contain "2013-06-10 15:40 Life is good"

