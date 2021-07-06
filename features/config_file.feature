Feature: Implementing usage of alternate configuration file

        Scenario: Use personal config stored in user's home folder
        Given we use config file path "work-config.yaml" by running
        `jrnl --config-file ~/work-config.yaml`, which contains valid
        configuration options for `jrnl`, the program should use
        configuration within the given configuration file specified.

        Scenario: Use not existing configuration file
        Given we use the config path "some-config.yaml" which does not point
        to an existing file program should exit with an error explaining the 
        situation. The output should be
        
        """
        Alternate configuration file not found at path specified.
        Exiting.
        """
