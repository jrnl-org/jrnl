Feature: Tagging
# See search.feature for tag-related searches
# And format.feature for tag-related output

    Scenario Outline: Tags should allow certain special characters such as /, +, #
        Given we use the config "<config>.yaml"
        When we run "jrnl 2020-09-26: This is an entry about @os/2 and @c++ and @c#"
        When we run "jrnl --tags -on 2020-09-26"
        Then we should get no error
        And the output should be
            """
            @os/2                : 1
            @c++                 : 1
            @c#                  : 1
            """

        Examples: configs
        | config        |
        | basic_onefile |
        | basic_folder  |
        | basic_dayone  |

    Scenario Outline: Emails addresses should not be parsed as tags
        Given we use the config "<config>.yaml"
        When we run "jrnl 2020-09-26: The email address test@example.com does not seem to work for me"
        When we run "jrnl 2020-09-26: The email address test@example.org also does not work for me"
        When we run "jrnl 2020-09-26: I tried test@example.org and test@example.edu too"
        Then we flush the output
        When we run "jrnl --tags -on 2020-09-26"
        Then we should get no error
        And the output should be "[No tags found in journal.]"

        Examples: configs
        | config        |
        | basic_onefile |
        | basic_folder  |
        | basic_dayone  |

    Scenario Outline: Emails addresses should not be parsed as tags
        Given we use the config "<config>.yaml"
        When we run "jrnl 2020-09-26: The email address test@example.com doesn't seem to work for me"
        When we run "jrnl 2020-09-26: The email address test@example.org also doesn't work for me"
        When we run "jrnl 2020-09-26: I tried test@example.org and test@example.edu too"
        Then we flush the output
        When we run "jrnl --tags -on 2020-09-26"
        Then we should get no error
        And the output should be "[No tags found in journal.]"

        Examples: configs
        | config        |
        | basic_onefile |
        | basic_folder  |
        | basic_dayone  |

    Scenario Outline:  Entry can start and end with tags
        Given we use the config "<config>.yaml"
        When we run "jrnl 2020-09-26: @foo came over, we went to a @bar"
        When we run "jrnl --tags -on 2020-09-26"
        Then the output should be
            """
            @foo                 : 1
            @bar                 : 1
            """

        Examples: configs
        | config        |
        | basic_onefile |
        | basic_folder  |
        | basic_dayone  |
