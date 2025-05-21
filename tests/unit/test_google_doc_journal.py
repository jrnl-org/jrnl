# tests/unit/test_google_doc_journal.py
import unittest
from unittest.mock import patch, MagicMock, mock_open
import os # For path manipulations if needed in tests
import logging

# Assuming jrnl.journals.GoogleDocJournal can be imported
# This might require PYTHONPATH adjustments if running standalone,
# but pytest/unittest discovery should handle it in a project structure.
from jrnl.journals.GoogleDocJournal import GoogleDocJournal 
# We will mock jrnl.path.get_config_path used in GoogleDocJournal.__init__

# Mock HttpError if not easily importable or to simplify
# Based on googleapiclient.errors.HttpError
class MockHttpError(Exception):
    def __init__(self, resp_status, reason_phrase, content=b""):
        super().__init__(f"<{resp_status}> {reason_phrase}")
        self.resp = MagicMock()
        self.resp.status = resp_status
        self.resp.reason = reason_phrase # HttpError uses resp.reason
        self.content = content

    def _get_reason(self): # Match the method name in HttpError
        return self.resp.reason

# Suppress logging output during tests unless specifically testing for it
logging.disable(logging.CRITICAL)

class TestGoogleDocJournal(unittest.TestCase):

    def setUp(self):
        # Basic config for the journal
        self.mock_journal_name = "gdoc_test"
        self.base_config_dir = "/fake/config_dir" # Used by mock_get_config_path
        
        self.mock_config = {
            "type": "googledoc",
            "journal": "/fake/local_journal.txt", # Local backup file path
            "google_doc_id": "fake_doc_id",
            # Paths for token and credentials will be derived from base_config_dir
            # or overridden by specific config values if provided.
            "google_credentials_path": os.path.join(self.base_config_dir, "google_credentials.json"),
            "google_token_path": os.path.join(self.base_config_dir, "google_token.json"),
        }

        # Patch get_config_path used in GoogleDocJournal.__init__
        self.patch_get_config_path = patch('jrnl.journals.GoogleDocJournal.get_config_path')
        self.mock_get_config_path = self.patch_get_config_path.start()
        # Let get_config_path return the path to a dummy jrnl.yaml, so its dirname is base_config_dir
        self.mock_get_config_path.return_value = os.path.join(self.base_config_dir, "jrnl.yaml")

        # Patch external dependencies common to most tests
        self.patch_os_path_exists = patch('os.path.exists')
        self.mock_os_path_exists = self.patch_os_path_exists.start()

        self.patch_makedirs = patch('os.makedirs')
        self.mock_makedirs = self.patch_makedirs.start()
        
        self.patch_credentials_from_file = patch('jrnl.journals.GoogleDocJournal.Credentials.from_authorized_user_file')
        self.mock_credentials_from_file = self.patch_credentials_from_file.start()

        self.patch_credentials_refresh = patch('jrnl.journals.GoogleDocJournal.Credentials.refresh')
        # This needs to be attached to a mock Credentials instance, done in tests where creds are loaded

        self.patch_installed_app_flow = patch('jrnl.journals.GoogleDocJournal.InstalledAppFlow.from_client_secrets_file')
        self.mock_installed_app_flow = self.patch_installed_app_flow.start()
        
        self.patch_build = patch('jrnl.journals.GoogleDocJournal.build')
        self.mock_build = self.patch_build.start()

        self.patch_open = patch('builtins.open', new_callable=mock_open)
        self.mock_open_file = self.patch_open.start()
        
        self.patch_os_remove = patch('os.remove')
        self.mock_os_remove = self.patch_os_remove.start()

        # Default mock behaviors
        self.mock_os_path_exists.return_value = False # Default to no files existing
        self.mock_credentials_from_file.return_value = None # Default to no existing credentials
        
        self.mock_flow_instance = MagicMock()
        self.mock_installed_app_flow.return_value = self.mock_flow_instance
        
        self.mock_service_instance = MagicMock()
        self.mock_build.return_value = self.mock_service_instance
        
        # Mock for credentials.refresh()
        self.mock_creds_instance = MagicMock()


    def tearDown(self):
        self.patch_get_config_path.stop()
        self.patch_os_path_exists.stop()
        self.patch_makedirs.stop()
        self.patch_credentials_from_file.stop()
        # self.patch_credentials_refresh.stop() # Not started directly
        self.patch_installed_app_flow.stop()
        self.patch_build.stop()
        self.patch_open.stop()
        self.patch_os_remove.stop()
        logging.disable(logging.NOTSET) # Re-enable logging

    def _create_journal_instance(self, config_overrides=None):
        # Ensure base_config_dir exists for __init__ logic
        # In __init__, if jrnl_base_dir (derived from get_config_path) doesn't exist, it tries to create it.
        # Let's simulate it exists to prevent makedirs call for the base dir itself.
        def os_path_exists_side_effect(path):
            if path == self.base_config_dir:
                return True
            # Fallback to default for other paths (usually False unless overridden in test)
            return self.mock_os_path_exists.orig_return_value if hasattr(self.mock_os_path_exists, 'orig_return_value') else False
        
        # Store original return_value if needed, or use specific side_effects in tests.
        # For this generic instance creation, assume it's okay if it's just False for token/creds paths.
        # More specific side_effects for os.path.exists will be set in individual tests.

        current_config = self.mock_config.copy()
        if config_overrides:
            current_config.update(config_overrides)
        
        # Ensure derived paths are correct if base_config_dir changed
        if "google_credentials_path" not in (config_overrides or {}):
            current_config["google_credentials_path"] = os.path.join(self.base_config_dir, "google_credentials.json")
        if "google_token_path" not in (config_overrides or {}):
            current_config["google_token_path"] = os.path.join(self.base_config_dir, "google_token.json")
            
        return GoogleDocJournal(name=self.mock_journal_name, **current_config)

    def test_init_calls_initialize_service_if_doc_id_present(self):
        with patch.object(GoogleDocJournal, '_initialize_docs_service') as mock_init_service:
            self._create_journal_instance()
            mock_init_service.assert_called_once()

    def test_init_does_not_initialize_service_if_no_doc_id(self):
        with patch.object(GoogleDocJournal, '_initialize_docs_service') as mock_init_service:
            self._create_journal_instance(config_overrides={"google_doc_id": None})
            mock_init_service.assert_not_called()
            
    def test_initialize_service_loads_valid_token(self):
        token_path = self.mock_config["google_token_path"]
        self.mock_os_path_exists.side_effect = lambda path: path == token_path
        
        self.mock_creds_instance.valid = True
        self.mock_creds_instance.expired = False
        self.mock_creds_instance.refresh_token = "dummy_refresh_token" # Has a refresh token
        self.mock_credentials_from_file.return_value = self.mock_creds_instance
        
        journal = self._create_journal_instance()
        
        self.mock_credentials_from_file.assert_called_with(token_path, GoogleDocJournal.SCOPES)
        self.mock_build.assert_called_with("docs", "v1", credentials=self.mock_creds_instance, cache_discovery=False)
        self.assertIsNotNone(journal.docs_service)
        self.mock_installed_app_flow.assert_not_called() # Auth flow should not run
        self.mock_open_file.assert_not_called() # Token should not be re-saved

    def test_initialize_service_runs_auth_flow_if_no_token(self):
        # Simulate only credentials.json exists, token_path does not.
        credentials_path = self.mock_config["google_credentials_path"]
        self.mock_os_path_exists.side_effect = lambda path: path == credentials_path
        
        with patch.object(GoogleDocJournal, '_run_auth_flow') as mock_run_auth_method:
            # Simulate _run_auth_flow does not successfully set creds by default for this isolated test
            # (i.e., self.creds remains None after its call unless it's made to set it)
            journal = self._create_journal_instance()
            mock_run_auth_method.assert_called_once()
            # self.creds would be None if _run_auth_flow didn't set it.
            # So, build should not be called if _run_auth_flow (as mocked here) doesn't update self.creds
            self.mock_build.assert_not_called()


    def test_run_auth_flow_handles_missing_credentials_file(self):
        # Ensure google_credentials_path does not exist
        self.mock_os_path_exists.return_value = False 
        
        journal = self._create_journal_instance() # This calls _initialize_docs_service
        # _initialize_docs_service will call _run_auth_flow because no token exists
        
        self.mock_installed_app_flow.assert_not_called() # Flow object should not be created
        self.assertIsNone(journal.creds)
        # Check logs (optional here, but good for real debugging)

    def test_run_auth_flow_simulates_successful_interactive_auth(self):
        # Simulate credentials.json exists
        credentials_path = self.mock_config["google_credentials_path"]
        self.mock_os_path_exists.side_effect = lambda path: path == credentials_path

        mock_successful_creds = MagicMock()
        mock_successful_creds.valid = True
        self.mock_flow_instance.run_local_server.return_value = mock_successful_creds
        
        journal = self._create_journal_instance() # This calls _initialize_docs_service, which calls _run_auth_flow
        
        self.mock_installed_app_flow.assert_called_with(credentials_path, GoogleDocJournal.SCOPES)
        self.mock_flow_instance.run_local_server.assert_called_once()
        self.assertEqual(journal.creds, mock_successful_creds)
        # Also check that token is saved
        self.mock_open_file.assert_called_with(self.mock_config["google_token_path"], "w")
        self.mock_open_file().write.assert_called_with(mock_successful_creds.to_json())
        # And service is built
        self.mock_build.assert_called_with("docs", "v1", credentials=mock_successful_creds, cache_discovery=False)


    @patch('jrnl.journals.GoogleDocJournal.traceback.format_exc') # Mock traceback
    def test_write_to_google_doc_overwrite_logic(self, mock_traceback_format_exc):
        # Setup for a successful write to an existing document
        # Assume service is initialized and journal instance is ready
        self.mock_os_path_exists.side_effect = lambda path: path == self.mock_config["google_token_path"]
        self.mock_creds_instance.valid = True
        self.mock_credentials_from_file.return_value = self.mock_creds_instance
        journal = self._create_journal_instance()
        self.assertIsNotNone(journal.docs_service) # Ensure service was built

        # Mock the .get().execute() call for current doc content
        mock_get_result = {
            'body': {
                'content': [
                    {'endIndex': 1}, 
                    {'startIndex': 1, 'endIndex': 50, 'paragraph': {}}, 
                ]
            },
            'documentId': 'fake_doc_id' # Added for completeness
        }
        self.mock_service_instance.documents().get().execute.return_value = mock_get_result
        
        # Mock the .batchUpdate().execute() call
        self.mock_service_instance.documents().batchUpdate().execute.return_value = {} # Success

        new_content = "This is the new journal content."
        journal._write_to_google_doc(new_content) # Call the method under test

        expected_requests = [
            {'deleteContentRange': {'range': {'startIndex': 1, 'endIndex': 50}}},
            {'insertText': {'location': {'index': 1}, 'text': new_content}}
        ]
        self.mock_service_instance.documents().batchUpdate.assert_called_once_with(
            documentId="fake_doc_id",
            body={'requests': expected_requests}
        )

    @patch('jrnl.journals.GoogleDocJournal.traceback.format_exc')
    def test_write_to_google_doc_handles_httperror_403(self, mock_traceback_format_exc):
        # Assume service is initialized
        self.mock_os_path_exists.side_effect = lambda path: path == self.mock_config["google_token_path"]
        self.mock_creds_instance.valid = True
        self.mock_credentials_from_file.return_value = self.mock_creds_instance
        journal = self._create_journal_instance()
        self.assertIsNotNone(journal.docs_service)

        # Simulate HttpError on batchUpdate
        http_error = MockHttpError(resp_status=403, reason_phrase="Permission Denied", content=b'{"error": "permission_denied"}')
        
        # Doc is initially empty for this error test, simplifying .get()
        self.mock_service_instance.documents().get().execute.return_value = {'body':{'content':[{'endIndex':1}]}, 'documentId': 'fake_doc_id'}
        self.mock_service_instance.documents().batchUpdate().execute.side_effect = http_error
        
        with patch.object(GoogleDocJournal._logger, 'error') as mock_log_error:
            journal._write_to_google_doc("some content")
            
            self.assertTrue(any("HttpError occurred" in call_args[0][0] for call_args in mock_log_error.call_args_list))
            self.assertTrue(any("HTTP 403 Forbidden" in call_args[0][0] for call_args in mock_log_error.call_args_list))

if __name__ == '__main__':
    # To run this test file directly (e.g., python tests/unit/test_google_doc_journal.py)
    # you might need to adjust sys.path if jrnl is not installed in the environment.
    # Example:
    # import sys
    # sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
    unittest.main(verbosity=2)
