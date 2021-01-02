import textwrap

from jrnl.exception import JrnlError


def test_config_directory_exception_message():
    ex = JrnlError(
        "ConfigDirectoryIsFile", config_directory_path="/config/directory/path"
    )

    assert ex.message == textwrap.dedent(
        """
        The path to your jrnl configuration directory is a file, not a directory:
        
        /config/directory/path
        
        Removing this file will allow jrnl to save its configuration.
		"""
    )
