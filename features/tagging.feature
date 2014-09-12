Feature: Tagging

    Scenario: Displaying tags
        Given we use the config "tags.yaml"
        When we run "jrnl --tags"
        Then we should get no error
        and the output should be
            """
            @idea                : 2
            @journal             : 1
            @dan                 : 1
            """

    Scenario: Filtering journals should also filter tags
        Given we use the config "tags.yaml"
        When we run "jrnl -from 'may 2013' --tags"
        Then we should get no error
        and the output should be
            """
            @idea                : 1
            @dan                 : 1
            """

    Scenario: Tags should allow certain special characters
        Given we use the config "tags-216.yaml"
        When we run "jrnl --tags"
        Then we should get no error
        and the output should be
            """
            @os/2                : 1
            @c++                 : 1
            @c#                  : 1
            """
    Scenario:  An email should not be a tag
        Given we use the config "tags-237.yaml"
        When we run "jrnl --tags"
        Then we should get no error
        and the output should be
            """
            @newline             : 1
            @email               : 1
            """

    Scenario:  Entry cans start and end with tags
        Given we use the config "basic.yaml"
        When we run "jrnl today: @foo came over, we went to a @bar"
        When we run "jrnl --tags"
        Then the output should be
            """
            @foo                 : 1
            @bar                 : 1
            """
