# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

Feature: Upgrading Journals from 1.x.x to 2.x.x

    Scenario: Upgrade and parse journals with square brackets
        Given we use the config "upgrade_from_195.json"
        When we run "jrnl -9" and enter "Y"
        When we run "jrnl -99 --short"
        Then the output should be
            """
            2010-06-10 15:00 A life without chocolate is like a bad analogy.
            2013-06-10 15:40 He said "[this] is the best time to be alive".
            """
        And the output should contain
            """
            2010-06-10 15:00 A life without chocolate is like a bad analogy.
            """
        And the output should contain
            """
            2013-06-10 15:40 He said "[this] is the best time to be alive".
            """
        When we run "jrnl --format json"
        Then we should get no error
        And the output should be valid JSON
        Given we parse the output as JSON
        # The bracketed '[2019-08-03 12:55] Some chat log or something' line below
        # correctly ends up as body text of the entry above it, not a separate
        # entry. The bracketed-date format postdates jrnl 1.x, so a genuine v1
        # journal can never contain a real bracket-dated entry - any line
        # starting with '[' must be literal content the user typed. Treating it
        # as a new entry would be wrong, so LegacyJournal._parse folds it into
        # the current entry's body, escaping it with a leading space so the
        # re-serialized (bracketed) file won't have this line misread as an
        # entry boundary if it's ever reopened.
        Then "entries" in the parsed output should have 2 elements
        And "entries.0.title" in the parsed output should be
            """
            A life without chocolate is like a bad analogy.
            """
        And "entries.0.body" in the parsed output should have 0 elements
        And "entries.1.title" in the parsed output should be
            """
            He said "[this] is the best time to be alive".
            """
        And "entries.1.body" in the parsed output should be
            """
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent malesuada
            quis est ac dignissim. Aliquam dignissim rutrum pretium. Phasellus pellentesque
            augue et venenatis facilisis.

             [2019-08-03 12:55] Some chat log or something

            Suspendisse potenti. Sed dignissim sed nisl eu consequat. Aenean ante ex,
            elementum ut interdum et, mattis eget lacus. In commodo nulla nec tellus
            placerat, sed ultricies metus bibendum. Duis eget venenatis erat. In at dolor
            dui.
            """

    Scenario: Upgrading a journal encrypted with jrnl 1.x
        Given we use the config "encrypted_old.json"
        When we run "jrnl -n 1" and enter
            """
            Y
            bad doggie no biscuit
            bad doggie no biscuit
            """
        Then we should be prompted for a password
        And the output should contain "2013-06-10 15:40 Life is good"

    Scenario: Upgrading a config without colors to colors
        Given we use the config "no_colors.yaml"
        When we run "jrnl -n 1"
        Then the config should contain
            """
            colors:
                date: none
                title: none
                body: none
                tags: none
            """

    Scenario: Displaying a tagged entry should not crash when the colors config is missing the tags key
        Given we use the config "missing_tags_color.yaml"
        When we run "jrnl -n 1"
        Then we should get no error
        And the output should contain "I met with @dan"

    Scenario: Upgrade and parse journals with little endian date format
        Given we use the config "upgrade_from_195_little_endian_dates.json"
        When we run "jrnl -9 --short" and enter "Y"
        Then the output should contain
            """
            10.06.2010 15:00 A life without chocolate is like a bad analogy.
            10.06.2013 15:40 He said "[this] is the best time to be alive".
            """

    Scenario: Upgrade with missing journal
        Given we use the config "upgrade_from_195_with_missing_journal.json"
        When we run "jrnl --list" and enter "Y"
        Then the output should contain "features/journals/missing.journal does not exist"
        And we should get no error

    Scenario: Upgrade with missing encrypted journal
        Given we use the config "upgrade_from_195_with_missing_encrypted_journal.json"
        When we run "jrnl --list" and enter
            """
            Y
            bad doggie no biscuit
            """
        Then the output should contain "features/journals/missing.journal does not exist"
        And the output should contain "We're all done"
        And we should get no error
