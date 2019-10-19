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

    Scenario:  Excluding a tag should filter it
        Given we use the config "basic.yaml"
        When we run "jrnl today: @foo came over, we went to a bar"
        When we run "jrnl I have decided I did not enjoy that @bar"
        When we run "jrnl --tags -not @bar"
        Then the output should be
            """
            @foo                 : 1
            """

    Scenario:  Excluding a tag should filter an entry, even if an unfiltered tag is in that entry
        Given we use the config "basic.yaml"
        When we run "jrnl today: I do @not think this will show up @thought"
        When we run "jrnl today: I think this will show up @thought"
        When we run "jrnl --tags -not @not"
        Then the output should be
            """
            @thought             : 1
            """

    Scenario:  Excluding multiple tags should filter them
        Given we use the config "basic.yaml"
        When we run "jrnl today: I do @not think this will show up @thought"
        When we run "jrnl today: I think this will show up @thought"
        When we run "jrnl today: This should @never show up @thought"
        When we run "jrnl today: What a nice day for filtering @thought"
        When we run "jrnl --tags -not @not @never"
        Then the output should be
            """
            @thought             : 2
            """
