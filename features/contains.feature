Feature: Contains

    Scenario: Searching for a string
        Given we use the config "basic.yaml"
        When we run "jrnl -contains life"
        Then we should get no error
        and the output should be
            """
            2013-06-10 15:40 Life is good.
            | But I'm better.
            """

    Scenario: Searching for a string within tag results
        Given we use the config "tags.yaml"
        When we run "jrnl @idea -contains software"
        Then we should get no error
        And the output should contain "software"

    Scenario: Searching for a string within AND tag results
        Given we use the config "tags.yaml"
        When we run "jrnl -and @journal @idea -contains software"
        Then we should get no error
        and the output should contain "software"

    Scenario: Searching for a string within NOT tag results
        Given we use the config "tags.yaml"
        When we run "jrnl -not @dan -contains software"
        Then we should get no error
        and the output should contain "software"
