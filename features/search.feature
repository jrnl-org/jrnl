Feature: Searching in a journal

    Scenario Outline: Displaying entries using -on today should display entries created today
        Given we use the config "<config>.yaml"
        When we run "jrnl today: Adding an entry right now."
        Then we should see the message "Entry added"
        When we run "jrnl -on today"
        Then the output should contain "Adding an entry right now."
        But the output should not contain "Everything is alright"
        And the output should not contain "Life is good"

        Examples: configs
        | config       |
        | simple       |
        | empty_folder |
        | dayone       |

    Scenario Outline: Displaying entries using -from day should display correct entries
        Given we use the config "<config>.yaml"
        When we run "jrnl yesterday: This thing happened yesterday"
        Then we should see the message "Entry added"
        When we run "jrnl today at 11:59pm: Adding an entry right now."
        Then we should see the message "Entry added"
        When we run "jrnl tomorrow: A future entry."
        Then we should see the message "Entry added"
        When we run "jrnl -from today"
        Then the output should contain "Adding an entry right now."
        And the output should contain "A future entry."
        And the output should not contain "This thing happened yesterday"

        Examples: configs
        | config       |
        | simple       |
        | empty_folder |
        | dayone       |

    Scenario Outline: Displaying entries using -from and -to day should display correct entries
        Given we use the config "<config>.yaml"
        When we run "jrnl yesterday: This thing happened yesterday"
        Then we should see the message "Entry added"
        When we run "jrnl today at 11:59pm: Adding an entry right now."
        Then we should see the message "Entry added"
        When we run "jrnl tomorrow: A future entry."
        Then we should see the message "Entry added"
        When we run "jrnl -from yesterday -to today"
        Then the output should contain "This thing happened yesterday"
        And the output should contain "Adding an entry right now."
        And the output should not contain "A future entry."

        Examples: configs
        | config       |
        | simple       |
        | empty_folder |
        | dayone       |

    Scenario Outline: Searching for a string
        Given we use the config "<config>.yaml"
        When we run "jrnl -contains first --short"
        Then we should get no error
        And the output should be
        """
        2020-08-29 11:11 Entry the first.
        """

        Examples: configs
        | config        |
        | basic_onefile |
        | basic_folder  |
        | basic_dayone  |

    Scenario Outline: Searching for a string within tag results
        Given we use the config "<config>.yaml"
        When we run "jrnl @tagone -contains maybe"
        Then we should get no error
        And the output should contain "maybe"

        Examples: configs
        | config        |
        | basic_onefile |
        | basic_folder  |
        | basic_dayone  |

    Scenario Outline: Searching for a string within AND tag results
        Given we use the config "<config>.yaml"
        When we run "jrnl -and @tagone @tagtwo -contains maybe"
        Then we should get no error
        And the output should contain "maybe"

        Examples: configs
        | config        |
        | basic_onefile |
        | basic_folder  |
        | basic_dayone  |

    Scenario Outline: Searching for a string within NOT tag results
        Given we use the config "<config>.yaml"
        When we run "jrnl -not @tagone -contains lonesome"
        Then we should get no error
        And the output should contain "lonesome"

        Examples: configs
        | config        |
        | basic_onefile |
        | basic_folder  |
        | basic_dayone  |

    Scenario Outline: Searching for dates
        Given we use the config "<config>.yaml"
        When we run "jrnl -on 2020-08-31 --short"
        Then the output should be "2020-08-31 14:32 A second entry in what I hope to be a long series."
        Then we flush the output
        When we run "jrnl -on 'august 31 2020' --short"
        Then the output should be "2020-08-31 14:32 A second entry in what I hope to be a long series."

        Examples: configs
        | config        |
        | basic_onefile |
        | basic_folder  |
        | basic_dayone  |

    Scenario: Out of order entries to a Folder journal should be listed in date order
        Given we use the config "empty_folder.yaml"
        When we run "jrnl 3/7/2014 4:37pm: Second entry of journal."
        Then we should see the message "Entry added"
        When we run "jrnl 23 July 2013: Testing folder journal."
        Then we should see the message "Entry added"
        When we run "jrnl -2"
        Then the output should be
        """
        2013-07-23 09:00 Testing folder journal.

        2014-03-07 16:37 Second entry of journal.
        """

    Scenario Outline: Searching for all tags should show counts of each tag
        Given we use the config "<config>.yaml"
        When we run "jrnl --tags"
        Then we should get no error
        And the output should be
        """
        @tagtwo              : 2
        @tagone              : 2
        @tagthree            : 1
        @ipsum               : 1
        """

        Examples: configs
        | config        |
        | basic_onefile |
        | basic_folder  |
        | basic_dayone  |

    Scenario Outline: Filtering journals should also filter tags
        Given we use the config "<config>.yaml"
        When we run "jrnl -from 'september 2020' --tags"
        Then we should get no error
        And the output should be
        """
        @tagthree            : 1
        @tagone              : 1
        """

        Examples: configs
        | config        |
        | basic_onefile |
        | basic_folder  |
        | basic_dayone  |

    Scenario Outline:  Excluding a tag should filter out all entries with that tag
        Given we use the config "<config>.yaml"
        When we run "jrnl --tags -not @tagtwo"
        Then the output should be
        """
        @tagthree            : 1
        @tagone              : 1
        """

        Examples: configs
        | config        |
        | basic_onefile |
        | basic_folder  |
        | basic_dayone  |

    Scenario Outline:  Excluding multiple tags should filter out all entries with those tags
        Given we use the config "<config>.yaml"
        When we run "jrnl --tags -not @tagone -not @tagthree"
        Then the output should be
        """
        @tagtwo              : 1
        """

        Examples: configs
        | config        |
        | basic_onefile |
        | basic_folder  |
        | basic_dayone  |

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
        """
        2013-06-09 15:39 My first entry.
        | Everything is alright

        2013-06-10 15:40 Life is good.
        | But I'm better.
        """

    Scenario Outline: Searching by month, day, or year
        Given we use the config "dates_similar.yaml"
        When we run "jrnl <args>"
        Then the output should be
        """
        <entry1>

        <entry2>
        """
        Examples: month
        | args            | entry1               | entry2               |
        | -month 2        | 2018-02-04 06:04 Hi. | 2020-02-05 12:10 Hi. |
        | -month 02        | 2018-02-04 06:04 Hi. | 2020-02-05 12:10 Hi. |
        | -month February | 2018-02-04 06:04 Hi. | 2020-02-05 12:10 Hi. |
        | -month Feb      | 2018-02-04 06:04 Hi. | 2020-02-05 12:10 Hi. |
        Examples: day
        | args   | entry1               | entry2               |
        | -day 5 | 2018-03-05 08:06 Hi. | 2020-02-05 12:10 Hi. |
        | -day 05 | 2018-03-05 08:06 Hi. | 2020-02-05 12:10 Hi. |
        Examples: year
        | args       | entry1               | entry2               |
        | -year 2018 | 2018-02-04 06:04 Hi. | 2018-03-05 08:06 Hi. |
        | -year 18   | 2018-02-04 06:04 Hi. | 2018-03-05 08:06 Hi. |
        Examples: combinations
        | args                       | entry1               | entry2                |
        | -month 1 -day 3            | 2019-01-03 10:08 Hi. | 2021-01-03 15:39 Hi.  |
        | -month 1 -year 2019        | 2019-01-03 10:08 Hi. | 2019-01-07 01:02 Hi.  |
        | -day 4 -year 2021          | 2021-01-04 10:21 Hi. | 2021-01-04 12:33 Hi.  |
        | -month 1 -day 4 -year 2021 | 2021-01-04 10:21 Hi. | 2021-01-04 12:33 Hi.  |

    Scenario: Reminiscing
        Given we use the config "dates_similar.yaml"
        And we set current date and time to "2021-01-03 15:39"
        When we run "jrnl -reminisce"
        Then the output should be
        """
        2019-01-03 10:08 Hi.

        2021-01-03 15:39 Hi.
        """
    
    Scenario: Loading a DayOne Journal
        Given we use the config "dayone.yaml"
        When we run "jrnl -from 'feb 2013'"
        Then we should get no error
        And the output should be
        """
        2013-05-17 11:39 This entry has tags!

        2013-06-17 20:38 This entry has a location.

        2013-07-17 11:38 This entry is starred!
        """
