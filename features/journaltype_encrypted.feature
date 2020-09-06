Feature: Loading the encrypted journal type

    Scenario: Loading an encrypted journal
        Given we use the config "encrypted.yaml"
        When we run "jrnl -n 1" and enter "bad doggie no biscuit"
        Then we should be prompted for a password
        And the output should contain "2013-06-10 15:40 Life is good"

    Scenario: Mistyping your password
        Given we use the config "basic.yaml"
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
        Given we use the config "basic.yaml"
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
