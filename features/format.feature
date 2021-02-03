Feature: Custom formats
    Scenario: Pretty Printing aka the Default 
    Given We use the config "pretty.yaml"
    When we run "jrnl --format pretty -3"
    Then we should get no error
    And the output should be pretty printed

    Scenario Outline: JSON format
        Given we use the config "<config>.yaml"
        And we use the password "test" if prompted
        When we run "jrnl --format json"
        Then we should get no error
        And the output should be parsable as json
        And "entries" in the json output should have 3 elements
        And "tags" in the json output should contain "@ipsum"
        And "tags" in the json output should contain "@tagone"
        And "tags" in the json output should contain "@tagthree"
        And "tags" in the json output should contain "@tagtwo"
        And entry 1 should have an array "tags" with 3 elements
        And entry 2 should have an array "tags" with 1 elements
        And entry 3 should have an array "tags" with 2 elements

        Examples: configs
        | config          |
        | basic_onefile   |
        | basic_encrypted |
        | basic_folder    |
        | basic_dayone    |

    Scenario: Exporting dayone to json
        Given we use the config "dayone.yaml"
        When we run "jrnl --export json"
        Then we should get no error
        And the output should be parsable as json
        And the json output should contain entries.0.uuid = "4BB1F46946AD439996C9B59DE7C4DDC1"

    Scenario Outline: Printing a journal that has multiline entries with tags
        Given we use the config "<config>.yaml"
        And we use the password "test" if prompted
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
        | config          |
        | basic_onefile   |
        | basic_encrypted |
        | basic_folder    |
        | basic_dayone    |

    Scenario Outline: Exporting using filters should only export parts of the journal
        Given we use the config "<config>.yaml"
        And we use the password "test" if prompted
        When we run "jrnl -until 'August 2020' --format json"
        Then the output should be parsable as json
        Then we should get no error
        And the output should be parsable as json
        And "entries" in the json output should have 2 elements
        And "tags" in the json output should contain "@ipsum"
        And "tags" in the json output should contain "@tagone"
        And "tags" in the json output should contain "@tagtwo"
        And entry 1 should have an array "tags" with 3 elements
        And entry 2 should have an array "tags" with 1 elements

        Examples: configs
        | config          |
        | basic_onefile   |
        | basic_encrypted |
        | basic_folder    |
        | basic_dayone    |

    Scenario Outline: Exporting using custom templates
        Given we use the config "<config>.yaml"
        And we load template "sample.template"
        And we use the password "test" if prompted
        When we run "jrnl -1 --format sample"
        Then the output should be
        """
        The third entry finally after weeks without writing.
        ----------------------------------------------------

        I'm so excited about emojis. 💯 🎶 💩

        Donec semper pellentesque iaculis. Nullam cursus et justo sit amet venenatis.
        Vivamus tempus ex dictum metus vehicula gravida. Aliquam sed sem dolor. Nulla
        eget ultrices purus. Quisque at nunc at quam pharetra consectetur vitae quis
        dolor. Fusce ultricies purus eu est feugiat, quis scelerisque nibh malesuada.
        Quisque egestas semper nibh in hendrerit. Nam finibus ex in mi mattis
        vulputate. Sed mauris urna, consectetur in justo eu, volutpat accumsan justo.
        Phasellus aliquam lacus placerat convallis vestibulum. Curabitur maximus at
        ante eget fringilla. @tagthree and also @tagone
        """

        Examples: configs
        | config          |
        | basic_onefile   |
        | basic_encrypted |
        | basic_folder    |
        | basic_dayone    |

    Scenario Outline: Increasing Headings on Markdown export
        Given we use the config "<config>.yaml"
        And we use the password "test" if prompted
        When we open the editor and append
        """
        [2020-10-14 13:23] Heading Test

        H1-1
        =

        H1-2
        ===

        H1-3
        ============================

        H2-1
        -

        H2-2
        ---

        H2-3
        ----------------------------------

        Horizontal Rules (ignore)

        ---

        ===

        # ATX H1

        ## ATX H2

        ### ATX H3

        #### ATX H4

        ##### ATX H5

        ###### ATX H6

        Stuff

        More stuff
        more stuff again
        """
        Then we flush the output
        When we run "jrnl -1 --export markdown"
        Then the output should be
        """
        # 2020

        ## October

        ### 2020-10-14 13:23 Heading Test

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

        Examples: configs
        | config          |
        | basic_onefile   |
        | basic_encrypted |
        | basic_folder    |
        # | basic_dayone    | @todo

    Scenario Outline: Add a blank line to Markdown export if there isn't one already
        # https://github.com/jrnl-org/jrnl/issues/768
        # https://github.com/jrnl-org/jrnl/issues/881
        Given we use the config "<config>.yaml"
        And we use the password "test" if prompted
        When we open the editor and append
        """
        [2020-10-29 11:11] First entry.
        [2020-10-29 11:11] Second entry.
        [2020-10-29 11:13] Third entry.
        """
        Then we flush the output
        When we run "jrnl -3 --format markdown"
        Then the output should be
        """
        # 2020

        ## October

        ### 2020-10-29 11:11 First entry.


        ### 2020-10-29 11:11 Second entry.


        ### 2020-10-29 11:13 Third entry.

        """

        Examples: configs
        | config          |
        | basic_onefile   |
        | basic_encrypted |
        | basic_folder    |
        # | basic_dayone    | @todo

    @skip
    Scenario Outline: Exporting to XML
        Given we use the config "<config>.yaml"
        And we use the password "test" if prompted
        When we run "jrnl --export xml"
        Then the output should be a valid XML string
        And "entries" node in the xml output should have 3 elements
        And "tags" in the xml output should contain ["@ipsum", "@tagone", "@tagtwo", "@tagthree"]
        And there should be 10 "tag" elements

        Examples: configs
        | config          |
        # | basic_onefile   | @todo
        # | basic_encrypted | @todo
        # | basic_folder    | @todo
        # | basic_dayone    | @todo

    Scenario: Exporting to XML
        Given we use the config "tags.yaml"
        And we use the password "test" if prompted
        When we run "jrnl --export xml"
        Then the output should be a valid XML string
        And "entries" node in the xml output should have 2 elements
        And "tags" in the xml output should contain ["@idea", "@journal", "@dan"]
        And there should be 7 "tag" elements

    Scenario Outline: Exporting tags
        Given we use the config "<config>.yaml"
        And we use the password "test" if prompted
        When we run "jrnl --export tags"
        Then the output should be
        """
        @tagtwo              : 2
        @tagone              : 2
        @tagthree            : 1
        @ipsum               : 1
        """

        Examples: configs
        | config          |
        | basic_onefile   |
        | basic_encrypted |
        | basic_folder    |
        | basic_dayone    |

    @todo
    Scenario Outline: Exporting fancy
        # Needs better emoji support
        Given we use the config "<config>.yaml"
        And we use the password "test" if prompted
        When we run "jrnl --export fancy"
        Then the output should be
        """
        ┎──────────────────────────────────────────────────────────────╮2020-08-29 11:11
        ┃ Entry the first.                                             ╘═══════════════╕
        ┠╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤
        ┃ Lorem @ipsum dolor sit amet, consectetur adipiscing elit. Praesent malesuada │
        ┃ quis est ac dignissim. Aliquam dignissim rutrum pretium. Phasellus           │
        ┃ pellentesque                                                                 │
        ┃ augue et venenatis facilisis. Suspendisse potenti. Sed dignissim sed nisl eu │
        ┃ consequat. Aenean ante ex, elementum ut interdum et, mattis eget lacus. In   │
        ┃ commodo nulla nec tellus placerat, sed ultricies metus bibendum. Duis eget   │
        ┃ venenatis erat. In at dolor dui. @tagone and maybe also @tagtwo.             │
        ┃                                                                              │
        ┃ Curabitur accumsan nunc ac neque tristique, eleifend faucibus justo          │
        ┃ ullamcorper. Suspendisse at mattis nunc. Nullam eget lacinia urna.           │
        ┃ Suspendisse                                                                  │
        ┃ potenti. Ut urna est, venenatis sed ante in, ultrices congue mi. Maecenas    │
        ┃ eget                                                                         │
        ┃ molestie metus. Mauris porttitor dui ornare gravida porta. Quisque sed       │
        ┃ lectus                                                                       │
        ┃ hendrerit, lacinia ante eget, vulputate ante. Aliquam vitae erat non felis   │
        ┃ feugiat sagittis. Phasellus quis arcu fringilla, mattis ligula id,           │
        ┃ vestibulum                                                                   │
        ┃ urna. Vivamus facilisis leo a mi tincidunt condimentum. Donec eu euismod     │
        ┃ enim.                                                                        │
        ┃ Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam eu ligula eget  │
        ┃ velit scelerisque fringilla. Phasellus pharetra justo et nulla fringilla, ac │
        ┃ porta sapien accumsan. Class aptent taciti sociosqu ad litora torquent per   │
        ┃ conubia nostra, per inceptos himenaeos.                                      │
        ┖──────────────────────────────────────────────────────────────────────────────┘
        ┎──────────────────────────────────────────────────────────────╮2020-08-31 14:32
        ┃ A second entry in what I hope to be a long series.           ╘═══════════════╕
        ┠╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤
        ┃ Sed sit amet metus et sapien feugiat elementum. Aliquam bibendum lobortis    │
        ┃ leo                                                                          │
        ┃ vitae tempus. Donec eleifend nec mi non volutpat. Lorem ipsum dolor sit      │
        ┃ amet,                                                                        │
        ┃ consectetur adipiscing elit. Praesent ut sodales libero. Maecenas nisl       │
        ┃ lorem,                                                                       │
        ┃ vestibulum in tempus sit amet, fermentum ut arcu. Donec vel vestibulum       │
        ┃ lectus,                                                                      │
        ┃ eget pretium enim. Maecenas diam nunc, imperdiet vitae pharetra sed, pretium │
        ┃ id                                                                           │
        ┃ lectus. Donec eu metus et turpis tempor tristique ac non ex. In tellus arcu, │
        ┃ egestas at efficitur et, ultrices vel est. Sed commodo et nibh non           │
        ┃ elementum.                                                                   │
        ┃ Mauris tempus vitae neque vel viverra. @tagtwo all by its lonesome.          │
        ┃                                                                              │
        ┃ Nulla mattis elementum magna, viverra pretium dui fermentum et. Cras vel     │
        ┃ vestibulum odio. Quisque sit amet turpis et urna finibus maximus. Interdum   │
        ┃ et                                                                           │
        ┃ malesuada fames ac ante ipsum primis in faucibus. Fusce porttitor iaculis    │
        ┃ sem,                                                                         │
        ┃ non dictum ipsum varius nec. Nulla eu erat at risus gravida blandit non vel  │
        ┃ ante. Nam egestas ipsum leo, eu ultricies ipsum tincidunt vel. Morbi a       │
        ┃ commodo                                                                      │
        ┃ eros.                                                                        │
        ┃                                                                              │
        ┃ Nullam dictum, nisl ac varius tempus, ex tortor fermentum nisl, non          │
        ┃ tempus dolor neque a lorem. Suspendisse a faucibus ex, vel ornare tortor.    │
        ┃ Maecenas tincidunt id felis quis semper. Pellentesque enim libero, fermentum │
        ┃ quis metus id, rhoncus euismod magna. Nulla finibus velit eu purus bibendum  │
        ┃ interdum. Integer id justo dui. Integer eu tellus in turpis bibendum         │
        ┃ blandit.                                                                     │
        ┃ Quisque auctor lacinia consectetur.                                          │
        ┖──────────────────────────────────────────────────────────────────────────────┘
        ┎──────────────────────────────────────────────────────────────╮2020-09-24 09:14
        ┃ The third entry finally after weeks without writing.         ╘═══════════════╕
        ┠╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤
        ┃ I'm so excited about emojis. 💯 🎶 💩                                           │
        ┃                                                                              │
        ┃ Donec semper pellentesque iaculis. Nullam cursus et justo sit amet           │
        ┃ venenatis.                                                                   │
        ┃ Vivamus tempus ex dictum metus vehicula gravida. Aliquam sed sem dolor.      │
        ┃ Nulla                                                                        │
        ┃ eget ultrices purus. Quisque at nunc at quam pharetra consectetur vitae quis │
        ┃ dolor. Fusce ultricies purus eu est feugiat, quis scelerisque nibh           │
        ┃ malesuada.                                                                   │
        ┃ Quisque egestas semper nibh in hendrerit. Nam finibus ex in mi mattis        │
        ┃ vulputate. Sed mauris urna, consectetur in justo eu, volutpat accumsan       │
        ┃ justo.                                                                       │
        ┃ Phasellus aliquam lacus placerat convallis vestibulum. Curabitur maximus at  │
        ┃ ante eget fringilla. @tagthree and also @tagone                              │
        ┖──────────────────────────────────────────────────────────────────────────────┘
        """

        Examples: configs
        | config          |
        | basic_onefile   |
        | basic_encrypted |
        | basic_folder    |
        | basic_dayone    |

    @skip_win
    Scenario Outline: Export to yaml
        Given we use the config "<config>.yaml"
        And we use the password "test" if prompted
        And we create a cache directory
        When we run "jrnl --export yaml -o {cache_dir}"
        Then the cache should contain the files
        """
        2020-08-29_entry-the-first.md
        2020-08-31_a-second-entry-in-what-i-hope-to-be-a-long-series.md
        2020-09-24_the-third-entry-finally-after-weeks-without-writing.md
        """
        And the content of file "2020-08-29_entry-the-first.md" in the cache should be
        """
        ---
        title: Entry the first.
        date: 2020-08-29 11:11
        starred: False
        tags: tagone, ipsum, tagtwo
        body: |
            Lorem @ipsum dolor sit amet, consectetur adipiscing elit. Praesent malesuada
            quis est ac dignissim. Aliquam dignissim rutrum pretium. Phasellus pellentesque
            augue et venenatis facilisis. Suspendisse potenti. Sed dignissim sed nisl eu
            consequat. Aenean ante ex, elementum ut interdum et, mattis eget lacus. In
            commodo nulla nec tellus placerat, sed ultricies metus bibendum. Duis eget
            venenatis erat. In at dolor dui. @tagone and maybe also @tagtwo.

            Curabitur accumsan nunc ac neque tristique, eleifend faucibus justo
            ullamcorper. Suspendisse at mattis nunc. Nullam eget lacinia urna. Suspendisse
            potenti. Ut urna est, venenatis sed ante in, ultrices congue mi. Maecenas eget
            molestie metus. Mauris porttitor dui ornare gravida porta. Quisque sed lectus
            hendrerit, lacinia ante eget, vulputate ante. Aliquam vitae erat non felis
            feugiat sagittis. Phasellus quis arcu fringilla, mattis ligula id, vestibulum
            urna. Vivamus facilisis leo a mi tincidunt condimentum. Donec eu euismod enim.
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam eu ligula eget
            velit scelerisque fringilla. Phasellus pharetra justo et nulla fringilla, ac
            porta sapien accumsan. Class aptent taciti sociosqu ad litora torquent per
            conubia nostra, per inceptos himenaeos.        
        ...
        """

        Examples: configs
        | config          |
        | basic_onefile   |
        | basic_encrypted |
        | basic_folder    |
        # | basic_dayone    |

    @skip_win # @todo YAML exporter does not correctly export emoji on Windows
    Scenario Outline: Add a blank line to YAML export if there isn't one already
        # https://github.com/jrnl-org/jrnl/issues/768
        # https://github.com/jrnl-org/jrnl/issues/881
        Given we use the config "<config>.yaml"
        And we use the password "test" if prompted
        And we create a cache directory
        When we run "jrnl --export yaml -o {cache_dir}"
        Then the cache should contain the files
        """
        2020-08-29_entry-the-first.md
        2020-08-31_a-second-entry-in-what-i-hope-to-be-a-long-series.md
        2020-09-24_the-third-entry-finally-after-weeks-without-writing.md
        """
        And the content of file "2020-09-24_the-third-entry-finally-after-weeks-without-writing.md" in the cache should be
        """
        ---
        title: The third entry finally after weeks without writing.
        date: 2020-09-24 09:14
        starred: False
        tags: tagone, tagthree
        body: |
            I'm so excited about emojis. 💯 🎶 💩

            Donec semper pellentesque iaculis. Nullam cursus et justo sit amet venenatis.
            Vivamus tempus ex dictum metus vehicula gravida. Aliquam sed sem dolor. Nulla
            eget ultrices purus. Quisque at nunc at quam pharetra consectetur vitae quis
            dolor. Fusce ultricies purus eu est feugiat, quis scelerisque nibh malesuada.
            Quisque egestas semper nibh in hendrerit. Nam finibus ex in mi mattis
            vulputate. Sed mauris urna, consectetur in justo eu, volutpat accumsan justo.
            Phasellus aliquam lacus placerat convallis vestibulum. Curabitur maximus at
            ante eget fringilla. @tagthree and also @tagone        
        ...
        """

        Examples: configs
        | config          |
        | basic_onefile   |
        | basic_encrypted |
        | basic_folder    |
        # | basic_dayone    | @todo

    Scenario: Empty DayOne entry bodies should not error
        # https://github.com/jrnl-org/jrnl/issues/780
        Given we use the config "bug780.yaml"
        When we run "jrnl --short"
        Then we should get no error

    Scenario Outline: --short displays the short version of entries (only the title)
        Given we use the config "<config>.yaml"
        And we use the password "test" if prompted
        When we run "jrnl -on 2020-08-31 --short"
        Then the output should be "2020-08-31 14:32 A second entry in what I hope to be a long series."

        Examples: configs
        | config          |
        | basic_onefile   |
        | basic_encrypted |
        | basic_folder    |
        | basic_dayone    |

    Scenario Outline: -s displays the short version of entries (only the title)
        Given we use the config "<config>.yaml"
        And we use the password "test" if prompted
        When we run "jrnl -on 2020-08-31 -s"
        Then the output should be "2020-08-31 14:32 A second entry in what I hope to be a long series."

        Examples: configs
        | config          |
        | basic_onefile   |
        | basic_encrypted |
        | basic_folder    |
        | basic_dayone    |

    Scenario: Markdown Support from config file
        Given we use the config "format_md.yaml"
        When we run "jrnl -n 1"
        Then the output should be
            """
            # 2013

            ## June

            ### 2013-06-10 15:40 Life is good.

            But I'm better.
            """

    Scenario: Text Formatter from config file
        Given we use the config "format_text.yaml"
        When we run "jrnl -n 1"
        Then the output should be
            """
            [2013-06-10 15:40] Life is good.
            But I'm better.
            """

    Scenario Outline: Exporting entries with Cyrillic characters to directory should not fail
        Given we use the config "<config>.yaml"
        And we use the password "test" if prompted
        And we create a cache directory
        When we run "jrnl 2020-11-21: Первая"
        When we run "jrnl --format md --file {cache_dir} -on 2020-11-21"
        Then the cache should contain the files
        """
        2020-11-21_первая.md
        """

        Examples: configs
        | config          |
        | basic_onefile   |
        | basic_encrypted |
        | basic_folder    |
        | basic_dayone    |

    Scenario Outline: Export date counts
        Given we use the config "<config>.yaml"
        And we use the password "test" if prompted
        When we run "jrnl 2020-08-31 01:01: Hi."
        And we run "jrnl --format dates"
        Then the output should be
        """
        2020-08-29, 1
        2020-08-31, 2
        2020-09-24, 1
        """

        Examples: configs
        | config          |
        | basic_onefile   |
        | basic_encrypted |
        | basic_folder    |
        | basic_dayone    |
