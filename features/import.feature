Feature: Importing data

    Scenario: --import allows new entry from stdin
      Given we use the config "basic.yaml"
      When we run "jrnl --import" and pipe "[2020-07-05 15:00] Observe and import."
      And we run "jrnl -1"
      Then the journal should contain "[2020-07-05 15:00] Observe and import."
      And the output should contain "Observe and import"

    Scenario: --import allows new large entry from stdin
      Given we use the config "basic.yaml"
      When we run "jrnl --import" and pipe
      """
      [2020-07-05 15:00] Observe and import.
      Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent malesuada quis
      est ac dignissim. Aliquam dignissim rutrum pretium. Phasellus pellentesque augue
      et venenatis facilisis. Suspendisse potenti. Sed dignissim sed nisl eu consequat.
      Aenean ante ex, elementum ut interdum et, mattis eget lacus. In commodo nulla nec
      tellus placerat, sed ultricies metus bibendum. Duis eget venenatis erat. In at
      dolor dui end of entry.
      """
      And we run "jrnl -1"
      Then the journal should contain "[2020-07-05 15:00] Observe and import."
      And the output should contain "Observe and import"
      And the output should contain "Lorem ipsum"
      And the output should contain "end of entry."

    Scenario: --import allows multiple new entries from stdin
      Given we use the config "basic.yaml"
      When we run "jrnl --import" and pipe
      """
      [2020-07-05 15:00] Observe and import.
      Lorem ipsum dolor sit amet, consectetur adipiscing elit.

      [2020-07-05 15:01] Twice as nice.
      Sed dignissim sed nisl eu consequat.
      """
      Then the journal should contain "[2020-07-05 15:00] Observe and import."
      Then the journal should contain "[2020-07-05 15:01] Twice as nice."

    Scenario: --import allows import new entries from file
      Given we use the config "basic.yaml"
      Then the journal should contain "My first entry."
      And the journal should contain "Life is good."
      But the journal should not contain "I have an @idea"
      And the journal should not contain "I met with"
      When we run "jrnl --import --file features/journals/tags.journal"
      Then the journal should contain "My first entry."
      And the journal should contain "Life is good."
      And the journal should contain "PROFIT!"

    Scenario: --import prioritizes --file over pipe data if both are given
      Given we use the config "basic.yaml"
      Then the journal should contain "My first entry."
      And the journal should contain "Life is good."
      But the journal should not contain "I have an @idea"
      And the journal should not contain "I met with"
      When we run "jrnl --import --file features/journals/tags.journal" and pipe
      """
      [2020-07-05 15:00] I should not exist!
      """
      Then the journal should contain "My first entry."
      And the journal should contain "PROFIT!"
      But the journal should not contain "I should not exist!"

