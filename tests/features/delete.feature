Feature: Delete entries from journal
    Scenario Outline: Delete flag allows deletion of single entry
        Given we use the config "<config_file>"
        And we use the password "test" if prompted
        When we run "jrnl -1"
        Then the output should contain "2020-09-24 09:14 The third entry finally"
        When we run "jrnl --delete" and enter
            N
            N
            Y
        When we run "jrnl -99 --short"
        Then the output should be
            2020-08-29 11:11 Entry the first.
            2020-08-31 14:32 A second entry in what I hope to be a long series.

        Examples: Configs
        | config_file          |
        | basic_onefile.yaml   |
        | basic_encrypted.yaml |
        # | basic_folder.yaml    | @todo
        # | basic_dayone.yaml    | @todo
 
    Scenario Outline: Backing out of interactive delete does not change journal
        Given we use the config "<config_file>"
        When we run "jrnl --delete -n 1" and enter
            N
        When we run "jrnl -99 --short"
        Then the output should be
            2020-08-29 11:11 Entry the first.
            2020-08-31 14:32 A second entry in what I hope to be a long series.
            2020-09-24 09:14 The third entry finally after weeks without writing.

        Examples: Configs
        | config_file        |
        | basic_onefile.yaml |
        | basic_folder.yaml  |
        | basic_dayone.yaml  |

 
    Scenario Outline: Delete flag with nonsense input deletes nothing (issue #932)
        Given we use the config "<config_file>"
        When we run "jrnl --delete asdfasdf"
        When we run "jrnl -99 --short"
        Then the output should be
            2020-08-29 11:11 Entry the first.
            2020-08-31 14:32 A second entry in what I hope to be a long series.
            2020-09-24 09:14 The third entry finally after weeks without writing.

        Examples: Configs
        | config_file        |
        | basic_onefile.yaml |
        | basic_folder.yaml  |
        | basic_dayone.yaml  |