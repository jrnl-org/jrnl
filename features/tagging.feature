Feature: Tagging

    Scenario: Displaying tags
        Given we use the config "tags.json"
        When we run "jrnl --tags"
        Then we should get no error
        and the output should be
            """
            @idea                : 2
            @journal             : 1
            @dan                 : 1
            """

    Scenario: Filtering journals should also filter tags
        Given we use the config "tags.json"
        When we run "jrnl -from 'may 2013' --tags"
        Then we should get no error
        and the output should be
            """
            @idea                : 1
            @dan                 : 1
            """

    Scenario: Tags should allow certain special characters
        Given we use the config "tags-216.json"
        When we run "jrnl --tags"
        Then we should get no error
        and the output should be
            """
            @os/2                : 1
            @c++                 : 1
            @c#                  : 1
            """
	Scenario:  An email should not be a tag
		Given we use the config "tags-237.json"
		When we run "jrnl --tags"
		Then we should get no error
		and the output should be
			"""
			@email               : 1
			"""