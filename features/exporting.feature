Feature: Exporting a Journal

    Scenario: Exporting to json
        Given we use the config "tags.yaml"
        When we run "jrnl --export json"
        Then we should get no error
        and the output should be parsable as json
        and "entries" in the json output should have 2 elements
        and "tags" in the json output should contain "@idea"
        and "tags" in the json output should contain "@journal"
        and "tags" in the json output should contain "@dan"

    Scenario: Exporting using filters should only export parts of the journal
        Given we use the config "tags.yaml"
        When we run "jrnl -until 'may 2013' --export json"
        # Then we should get no error
        Then the output should be parsable as json
        and "entries" in the json output should have 1 element
        and "tags" in the json output should contain "@idea"
        and "tags" in the json output should contain "@journal"
        and "tags" in the json output should not contain "@dan"

    Scenario: Exporting dayone to json
        Given we use the config "dayone.yaml"
        When we run "jrnl --export json"
        Then we should get no error
        and the output should be parsable as json
        and the json output should contain entries.0.uuid = "4BB1F46946AD439996C9B59DE7C4DDC1"
