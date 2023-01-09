# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

Feature: Multiple journals

    Scenario: Loading a config with two journals
        Given we use the config "multiple.yaml"
        When we run "jrnl -99 --short"
        Then the output should be
            2013-06-09 15:39 My first entry.
            2013-06-10 15:40 Life is good.
        When we run "jrnl work -99 --short"
        Then the output should be empty

    Scenario: Write to default config by default
        Given we use the config "multiple.yaml"
        When we run "jrnl this goes to default"
        When we run "jrnl -99 --short"
        Then the output should contain
            2013-06-09 15:39 My first entry.
            2013-06-10 15:40 Life is good.
        Then the output should contain
            this goes to default
        When we run "jrnl work -99 --short"
        Then the output should be empty

    Scenario: Write to specified journal
        Given we use the config "multiple.yaml"
        When we run "jrnl work a long day in the office"
        When we run "jrnl -99 --short"
        Then the output should be
            2013-06-09 15:39 My first entry.
            2013-06-10 15:40 Life is good.
        When we run "jrnl work -99 --short"
        Then the output should contain "a long day in the office"

    Scenario: Tell user which journal was used
        Given we use the config "multiple.yaml"
        When we run "jrnl work a long day in the office"
        Then the output should contain "Entry added to work journal"

    Scenario: Write to specified journal with a timestamp
        Given we use the config "multiple.yaml"
        When we run "jrnl work 23 july 2012: a long day in the office"
        When we run "jrnl -99 --short"
        Then the output should be
            2013-06-09 15:39 My first entry.
            2013-06-10 15:40 Life is good.
        When we run "jrnl work -99 --short"
        Then the output should be
            2012-07-23 09:00 a long day in the office

    Scenario: Write to specified journal without a timestamp but with colon
        Given we use the config "multiple.yaml"
        When we run "jrnl work : a long day in the office"
        Then the output should be
            2013-06-09 15:39 My first entry.
            2013-06-10 15:40 Life is good.
        When we run "jrnl work -99 --short"
        Then the output should be contain
            a long day in the office

    Scenario: Write to specified journal without a timestamp but with colon
        Given we use the config "multiple.yaml"
        When we run "jrnl work: a long day in the office"
        When we run "jrnl -99 --short"
        Then the output should be
            2013-06-09 15:39 My first entry.
            2013-06-10 15:40 Life is good.
        When we run "jrnl work -99 --short"
        Then the output should contain
            a long day in the office

   Scenario: Create new journals as required
        Given we use the config "multiple.yaml"
        Then journal "ideas" should not exist
        When we run "jrnl ideas 23 july 2012: sell my junk on ebay and make lots of money"
        When we run "jrnl ideas -99 --short"
        Then the output should be
            2012-07-23 09:00 sell my junk on ebay and make lots of money

   Scenario: Don't crash if no default journal is specified
        Given we use the config "no_default_journal.yaml"
        When we run "jrnl a long day in the office"
        Then the output should contain "No 'default' journal configured"

   Scenario: Don't crash if no file exists for a configured encrypted journal
        Given we use the config "multiple.yaml"
        When we run "jrnl new_encrypted Adding first entry" and enter
            these three eyes
            these three eyes
            n
        Then the output should contain "Journal 'new_encrypted' created at"

   Scenario: Read and write to journal with emoji name
        Given we use the config "multiple.yaml"
        When we run "jrnl ✨ Adding entry to sparkly journal"
        When we run "jrnl ✨ -1"
        Then the output should contain "Adding entry to sparkly journal"
