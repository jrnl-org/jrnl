Feature: Exporting a Journal

    Scenario: Exporting to json
        Given we use the config "tags.yaml"
        When we run "jrnl --export json"
        Then we should get no error
        And the output should be parsable as json
        And "entries" in the json output should have 2 elements
        And "tags" in the json output should contain "@idea"
        And "tags" in the json output should contain "@journal"
        And "tags" in the json output should contain "@dan"

    Scenario: Exporting using filters should only export parts of the journal
        Given we use the config "tags.yaml"
        When we run "jrnl -until 'may 2013' --export json"
        Then the output should be parsable as json
        And "entries" in the json output should have 1 element
        And "tags" in the json output should contain "@idea"
        And "tags" in the json output should contain "@journal"
        And "tags" in the json output should not contain "@dan"

    Scenario: Exporting using custom templates
        Given we use the config "basic.yaml"
        Given we load template "sample.template"
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

    Scenario: Exporting to XML
        Given we use the config "tags.yaml"
        When we run "jrnl --export xml"
        Then the output should be a valid XML string
        And "entries" node in the xml output should have 2 elements
        And "tags" in the xml output should contain ["@idea", "@journal", "@dan"]

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
        And we created a directory named "exported_journal"
        When we run "jrnl --export yaml -o exported_journal"
        Then "exported_journal" should contain the files ["2013-04-09_i-have-an-idea.md", "2013-06-10_i-met-with-dan.md"]
        And the content of exported yaml "exported_journal/2013-04-09_i-have-an-idea.md" should be
        """
        title: I have an @idea:
        date: 2013-04-09 15:39
        starred: False
        tags: idea, journal

        (1) write a command line @journal software
        (2) ???
        (3) PROFIT!
        """
