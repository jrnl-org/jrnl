Feature: Installing jrnl

    Scenario: Install jrnl with default options
        Given we use no config
        When we run "jrnl hello world" and enter
            \n
            \n
        Then the output should contain "Journal 'default' created"
        And the default journal "journal.txt" should be in the "." directory
        And the config should contain "encrypt: false"
        And the version in the config file should be up-to-date

    Scenario: Install jrnl with custom relative default journal path
        Given we use no config
        When we run "jrnl hello world" and enter
            default/custom.txt
            n
        Then the output should contain "Journal 'default' created"
        And the default journal "custom.txt" should be in the "default" directory
        And the config should contain "encrypt: false"
        And the version in the config file should be up-to-date

    Scenario: Install jrnl with custom expanded default journal path
        Given we use no config
        And the home directory is called "home"
        When we run "jrnl hello world" and enter
            ~/custom.txt
            n
        Then the output should contain "Journal 'default' created"
        And the default journal "custom.txt" should be in the "home" directory
        And the config should contain "encrypt: false"
        And the version in the config file should be up-to-date

    Scenario: Install jrnl with encrypted default journal
        Given we use no config
        When we run "jrnl hello world" and enter
            encrypted.txt
            y
        Then the output should contain "Journal will be encrypted"
        And the default journal "encrypted.txt" should be in the "." directory
        And the config should contain "encrypt: true"
        And the version in the config file should be up-to-date
        When we run "jrnl"
        Then we should be prompted for a password
    
    Scenario: Install jrnl with encrypted default journal with no entries
        Given we use no config
        And we use the password "test" if prompted
        When we run "jrnl -1" and enter
            encrypted.txt
            y
            n
        Then the error output should contain "Journal will be encrypted"
        And the default journal "encrypted.txt" should be in the "." directory
        And the config should contain "encrypt: true"
        And the version in the config file should be up-to-date
        When we run "jrnl -1"
        Then we should be prompted for a password
        And the error output should contain "no entries found"
        And the error output should not contain "Wrong password, try again"
