Feature: Reading & writing the config file

    Scenario: Sending an argument with spaces to the editor should work
        Given we use the config "editor-args.yaml"
        When we open the editor and enter "lorem ipsum"
        Then the editor should have been called with 5 arguments
        And one editor argument should be "vim"
        And one editor argument should be "-f"
        And one editor argument should be "-c"
        And one editor argument should match "'?setf markdown'?"

    Scenario: Invalid color configuration
        Given we use the config "invalid_color.yaml"
        When we run "jrnl -on 2013-06-10 -s"
        Then the output should be
            """
            2013-06-10 15:40 Life is good.
            """
        And we should get no error
        And the error output should contain
            """
            body set to invalid color
            """

    @todo
    Scenario: Missing values in config are given a default

    @todo
    Scenario: Journal-level config values override global-level config values

    @todo
    Scenario: Config with a lower version number updates to current version

    @todo
    Scenario: Nested config values are written to the config file

