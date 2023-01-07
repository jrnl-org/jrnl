# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

Feature: Searching in a journal

    Scenario Outline: Displaying entries using -on today should display entries created today
        Given we use the config "<config_file>"
        When we run "jrnl today: Adding an entry right now."
        Then we should get no error
        When we run "jrnl -on today"
        Then the output should contain "Adding an entry right now."
        But the output should not contain "Everything is alright"
        And the output should not contain "Life is good"

        Examples: configs
        | config_file       |
        | simple.yaml       |
        | empty_folder.yaml |
        | dayone.yaml       |

    Scenario Outline: Displaying entries using -from day should display correct entries
        Given we use the config "<config_file>"
        When we run "jrnl yesterday: This thing happened yesterday"
        Then we should get no error
        When we run "jrnl today at 11:59pm: Adding an entry right now."
        Then we should get no error
        When we run "jrnl tomorrow: A future entry."
        Then we should get no error
        When we run "jrnl -from today"
        Then the output should contain "2 entries found" 
        And the output should contain "Adding an entry right now."
        And the output should contain "A future entry."
        And the output should not contain "This thing happened yesterday"

        Examples: configs
        | config_file       |
        | simple.yaml       |
        | empty_folder.yaml |
        | dayone.yaml       |

    Scenario Outline: Displaying entries using -from and -to day should display correct entries
        Given we use the config "<config_file>"
        And now is "2022-03-10 02:32:00 PM"
        When we run "jrnl yesterday: This thing happened yesterday"
        Then we should get no error
        When we run "jrnl today at 11:59pm: Adding an entry right now."
        Then we should get no error
        When we run "jrnl tomorrow: A future entry."
        Then we should get no error
        When we run "jrnl -from yesterday -to today"
        Then the output should contain "2 entries found"
        And the output should contain "This thing happened yesterday"
        And the output should contain "Adding an entry right now."
        And the output should not contain "A future entry."

        Examples: configs
        | config_file       |
        | simple.yaml       |
        | empty_folder.yaml |
        | dayone.yaml       |

    Scenario Outline: Searching for a string
        Given we use the config "<config_file>"
        When we run "jrnl -contains first --short"
        Then we should get no error
        And the output should contain "1 entry found"
        And the output should be
            2020-08-29 11:11 Entry the first.

        Examples: configs
        | config_file   |
        | basic_onefile.yaml |
        | basic_folder.yaml  |
        | basic_dayone.yaml  |

    Scenario Outline: Searching for an unknown string
        Given we use the config "<config_file>"
        When we run "jrnl -contains slkdfsdkfjsd"
        Then we should get no error
        And the output should contain "no entries found"
        And the output should not contain "slkdfsdkfjsd"

        Examples: configs
        | config_file        |
        | basic_onefile.yaml |
        | basic_folder.yaml  |
        | basic_dayone.yaml  |

    Scenario Outline: Searching for a string within tag results
        Given we use the config "<config_file>"
        When we run "jrnl @tagone -contains maybe"
        Then we should get no error
        And the output should contain "maybe"

        Examples: configs
        | config_file        |
        | basic_onefile.yaml |
        | basic_folder.yaml  |
        | basic_dayone.yaml  |

    Scenario Outline: Searching for a string within AND tag results
        Given we use the config "<config_file>"
        When we run "jrnl -and @tagone @tagtwo -contains maybe"
        Then we should get no error
        And the output should contain "1 entry found"
        And the output should contain "maybe"

        Examples: configs
        | config_file        |
        | basic_onefile.yaml |
        | basic_folder.yaml  |
        | basic_dayone.yaml  |

    Scenario Outline: Searching for a string within NOT tag results
        Given we use the config "<config_file>"
        When we run "jrnl -not @tagone -contains lonesome"
        Then we should get no error
        And the output should contain "1 entry found"
        And the output should contain "lonesome"

        Examples: configs
        | config_file        |
        | basic_onefile.yaml |
        | basic_folder.yaml  |
        | basic_dayone.yaml  |

    Scenario Outline: Searching for dates
        Given we use the config "<config_file>"
        When we run "jrnl -on 2020-08-31 --short"
        Then the output should be "2020-08-31 14:32 A second entry in what I hope to be a long series."
        When we run "jrnl -on 'august 31 2020' --short"
        Then the output should be "2020-08-31 14:32 A second entry in what I hope to be a long series."

        Examples: configs
        | config_file   |
        | basic_onefile.yaml |
        | basic_folder.yaml  |
        | basic_dayone.yaml  |

    Scenario: Out of order entries to a Folder journal should be listed in date order
        Given we use the config "empty_folder.yaml"
        When we run "jrnl 3/7/2014 4:37pm: Second entry of journal."
        Then we should get no error
        When we run "jrnl 23 July 2013: Testing folder journal."
        Then we should get no error
        When we run "jrnl -2"
        Then the output should be
            2013-07-23 09:00 Testing folder journal.

            2014-03-07 16:37 Second entry of journal.

    Scenario Outline: Searching for all tags should show counts of each tag
        Given we use the config "<config_file>"
        When we run "jrnl --tags"
        Then we should get no error
        And the output should be
            @tagtwo              : 2
            @tagone              : 2
            @tagthree            : 1
            @ipsum               : 1

        Examples: configs
        | config_file   |
        | basic_onefile.yaml |
        | basic_folder.yaml  |
        | basic_dayone.yaml  |

    Scenario Outline: Filtering journals should also filter tags
        Given we use the config "<config_file>"
        When we run "jrnl -from 'september 2020' --tags"
        Then we should get no error
        And the output should be
            @tagthree            : 1
            @tagone              : 1

        Examples: configs
        | config_file   |
        | basic_onefile.yaml |
        | basic_folder.yaml  |
        | basic_dayone.yaml  |

    Scenario Outline:  Excluding a tag should filter out all entries with that tag
        Given we use the config "<config_file>"
        When we run "jrnl --tags -not @tagtwo"
        Then the output should be
            @tagthree            : 1
            @tagone              : 1

        Examples: configs
        | config_file   |
        | basic_onefile.yaml |
        | basic_folder.yaml  |
        | basic_dayone.yaml  |

    Scenario Outline:  Excluding multiple tags should filter out all entries with those tags
        Given we use the config "<config_file>"
        When we run "jrnl --tags -not @tagone -not @tagthree"
        Then the output should be
            @tagtwo              : 1

        Examples: configs
        | config_file   |
        | basic_onefile.yaml |
        | basic_folder.yaml  |
        | basic_dayone.yaml  |

    Scenario Outline:  Using -not should exclude all entries with that tag
        # https://github.com/jrnl-org/jrnl/issues/1472
        Given we use the config "<config_file>"
        When we run "jrnl -not @tagtwo"
        Then the output should not contain "@tagtwo"
        And the editor should not have been called

        Examples: configs
        | config_file   |
        | basic_onefile.yaml |
        | basic_folder.yaml  |
        | basic_dayone.yaml  |

    Scenario: DayOne tag searching should work with tags containing a mixture of upper and lower case.
        # https://github.com/jrnl-org/jrnl/issues/354
        Given we use the config "dayone.yaml"
        When we run "jrnl @plAy"
        Then the output should contain "2013-05-17 11:39 This entry has tags!"

    Scenario: Loading a sample journal
        Given we use the config "simple.yaml"
        When we run "jrnl -2"
        Then we should get no error
        And the output should be
            2013-06-09 15:39 My first entry.
            | Everything is alright

            2013-06-10 15:40 Life is good.
            | But I'm better.

    Scenario Outline: Searching by month
        Given we use the config "<config_file>"
        And we use the password "test" if prompted
        When we run "jrnl -month 9 --short"
        Then the output should be "2020-09-24 09:14 The third entry finally after weeks without writing."
        When we run "jrnl -month Sept --short"
        Then the output should be "2020-09-24 09:14 The third entry finally after weeks without writing."
        When we run "jrnl -month September --short"
        Then the output should be "2020-09-24 09:14 The third entry finally after weeks without writing."

        Examples: configs
        | config_file          |
        | basic_onefile.yaml   |
        | basic_encrypted.yaml |
        | basic_folder.yaml    |
        | basic_dayone.yaml    |

    Scenario Outline: Searching by day
        Given we use the config "<config_file>"
        And we use the password "test" if prompted
        When we run "jrnl -day 31 --short"
        Then the output should be "2020-08-31 14:32 A second entry in what I hope to be a long series."

        Examples: configs
        | config_file          |
        | basic_onefile.yaml   |
        | basic_encrypted.yaml |
        | basic_folder.yaml    |
        | basic_dayone.yaml    |

    Scenario Outline: Searching by year
        Given we use the config "<config_file>"
        And we use the password "test" if prompted
        When we run "jrnl 2019-01-01 01:01: I like this year."
        And we run "jrnl -year 2019 --short"
        Then the output should be "2019-01-01 01:01 I like this year."
        When we run "jrnl -year 19 --short"
        Then the output should be "2019-01-01 01:01 I like this year."

        Examples: configs
        | config_file          |
        | basic_onefile.yaml   |
        | basic_encrypted.yaml |
        | basic_folder.yaml    |
        | basic_dayone.yaml    |

    Scenario Outline: Combining month, day, and year search terms
        Given we use the config "<config_file>"
        And we use the password "test" if prompted
        When we run "jrnl -month 08 -day 29 --short"
        Then the output should be "2020-08-29 11:11 Entry the first."
        When we run "jrnl -day 29 -year 2020 --short"
        Then the output should be "2020-08-29 11:11 Entry the first."
        When we run "jrnl -month 09 -year 2020 --short"
        Then the output should be "2020-09-24 09:14 The third entry finally after weeks without writing."
        When we run "jrnl -month 08 -day 29 -year 2020 --short"
        Then the output should be "2020-08-29 11:11 Entry the first."

        Examples: configs
        | config_file          |
        | basic_onefile.yaml   |
        | basic_encrypted.yaml |
        | basic_folder.yaml    |
        | basic_dayone.yaml    |

    Scenario Outline: Searching today in history
        Given we use the config "<config_file>"
        And we use the password "test" if prompted
        And now is "2020-08-31 02:32:00 PM"
        When we run "jrnl 2019-08-31 01:01: Hi, from last year."
        And we run "jrnl -today-in-history --short"
        Then the output should contain "2 entries found"
        And the output should be
            2019-08-31 01:01 Hi, from last year.
            2020-08-31 14:32 A second entry in what I hope to be a long series.

        Examples: configs
        | config_file          |
        | basic_onefile.yaml   |
        | basic_encrypted.yaml |
        | basic_folder.yaml    |
        | basic_dayone.yaml    |

    Scenario: Loading a DayOne Journal
        Given we use the config "dayone.yaml"
        When we run "jrnl -from 'feb 2013'"
        Then we should get no error
        And the output should contain "3 entries found"
        And the output should be
            2013-05-17 11:39 This entry has tags!

            2013-06-17 20:38 This entry has a location.

            2013-07-17 11:38 This entry is starred!
