<!--
Copyright © 2012-2023 jrnl contributors
License: https://www.gnu.org/licenses/gpl-3.0.html
-->

# Journal Types
`jrnl` can store your journal in a few different ways:

 - a single text file (encrypted or otherwise)
 - a folder structure organized by date containing unencrypted text files
 - the DayOne Classic format

There is no need to specify what type of journal you'd like to use. Instead,
`jrnl` will automatically detect the journal type based on whether you're
referencing a file or a folder in your [config file](advanced.md),
and if it's a folder, whether or not DayOne Classic content exists in it.

## Single File
The single file format is the most flexible, as it can be [encrypted](encryption.md).
To use it, enter any path that is a file or does not already exist. You can
use any extension. `jrnl` will automatically create the file when you save
your first entry.

## Folder
The folder journal format organizes your entries into subfolders for the year
and month and `.txt` files for each day. If there are multiple entries in a day,
they all appear in the same `.txt` file.

The directory tree structure is in this format: `YYYY/MM/DD.txt`. For instance, if
you have an entry on May 5th, 2021 in a folder journal at `~/folderjournal`, it will
be located in: `~/folderjournal/2021/05/05.txt`

!!! note
Creating a new folder journal can be done in two ways:

* Create a folder with the name of the journal before running `jrnl`. Otherwise, when you run `jrnl` for the first time, it will assume that you are creating a single file journal instead, and it will create a file at that path.
* Create a new journal in your [config_file](advanced.md) and end the path with a ``/`` (on a POSIX system like Linux or MacOSX) or a ``\`` (on a Windows system). The folder will be created automatically if it doesn't exist.

!!! note
Folder journals can't be encrypted.

## Day One Classic
`jrnl` supports the original data format used by DayOne. It's similar to the folder
journal format, except it's identified by either of these characteristics:

* the folder has a `.dayone` extension
* the folder has a subfolder named `entries`

This is not to be confused with the DayOne 2.0 format, [which is very different](https://help.dayoneapp.com/en/articles/1187337-day-one-classic-is-retired).

!!! note
DayOne Classic journals can't be encrypted.

## Changing your journal type
You can't simply modify a journal's configuration to change its type. Instead,
define a new journal as the type you'd like, and use
[piping](https://en.wikipedia.org/wiki/Redirection_(computing)#Piping)
to export your old journal as `txt` to an import command on your new journal.

For instance, if you have a `projects` journal you would like to import into
a `new` journal, you would run the following after setting up the configuration
for your `new` journal:
```
jrnl projects --format txt | jrnl new --import
```

## Google Doc Journal (`googledoc`)

The `googledoc` journal type allows you to keep your journal entries synchronized between a local text file and a Google Document. Writes are sent to both locations, while reads are performed from the local text file for speed and offline access.

### Configuration

To use the Google Doc journal type, add a new journal configuration to your `jrnl.yaml` file (or your main configuration file).

Example configuration:

```yaml
journals:
  gdoc_journal: # Your preferred journal name
    type: googledoc
    # Path to the local text file for your journal
    journal: /path/to/your/local_gdoc_journal.txt 
    # The ID of the Google Document you want to sync with
    google_doc_id: "your_google_document_id_here"
    # Path to your Google API credentials file (credentials.json)
    # If not specified, jrnl will look for 'google_credentials.json' 
    # in your jrnl configuration directory (e.g., ~/.jrnl/google_credentials.json)
    google_credentials_path: /path/to/your/google_credentials.json 
    # Optional: Allow writing an empty journal to Google Docs (defaults to false)
    # allow_empty_gdoc_write: false 
    # Other standard journal options (encrypt, default_hour, timeformat, etc.) can also be included
    encrypt: false # Encryption is applied to the local file only.
```

**Key Configuration Options:**

*   `type: googledoc`: **Required.** Specifies the journal type.
*   `journal`: **Required.** The file path to the local copy of your journal.
*   `google_doc_id`: **Required.** The ID of the Google Document. You can find this ID in the URL of your Google Doc: `https://docs.google.com/document/d/YOUR_DOCUMENT_ID_IS_HERE/edit`.
*   `google_credentials_path`: **Required.** The full path to your `credentials.json` file obtained from the Google Cloud Console. Jrnl needs this to authenticate with the Google Docs API on your behalf.
*   `encrypt`: (Optional) If set to `true`, encryption will be applied *only* to the local text file. The content in the Google Doc will remain unencrypted by `jrnl`.

### Setting Up Google API Credentials

To use this feature, you need to:

1.  **Create or use an existing project in the [Google Cloud Console](https://console.cloud.google.com/).**
2.  **Enable the Google Docs API** for your project.
    *   In the Google Cloud Console, navigate to "APIs & Services" > "Library".
    *   Search for "Google Docs API" and enable it.
3.  **Create OAuth 2.0 Credentials for a Desktop Application.**
    *   Navigate to "APIs & Services" > "Credentials".
    *   Click "Create Credentials" > "OAuth client ID".
    *   Select "Desktop app" as the application type.
    *   Give it a name (e.g., "jrnl-googledoc-access").
    *   After creation, a dialog will show your Client ID and Client Secret. Click **"DOWNLOAD JSON"** to save the `credentials.json` file.
    *   Store this `credentials.json` file in a secure location on your computer and provide the path to it in the `google_credentials_path` configuration.
    *   For detailed instructions, refer to Google's guide on [Authorizing credentials for a desktop application](https://developers.google.com/docs/api/quickstart/python#authorize_credentials_for_a_desktop_application) (follow steps related to creating credentials).

### First-Time Authentication

The first time you use `jrnl` with a `googledoc` journal (or when your authorization expires), `jrnl` will attempt to open a web browser. You will be asked to log in to your Google account and authorize `jrnl` to access your Google Docs.

*   Follow the prompts in your browser.
*   Once authorized, `jrnl` will store an access token (typically in a file named `google_token.json` within your `jrnl` configuration directory). This token allows `jrnl` to access your Google Doc without requiring you to log in each time.
*   Keep your `credentials.json` file safe, but the `google_token.json` is what `jrnl` uses for day-to-day operations. If `google_token.json` is deleted or becomes invalid, `jrnl` will re-initiate the browser authentication flow using your `credentials.json`.

### How it Works

*   **Writing Entries:** When you write a new entry or modify your journal, `jrnl` will:
    1.  Save the changes to your local text file (specified by the `journal` path).
    2.  Update the content of the specified Google Document, replacing its entire content with your journal's current full text.
*   **Reading Entries:** When `jrnl` reads entries (e.g., for display, export), it reads from the local text file. This ensures fast access and offline capability.
*   **Synchronization Strategy:** The Google Doc is treated as a mirror of the local file's content. The entire content of the Google Doc is overwritten on each write to ensure consistency. This means any manual changes made directly in the Google Doc (not through `jrnl`) will be lost the next time `jrnl` writes to it.

### Important Notes

*   **Internet Connection:** An internet connection is required for the initial authentication and for writing entries to the Google Doc. If you are offline, writes will still go to your local file, but the Google Doc will not be updated until `jrnl` is run again with an internet connection and a write operation occurs.
*   **API Usage & Rate Limits:** For most users, Google's API rate limits should not be an issue. However, extremely frequent writes to large journals could potentially hit these limits.
*   **Security:** The `credentials.json` file grants significant access. Protect it appropriately. The content in the Google Doc itself is subject to your Google account's security and sharing settings.
