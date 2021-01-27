Feature: Implementing Runtime Overrides for Select Configuration Keys

        Scenario: Override configured editor with built-in input === editor:''
        Given we use the config "tiny.yaml"
        When we run jrnl with --config-override editor:''
        Then the stdin prompt must be launched 

        @skip_win
        Scenario: Override configured linewrap with a value of 23
        Given we use the config "tiny.yaml"
        When we run "jrnl  -2 --config-override linewrap:23 --format fancy"
        Then the output should be

        """
        ┎─────╮2013-06-09 15:39
        ┃ My  ╘═══════════════╕
        ┃ fir st  ent ry.     │
        ┠╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤
        ┃ Everything is       │
        ┃ alright             │
        ┖─────────────────────┘
        ┎─────╮2013-06-10 15:40
        ┃ Lif ╘═══════════════╕
        ┃ e is  goo d.        │
        ┠╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┤
        ┃ But I'm better.     │
        ┖─────────────────────┘
        """

        @skip_win
        @wip
        Scenario: Override color selections with runtime overrides 
        Given we use the config "tiny.yaml"
        When we run jrnl with -1 --config-override colors.body:blue
        Then the runtime config should have colors.body set to blue

        @skip_win 
        Scenario: Apply multiple config overrides 
        Given we use the config "tiny.yaml" 
        When we run jrnl with -1 --config-override colors.body:green,editor:"nano"
        Then the runtime config should have colors.body set to green 
        And the runtime config should have editor set to nano


        Scenario Outline: Override configured editor
        Given we use the config "tiny.yaml" 
        When we run jrnl with --config-override editor:"<editor>"
        Then the editor <editor> should have been called
        Examples: Editor Commands
        | editor            |
        | nano              |
        | vi -c startinsert | 
        | code -w -         | 
