Feature: Reading & writing the config file

    Scenario: Sending an argument with spaces to the editor should work
        Given we use the config "editor-args.yaml"
        When we open the editor and enter "lorem ipsum"
        Then the editor should have been called with 5 arguments
        And one editor argument should be "vim"
        And one editor argument should be "-f"
        And one editor argument should be "-c"
        And one editor argument should match "'?setf markdown'?"

