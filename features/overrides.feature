Feature: Implementing Runtime Overrides for Select Configuration Keys

Scenario: Override configured editor with built-in input === editor:''
Given we use the config "editor-args.yaml"
When we run "jrnl --override '{\"editor\": \"\""}'"
Then the editor "" should have been called 

Scenario: Override configured editor with 'nano'
Given we use the config "editor.yaml" 
When we run "jrnl --override '{\"editor\": \"nano\"}'"
Then the editor "nano" should have been called

Scenario: Override configured linewrap with a value of 23
Given we use the config "editor.yaml"
When we run "jrnl -2 --override '{"linewrap": 23}' --format fancy"
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