Feature: Using the installed keyring

    Scenario: Storing a password in keyring
        Given we use the config "multiple.yaml"
        And we have a keyring
        When we run "jrnl simple --encrypt" and enter
            sabertooth
            sabertooth
            Y
        Then the config for journal "simple" should have "encrypt" set to "bool:True"
        When we run "jrnl simple -n 1"
        Then the output should contain "2013-06-10 15:40 Life is good"
