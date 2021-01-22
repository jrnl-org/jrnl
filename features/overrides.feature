Feature: Implementing Runtime Overrides for Select Configuration Keys

Scenario: Override configured editor with built-in input === editor:''
Given we use the config "editor-args.yaml"
When we run "jrnl --override '{\"editor\": \"\"}'"
Then the editor "" should have been called 