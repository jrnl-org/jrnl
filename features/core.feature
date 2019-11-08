Feature: Basic reading and writing to a journal

    Scenario: Loading a sample journal
        Given we use the config "basic.yaml"
        When we run "jrnl -n 2"
        Then we should get no error
        and the output should be
            """
            2013-06-09 15:39 My first entry.
            | Everything is alright

            2013-06-10 15:40 Life is good.
            | But I'm better.
            """

    Scenario: Printing a journal that has multiline entries
        Given we use the config "multiline.yaml"
        When we run "jrnl -n 1"
        Then we should get no error
        and the output should be
            """
            2013-06-09 15:39 Multiple line entry.
            | This is the first line.
            | This line doesn't have any ending punctuation
            |
            | There is a blank line above this.
            """

    Scenario: Printing a journal that has multiline entries with tags
        Given we use the config "multiline-tags.yaml"
        When we run "jrnl -n 1"
        Then we should get no error
        and the output should be
            """
            [2013-06-09 15:39] Multiple @line entry with @tags.
            | Tag with @punctuation. afterwards
            | @TagOnLineAloneWithOutPunctuation
            | @TagOnLineAloneWithPunctuation.
            | Text before @tag. And After.
            | @hi. Hello
            | hi Hello
            """

    Scenario: Writing an entry from command line
        Given we use the config "basic.yaml"
        When we run "jrnl 23 july 2013: A cold and stormy day. I ate crisps on the sofa."
        Then we should see the message "Entry added"
        When we run "jrnl -n 1"
        Then the output should contain "2013-07-23 09:00 A cold and stormy day."

    Scenario: Filtering for dates
        Given we use the config "basic.yaml"
        When we run "jrnl -on 2013-06-10 --short"
        Then the output should be "2013-06-10 15:40 Life is good."
        When we run "jrnl -on 'june 6 2013' --short"
        Then the output should be "2013-06-10 15:40 Life is good."

    Scenario: Emoji support
        Given we use the config "basic.yaml"
        When we run "jrnl 23 july 2013: 🌞 sunny day. Saw an 🐘"
        Then we should see the message "Entry added"
        When we run "jrnl -n 1"
        Then the output should contain "🌞"
        and the output should contain "🐘"

    Scenario: Writing an entry at the prompt
        Given we use the config "basic.yaml"
        When we run "jrnl" and enter "25 jul 2013: I saw Elvis. He's alive."
        Then we should get no error
        and the journal should contain "[2013-07-25 09:00] I saw Elvis."
        and the journal should contain "He's alive."

    Scenario: Displaying the version number
        Given we use the config "basic.yaml"
        When we run "jrnl -v"
        Then we should get no error
        Then the output should contain "version"

    Scenario: --short displays the short version of entries (only the title)
        Given we use the config "basic.yaml"
        When we run "jrnl -on 2013-06-10 --short"
        Then the output should be "2013-06-10 15:40 Life is good."

    Scenario: -s displays the short version of entries (only the title)
        Given we use the config "basic.yaml"
        When we run "jrnl -on 2013-06-10 -s"
        Then the output should be "2013-06-10 15:40 Life is good."

    Scenario: Invalid color configuration
        Given we use the config "invalid_color.yaml"
        When we run "jrnl -on 2013-06-10 -s"
        Then the output should be
        """
        2013-06-10 15:40 Life is good.
        """
        And we should get no error
