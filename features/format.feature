Feature: Custom formats

    Scenario: JSON format
        Given we use the config "tags.yaml"
        When we run "jrnl --export json"
        Then we should get no error
        And the output should be parsable as json
        And "entries" in the json output should have 2 elements
        And "tags" in the json output should contain "@idea"
        And "tags" in the json output should contain "@journal"
        And "tags" in the json output should contain "@dan"
        And entry 1 should have an array "tags" with 2 elements
        And entry 2 should have an array "tags" with 2 elements

    Scenario Outline: Printing a journal that has multiline entries with tags
        Given we use the config "<config>.yaml"
        When we run "jrnl -n 1 @ipsum"
        Then we should get no error
        And the output should be
        """
        2020-08-29 11:11 Entry the first.
        | Lorem @ipsum dolor sit amet, consectetur adipiscing elit. Praesent malesuada
        | quis est ac dignissim. Aliquam dignissim rutrum pretium. Phasellus
        | pellentesque
        | augue et venenatis facilisis. Suspendisse potenti. Sed dignissim sed nisl eu
        | consequat. Aenean ante ex, elementum ut interdum et, mattis eget lacus. In
        | commodo nulla nec tellus placerat, sed ultricies metus bibendum. Duis eget
        | venenatis erat. In at dolor dui. @tagone and maybe also @tagtwo.
        |
        | Curabitur accumsan nunc ac neque tristique, eleifend faucibus justo
        | ullamcorper. Suspendisse at mattis nunc. Nullam eget lacinia urna. Suspendisse
        | potenti. Ut urna est, venenatis sed ante in, ultrices congue mi. Maecenas eget
        | molestie metus. Mauris porttitor dui ornare gravida porta. Quisque sed lectus
        | hendrerit, lacinia ante eget, vulputate ante. Aliquam vitae erat non felis
        | feugiat sagittis. Phasellus quis arcu fringilla, mattis ligula id, vestibulum
        | urna. Vivamus facilisis leo a mi tincidunt condimentum. Donec eu euismod enim.
        | Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam eu ligula eget
        | velit scelerisque fringilla. Phasellus pharetra justo et nulla fringilla, ac
        | porta sapien accumsan. Class aptent taciti sociosqu ad litora torquent per
        | conubia nostra, per inceptos himenaeos.
        """

        Examples: configs
        | config        |
        | basic_onefile |
        | basic_folder  |
        | basic_dayone  |

    Scenario: Exporting using filters should only export parts of the journal
        Given we use the config "tags.yaml"
        When we run "jrnl -until 'may 2013' --export json"
        Then the output should be parsable as json
        And "entries" in the json output should have 1 element
        And "tags" in the json output should contain "@idea"
        And "tags" in the json output should contain "@journal"
        And "tags" in the json output should not contain "@dan"

    Scenario: Exporting using custom templates
        Given we use the config "simple.yaml"
        And we load template "sample.template"
        When we run "jrnl --export sample"
        Then the output should be
            """
            My first entry.
            ---------------

            Everything is alright

            Life is good.
            -------------

            But I'm better.
            """

    Scenario: Increasing Headings on Markdown export
        Given we use the config "markdown-headings-335.yaml"
        When we run "jrnl --export markdown"
        Then the output should be
            """
            # 2015

            ## April

            ### 2015-04-14 13:23 Heading Test

            #### H1-1

            #### H1-2

            #### H1-3

            ##### H2-1

            ##### H2-2

            ##### H2-3

            Horizontal Rules (ignore)

            ---

            ===

            #### ATX H1

            ##### ATX H2

            ###### ATX H3

            ####### ATX H4

            ######## ATX H5

            ######### ATX H6

            Stuff

            More stuff
            more stuff again
            """

    # the "deletion" journal is used because it doesn't have a newline at the
    # end of the last entry
    Scenario: Add a blank line to Markdown export if there isn't one already
        # https://github.com/jrnl-org/jrnl/issues/768
        # https://github.com/jrnl-org/jrnl/issues/881
        Given we use the config "deletion.yaml"
        When we run "jrnl --format markdown"
        Then the output should be
            """
            # 2019

            ## October

            ### 2019-10-29 11:11 First entry.


            ### 2019-10-29 11:11 Second entry.


            ### 2019-10-29 11:13 Third entry.

            """

    Scenario: Exporting to XML
        Given we use the config "tags.yaml"
        When we run "jrnl --export xml"
        Then the output should be a valid XML string
        And "entries" node in the xml output should have 2 elements
        And "tags" in the xml output should contain ["@idea", "@journal", "@dan"]
        And there should be 7 "tag" elements

    Scenario: Exporting tags
        Given we use the config "tags.yaml"
        When we run "jrnl --export tags"
        Then the output should be
            """
            @idea                : 2
            @journal             : 1
            @dan                 : 1
            """

    Scenario: Exporting fancy
        Given we use the config "tags.yaml"
        When we run "jrnl --export fancy"
        Then the output should be
        """
        ┎──────────────────────────────────────────────────────────────╮2013-04-09 15:39
        ┃ I have an @idea:                                             ╘═══════════════╕
        ┠╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤
        ┃ (1) write a command line @journal software                                   │
        ┃ (2) ???                                                                      │
        ┃ (3) PROFIT!                                                                  │
        ┖──────────────────────────────────────────────────────────────────────────────┘
        ┎──────────────────────────────────────────────────────────────╮2013-06-10 15:40
        ┃ I met with @dan.                                             ╘═══════════════╕
        ┠╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤
        ┃ As alway's he shared his latest @idea on how to rule the world with me.      │
        ┃ inst                                                                         │
        ┖──────────────────────────────────────────────────────────────────────────────┘
        """

    Scenario: Export to yaml
        Given we use the config "tags.yaml"
        And we create cache directory "exported_journal"
        When we run "jrnl --export yaml -o {cache_dir}" with cache directory "exported_journal"
        Then cache directory "exported_journal" should contain the files
        """
        [
        "2013-04-09_i-have-an-idea.md",
        "2013-06-10_i-met-with-dan.md"
        ]
        """
        And the content of file "2013-04-09_i-have-an-idea.md" in cache directory "exported_journal" should be
        """
        title: I have an @idea:
        date: 2013-04-09 15:39
        starred: False
        tags: idea, journal

        (1) write a command line @journal software
        (2) ???
        (3) PROFIT!
        """

    Scenario: Add a blank line to YAML export if there isn't one already
        # https://github.com/jrnl-org/jrnl/issues/768
        # https://github.com/jrnl-org/jrnl/issues/881
        Given we use the config "deletion.yaml"
        And we create cache directory "bug768"
        When we run "jrnl --export yaml -o {cache_dir}" with cache directory "bug768"
        Then cache directory "bug768" should contain the files
            """
            [
            "2019-10-29_first-entry.md",
            "2019-10-29_second-entry.md",
            "2019-10-29_third-entry.md"
            ]
            """
        And the content of file "2019-10-29_third-entry.md" in cache directory "bug768" should be
            """
            title: Third entry.
            date: 2019-10-29 11:13
            starred: False
            tags:

            """

    Scenario: Printing a journal that has multiline entries
        Given we use the config "multiline.yaml"
        When we run "jrnl -n 1"
        Then we should get no error
        And the output should be
            """
            2013-06-09 15:39 Multiple line entry.
            | This is the first line.
            | This line doesn't have any ending punctuation
            |
            | There is a blank line above this.
            """

    Scenario: Exporting dayone to json
        Given we use the config "dayone.yaml"
        When we run "jrnl --export json"
        Then we should get no error
        And the output should be parsable as json
        And the json output should contain entries.0.uuid = "4BB1F46946AD439996C9B59DE7C4DDC1"

    Scenario: Empty DayOne entry bodies should not error
        # https://github.com/jrnl-org/jrnl/issues/780
        Given we use the config "bug780.yaml"
        When we run "jrnl --short"
        Then we should get no error

    Scenario: --short displays the short version of entries (only the title)
        Given we use the config "simple.yaml"
        When we run "jrnl -on 2013-06-10 --short"
        Then the output should be "2013-06-10 15:40 Life is good."

    Scenario: -s displays the short version of entries (only the title)
        Given we use the config "simple.yaml"
        When we run "jrnl -on 2013-06-10 -s"
        Then the output should be "2013-06-10 15:40 Life is good."

