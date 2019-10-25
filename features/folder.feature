Feature: Testing a journal with a root directory and multiple files in the format of yyyy/mm/dd.txt

    Scenario: Opening an folder that's not a DayOne folder should treat as folder journal
        Given we use the config "empty_folder.yaml"
        When we run "jrnl 23 july 2013: Testing folder journal."
        Then we should see the message "Entry added"
        When we run "jrnl -1"
        Then the output should be 
            """
            2013-07-23 09:00 Testing folder journal.
            """

    Scenario: Adding entries to a Folder journal should generate date files
      Given we use the config "empty_folder.yaml"
      When we run "jrnl 23 July 2013: Testing folder journal."
      Then we should see the message "Entry added"
      When the journal directory is listed
      Then the output should contain "2013/07/23.txt"


    Scenario: Adding multiple entries to a Folder journal should generate multiple date files
      Given we use the config "empty_folder.yaml"
      When we run "jrnl 23 July 2013: Testing folder journal."
      And we run "jrnl 3/7/2014: Second entry of journal."
      Then we should see the message "Entry added"
      When the journal directory is listed
      Then the output should contain "2013/07/23.txt"
      And the output should contain "2014/03/07.txt"


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
