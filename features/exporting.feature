Feature: Expoting a Journal

    Scenario: Exporting to json
        Given we use the config "tags.json"
        When we run "jrnl --export json"
        Then we should get no error
        and the output should be
            """
            {
              "entries": [
                {
                  "body": "(1) write a command line @journal software\n(2) ???\n(3) PROFIT!",
                  "date": "2013-04-09",
                  "time": "15:39",
                  "title": "I have an @idea:"
                },
                {
                  "body": "As alway's he shared his latest @idea on how to rule the world with me.",
                  "date": "2013-06-10",
                  "time": "15:40",
                  "title": "I met with @dan."
                }
              ],
              "tags": {
                "@idea": 2,
                "@journal": 1,
                "@dan": 1
              }
            }
            """

        Scenario: Exporting using filters should only export parts of the journal
            Given we use the config "tags.json"
            When we run "jrnl -to 'may 2013' --export json"
            Then we should get no error
            and the output should be
                """
                {
                  "entries": [
                    {
                      "body": "(1) write a command line @journal software\n(2) ???\n(3) PROFIT!",
                      "date": "2013-04-09",
                      "time": "15:39",
                      "title": "I have an @idea:"
                    }
                  ],
                  "tags": {
                    "@idea": 1,
                    "@journal": 1
                  }
                }
                """
