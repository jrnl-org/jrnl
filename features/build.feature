Feature: Build process

    @deployment_tests
    Scenario: Version numbers should stay in sync
        Given we use the config "simple.yaml"
        When we run "jrnl --version"
        Then we should get no error
        And the output should contain pyproject.toml version
