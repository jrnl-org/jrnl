Feature: Implementing Runtime Overrides for Select Configuration Keys

Scenario: Override configured editor with built-in input === editor:''
Given we use the config "editor-args.yaml"
When we run "jrnl --config-override '{"editor": ""}'"
Then the editor "" should have been called 

Scenario: Override configured editor with 'nano'
Given we use the config "editor.yaml" 
When we run "jrnl --config-override '{"editor": "nano"}'"
Then the editor "nano" should have been called

@skip_win
Scenario: Override configured linewrap with a value of 23
Given we use the config "editor.yaml"
When we run "jrnl -2 --config-override '{"linewrap": 23}' --format fancy"
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
Scenario: Override color selections with runtime overrides 
Given we use the config "tiny.yaml"
When we run jrnl with -1 --config-override '{"colors.body": "blue"}' 
Then the runtime config should have colors.body set to blue

@skip_win 
Scenario: Apply multiple config overrides 
Given we use the config "tiny.yaml" 
When we run jrnl with -1 --config-override '{"colors.body": "green", "editor": "nano"}'
Then the runtime config should have colors.body set to green 
And the runtime config should have editor set to nano
