Feature: Fixing broken config files

    Scenario: Loading a file with  journal
        Given we use the config "broken.json"
        When we run "jrnl -n 2"
        Then we should see the message "Some errors in your jrnl config have been fixed for you."
        and the output should be
            """
            2013-06-09 15:39 My first entry.
            | Everything is alright

            2013-06-10 15:40 Life is good.
            | But I'm better.
            """
