# Copyright © 2023-2024 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import logging
import os
import traceback # Added for detailed error logging
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from jrnl.path import get_config_path # For determining jrnl's config directory
from .Journal import Journal # Ensure Journal base class is imported


class GoogleDocJournal(Journal):
    _logger = logging.getLogger(__name__)
    SCOPES = ["https://www.googleapis.com/auth/documents"] # Class constant for scopes

    def __init__(self, name="default", **kwargs):
        super().__init__(name, **kwargs)
        self._logger.debug(f"Initializing GoogleDocJournal '{name}' with config: {kwargs}")
        self.google_doc_id = self.config.get("google_doc_id")
        self.creds = None
        self.docs_service = None

        try:
            # config_file_path is the path to the jrnl.yaml or equivalent
            config_file_path = get_config_path() 
            jrnl_base_dir = os.path.dirname(config_file_path)
            if not jrnl_base_dir: # Fallback if dirname is empty
                self._logger.warning("Could not determine jrnl base directory from get_config_path(). Falling back to ~/.jrnl.")
                jrnl_base_dir = os.path.join(os.path.expanduser("~"), ".jrnl")
        except Exception as e: 
            self._logger.error(f"Error getting jrnl config path: {e}. Falling back to ~/.jrnl for token/credentials.")
            jrnl_base_dir = os.path.join(os.path.expanduser("~"), ".jrnl")
        
        if not os.path.exists(jrnl_base_dir):
            try:
                os.makedirs(jrnl_base_dir)
                self._logger.info(f"Created jrnl configuration directory at {jrnl_base_dir}")
            except OSError as e:
                self._logger.error(f"Failed to create jrnl configuration directory at {jrnl_base_dir}: {e}. Using current directory as fallback.")
                jrnl_base_dir = "." # Fallback to current directory

        self.token_path = self.config.get("google_token_path", os.path.join(jrnl_base_dir, "google_token.json"))
        self.credentials_path = self.config.get("google_credentials_path", os.path.join(jrnl_base_dir, "google_credentials.json"))
        
        self._logger.info(f"Google Docs Token path: {self.token_path}")
        self._logger.info(f"Google Docs Credentials path (user-provided 'credentials.json'): {self.credentials_path}")

        if self.google_doc_id:
            self._logger.info(f"Google Doc ID '{self.google_doc_id}' is configured. Initializing Google Docs service.")
            self._initialize_docs_service()
        else:
            self._logger.info("No Google Doc ID configured. Google Docs service will not be initialized at startup.")

    def _initialize_docs_service(self):
        self._logger.debug("Attempting to initialize Google Docs service...")
        if os.path.exists(self.token_path):
            try:
                self.creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)
                self._logger.info(f"Loaded existing Google credentials from {self.token_path}")
            except Exception as e:
                self._logger.error(f"Error loading token file '{self.token_path}': {e}. Credentials may be invalid or require re-authentication.")
                self.creds = None

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                try:
                    self._logger.info("Refreshing expired Google access token...")
                    self.creds.refresh(Request())
                    self._logger.info("Google access token refreshed successfully.")
                except Exception as e:
                    self._logger.error(f"Error refreshing Google access token: {e}. Re-authentication will be attempted.")
                    self._run_auth_flow() 
            else:
                self._logger.info("No valid Google credentials found, running authentication flow.")
                self._run_auth_flow()
            
            if self.creds and self.creds.valid: # After potential auth flow or refresh
                try:
                    with open(self.token_path, "w") as token_file:
                        token_file.write(self.creds.to_json())
                    self._logger.info(f"Google credentials saved to {self.token_path}")
                except Exception as e:
                    self._logger.error(f"Error saving Google token file '{self.token_path}': {e}")
        
        if self.creds and self.creds.valid:
            try:
                self.docs_service = build("docs", "v1", credentials=self.creds, cache_discovery=False) # cache_discovery=False for dynamic environments
                self._logger.info("Google Docs service initialized successfully.")
            except Exception as e:
                self._logger.error(f"Error building Google Docs service: {e}")
                self.docs_service = None
        else:
            self._logger.warning("Could not initialize Google Docs service due to invalid or missing credentials after auth attempt.")

    def _run_auth_flow(self):
        self._logger.info("Starting Google OAuth authentication flow...")
        if not os.path.exists(self.credentials_path):
            self._logger.error(f"Google API Credentials file ('{os.path.basename(self.credentials_path)}') not found at expected path: '{self.credentials_path}'.")
            self._logger.error("Please download your OAuth 2.0 client ID and secret from the Google Cloud Console ( τύπος \"Desktop app\" ) and save it as 'google_credentials.json' (or configure 'google_credentials_path' in jrnl config) and place it at the specified path.")
            self._logger.error("Instructions: https://developers.google.com/docs/api/quickstart/python#authorize_credentials_for_a_desktop_application")
            # Consider using print_msg for more direct user feedback if available and appropriate
            # from jrnl.output import print_msg
            # from jrnl.messages import Message, MsgText, MsgStyle
            # print_msg(Message(MsgText.PLAIN_TEXT_MESSAGE_TEMPLATE, MsgStyle.ERROR, {"text": "Google API Credentials file not found..."}))
            self.creds = None 
            return

        try:
            flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, self.SCOPES)
            self._logger.info("Attempting to launch browser for Google OAuth authentication. Please follow the prompts in your browser.")
            # Make sure user is informed that a browser will open.
            # Consider print_msg here for direct feedback.
            print("Attempting to launch browser for Google OAuth authentication. Please follow the prompts in your browser. If the browser does not open, please check your system's default browser settings.")
            
            self.creds = flow.run_local_server(port=0,
                                               authorization_prompt_message="Please authorize jrnl to access your Google Docs in the web browser that has just opened. Waiting for authorization...",
                                               success_message="OAuth2 authorization successful! You can close the browser tab/window.",
                                               open_browser=True) # Explicitly true, though it's default
            
            if self.creds:
                self._logger.info("OAuth flow completed successfully. Credentials obtained.")
            else:
                # This case might not be hit if run_local_server raises an exception on failure,
                # but good for robustness.
                self._logger.error("OAuth flow did not result in valid credentials.")
                self.creds = None

        except FileNotFoundError: # Should be caught by the initial os.path.exists, but good practice.
            self._logger.error(f"Credentials file not found at '{self.credentials_path}' during OAuth flow initiation.")
            self.creds = None
        except Exception as e:
            self._logger.error(f"An error occurred during the Google OAuth flow: {e}")
            self._logger.error("Possible issues: Incorrectly formatted credentials.json, network problems, or browser interaction issues.")
            self.creds = None
        
        # The obtained self.creds will be saved by the calling method _initialize_docs_service
        # if they are valid.

    def open(self, filename: str | None = None) -> "GoogleDocJournal":
        # For now, this will behave like the standard journal's open
        # It will be modified later to handle Google Docs specifics
        return super().open(filename)

    def write(self, filename: str | None = None) -> None:
        super().write(filename) # Write to local file first
        self._logger.debug(f"Local journal file '{filename if filename else self.config['journal']}' written.")

        if self.google_doc_id:
            if not self.docs_service: # If service wasn't initialized at startup (e.g. no doc_id then, but added later)
                self._logger.warning("Google Docs service not initialized. Attempting to initialize for write operation.")
                self._initialize_docs_service() 

            if self.docs_service:
                self._logger.info(f"Preparing to write to Google Doc ID: {self.google_doc_id}")
                # Determine what content to write. For now, the full journal text.
                # This could be optimized later to only send new/modified entries.
                full_journal_text = self._to_text() 
                
                # allow_empty_gdoc_write can be a config option if needed, default to False
                allow_empty = self.config.get("allow_empty_gdoc_write", False) 
                if full_journal_text or allow_empty:
                    self._write_to_google_doc(full_journal_text)
                else:
                    self._logger.info("Journal is empty and 'allow_empty_gdoc_write' is false. Nothing to write to Google Doc.")
            else:
                self._logger.error("Google Docs service could not be initialized. Cannot write to Google Doc.")
        else:
            self._logger.debug("No Google Doc ID configured. Skipping write to Google Docs.")

    def _write_to_google_doc(self, content: str):
        if not self.docs_service: # Should be checked by caller, but good for safety
            self._logger.error("Google Docs service not available. Cannot write to Google Doc.")
            return
        
        # Ensure content is not None, though _to_text() should return "" for empty.
        content_to_write = content if content is not None else ""

        if not self.docs_service:
            self._logger.error("Google Docs service not available. Cannot write to Google Doc.")
            return
        if not self.google_doc_id:
            self._logger.error("Google Doc ID not configured. Cannot write to Google Doc.")
            return
        
        content_to_write = content if content is not None else ""

        self._logger.info(f"Preparing to write to Google Doc ID '{self.google_doc_id}'. Strategy: Overwrite/Replace.")

        requests = []
        try:
            # 1. Get the current document's structure to find the end of content for deletion.
            # Fetching the full document is more reliable for complex documents.
            document = self.docs_service.documents().get(documentId=self.google_doc_id).execute()
            
            current_doc_end_index = 1 # Default for an empty document (has one implicit paragraph).
            body_content_list = document.get('body', {}).get('content', [])
            if body_content_list:
                # The document's content is a list of StructuralElements.
                # The last element's endIndex is the effective length of the document's content.
                # Ensure we only access endIndex if the element is not None and has the key.
                last_element = body_content_list[-1]
                if last_element and 'endIndex' in last_element:
                    current_doc_end_index = last_element['endIndex']

            self._logger.debug(f"Current document's perceived end index: {current_doc_end_index}")

            # 2. Create a request to delete all existing content.
            # The Google Docs API uses 1-based indexing. The range for deletion is [startIndex, endIndex).
            # To delete all content, we delete from index 1 up to the document's current total length (current_doc_end_index).
            if current_doc_end_index > 1:  # If there's content beyond the initial empty paragraph.
                requests.append({
                    'deleteContentRange': {
                        'range': {
                            'startIndex': 1, # Deletion starts after the very first position.
                            'endIndex': current_doc_end_index, # Deletes up to (but not including) this index.
                        }
                    }
                })
                self._logger.debug(f"Added request to delete content from range [1, {current_doc_end_index}).")

            # 3. Create a request to insert the new content at the beginning (index 1).
            if content_to_write:
                requests.append({
                    'insertText': {
                        'location': {
                            'index': 1  # Insert at the beginning of the document body.
                        },
                        'text': content_to_write
                    }
                })
                self._logger.debug(f"Added request to insert new content (length {len(content_to_write)}) at index 1.")
            elif not requests: 
                # This means current_doc_end_index <= 1 (doc was empty) AND content_to_write is empty.
                self._logger.info("Document is already empty and new content is empty. No API call needed.")
                return 

            # 4. Execute the batchUpdate if there are any requests
            if requests:
                self._logger.info(f"Executing batchUpdate with {len(requests)} requests for Google Doc '{self.google_doc_id}'.")
                self.docs_service.documents().batchUpdate(
                    documentId=self.google_doc_id, body={'requests': requests}
                ).execute()
                self._logger.info(f"Successfully updated content in Google Doc '{self.google_doc_id}'.")
            # No 'else' needed here as the "already empty and new content is empty" case is handled above.
            
        except HttpError as error:
            self._logger.error(f"An HttpError occurred while writing to Google Doc '{self.google_doc_id}': {error.resp.status} - {error._get_reason()}")
            error_details = "No additional details."
            if error.content:
                try:
                    error_details = error.content.decode('utf-8') # Try to decode as utf-8
                except Exception: 
                    error_details = str(error.content) # Fallback to string representation
            self._logger.error(f"Details: {error_details}")
                if error.resp.status == 400:
                    self._logger.error("HTTP 400 Bad Request: The request sent by jrnl was malformed. This could be due to an unexpected document structure or a bug in jrnl. Please report this issue if it persists.")
                elif error.resp.status == 401:
                    self._logger.error("HTTP 401 Unauthorized: Your authentication credentials may be invalid or expired. jrnl will attempt to re-authenticate on the next run. If this persists, your Google token might be corrupted or scopes insufficient.")
                    # Forcing re-authentication by clearing current credentials
                    self.creds = None
                    self.docs_service = None 
                    try:
                        if os.path.exists(self.token_path):
                            os.remove(self.token_path)
                            self._logger.info(f"Removed potentially corrupted token file at {self.token_path} to force re-authentication.")
                    except Exception as ex_remove:
                        self._logger.error(f"Error removing token file {self.token_path}: {ex_remove}")
                elif error.resp.status == 403:
                    self._logger.error("HTTP 403 Forbidden: Permission denied. Ensure 'jrnl' has write access to the Google Doc and that the Google Docs API is enabled in your Google Cloud project. Check the sharing settings for the document.")
            elif error.resp.status == 404:
                    self._logger.error(f"HTTP 404 Not Found: The Google Doc with ID '{self.google_doc_id}' was not found. Please verify the 'google_doc_id' in your journal's configuration.")
                elif error.resp.status == 429:
                    self._logger.error("HTTP 429 Resource Exhausted (Rate Limit): You've made too many requests to Google Docs API in a short period. Please wait a while and try again.")
                elif error.resp.status >= 500 and error.resp.status < 600:
                    self._logger.error(f"HTTP {error.resp.status} Server Error: A server-side error occurred with Google's services. This is likely a temporary issue. Please try again later.")
                # else:
                #    self._logger.error(f"Unhandled HTTP Error {error.resp.status}: {error._get_reason()}. Details: {error_details}")
        except Exception as e:
            self._logger.error(f"A general error occurred while writing to Google Doc '{self.google_doc_id}': {e}")
            # It's good to have traceback for unexpected errors during development/debugging.
            # Import traceback at the top of the file: import traceback
            self._logger.debug(f"Traceback: {traceback.format_exc()}")
