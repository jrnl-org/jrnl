# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

# localization format example
# OneLineMessage = T(
#     en="something",
#     ja="何か",
# )
# MultiLineMessage = T(
#     en="""
#     something
#     """,
#     ja="""
#     何か
#     """,
# )

from enum import Enum


class MsgText(Enum):
    def __str__(self) -> str:
        return self.value

    # -- Welcome --- #
    WelcomeToJrnl = T(
        en="""
        Welcome to jrnl {version}!

        It looks like you've been using an older version of jrnl until now. That's
        okay - jrnl will now upgrade your configuration and journal files. Afterwards
        you can enjoy all of the great new features that come with jrnl 2:

        - Support for storing your journal in multiple files
        - Faster reading and writing for large journals
        - New encryption back-end that makes installing jrnl much easier
        - Tons of bug fixes

        Please note that jrnl 1.x is NOT forward compatible with this version of jrnl.
        If you choose to proceed, you will not be able to use your journals with
        older versions of jrnl anymore.
        """,
        ja="""
        jrnl {version} へようこそ!

        これまでは古いバージョンの jrnl を使用していたようです。問題ありません。jrnl はこれから
        設定ファイルとジャーナル ファイルをアップグレードします。その後は、jrnl 2 に付属する
        すばらしい新機能をすべてお楽しめます:

        - ジャーナルを複数のファイルに保存するためのサポート
        - 大きなジャーナルの読み取りと書き込みの高速化
        - jrnl のインストールを大幅に容易にする新しい暗号化バックエンド
        - 多数のバグ修正

        jrnl 1.x は、このバージョンの jrnl と前方互換性がありませんのでご注意ください。
        続行する場合は、古いバージョンの jrnl ではジャーナルを使用できなくなります。
        """,
        )
    AllDoneUpgrade = T(
        en="We're all done here and you can start enjoying jrnl 2",
        ja="これですべて完了です、jrnl 2 をお楽しみください",
        )
    InstallComplete = T(
        en="""
        jrnl configuration created at {config_path}
        For advanced features, read the docs at https://jrnl.sh
        """,
        ja="""
        jrnl 構成がここに作成されました： {config_path} 
        高度な機能については、https://jrnl.sh のドキュメントをお読みください。
        """,
        )

    # --- Prompts --- #
    InstallJournalPathQuestion = T(
        en="""
        Path to your journal file (leave blank for {default_journal_path}):
        """,
        ja="""
        ジャーナル ファイルへのパス ({default_journal_path} で良ければ空白のままにしてください):
        """,
        )
    DeleteEntryQuestion = T(
        en="Delete entry '{entry_title}'?",
        ja="エントリ '{entry_title}' を削除しますか?",
        )
    ChangeTimeEntryQuestion = T(
        en="Change time for '{entry_title}'?",
        ja="'{entry_title}' の時間を変更しますか？",
        )
    EncryptJournalQuestion = T(
        en="""
        Do you want to encrypt your journal? (You can always change this later)
        """,
        ja="""
        ジャーナルを暗号化しますか？（これは後でいつでも変更できます）
        """,
        )
    UseColorsQuestion = T(
        en="""
        Do you want jrnl to use colors to display entries? (You can always change this later)
        """,  # noqa: E501 - the line is still under 88 when dedented
        ja="""
        jrnl でエントリの表示に色を使用しますか？（これは後でいつでも変更できます）
        """,
        )
    YesOrNoPromptDefaultYes = "[Y/n]"
    YesOrNoPromptDefaultNo = "[y/N]"
    ContinueUpgrade = T(
        en="Continue upgrading jrnl?",
        ja="jrnl のアップグレードを続行しますか？",
        )

    # these should be lowercase, if possible in language
    # "lowercase" means whatever `.lower()` returns
    OneCharacterYes = "y"
    OneCharacterNo = "n"

    # --- Exceptions ---#
    Error = T(
        en="Error",
        ja="エラー",
        )
    UncaughtException = T(
        en="""
        {name}
        {exception}

        This is probably a bug. Please file an issue at:
        https://github.com/jrnl-org/jrnl/issues/new/choose
        """,
        ja="""
        {name}
        {exception}

        これはおそらくバグです。問題を報告してください:
        https://github.com/jrnl-org/jrnl/issues/new/choose
        """,
        )
    ConfigDirectoryIsFile = T(
        en="""
        Problem with config file!
        The path to your jrnl configuration directory is a file, not a directory:

        {config_directory_path}

        Removing this file will allow jrnl to save its configuration.
        """,
        ja="""
        構成ファイルに問題があります!
        jrnl 構成ディレクトリへのパスはディレクトリではなくファイルです:

        {config_directory_path}

        このファイルを削除すると、jrnl が構成を保存できるようになります。
        
        """,
        )
    CantParseConfigFile = T(
        en="""
        Unable to parse config file at:
        {config_path}
        """,
        ja="""
        ここにある構成ファイルを解析できません:
        {config_path}
        """,
        )
    LineWrapTooSmallForDateFormat = T(
        en="""
        The provided linewrap value of {config_linewrap} is too small by
        {columns} columns to display the timestamps in the configured time
        format for journal {journal}.

        You can avoid this error by specifying a linewrap value that is larger
        by at least {columns} in the configuration file or by using
        --config-override at the command line
        """,
        ja="""
        指定された {config_linewrap} の行折り返し値は、ジャーナル {journal} に
        設定された時間形式でタイムスタンプを表示するには、{columns} 列分小さすぎます。

        このエラーを回避するには、構成ファイルで行折り返し値を少なくとも {columns} 大きく
        指定するか、コマンド ラインで --config-override を使用してください。
        """,
        )
    CannotEncryptJournalType = T(
        en="""
        The journal {journal_name} can't be encrypted because it is a
        {journal_type} journal.

        To encrypt it, create a new journal referencing a file, export
        this journal to the new journal, then encrypt the new journal.
        """,
        ja="""
        ジャーナル {journal_name} は {journal_type} ジャーナルであるため暗号化できません。

        暗号化するには、ファイルを参照する新しいジャーナルを作成し、このジャーナルを新しい
        ジャーナルにエクスポートしてから、新しいジャーナルを暗号化してください。
        """,
        )
    ConfigEncryptedForUnencryptableJournalType = T(
        en="""
        The config for journal "{journal_name}" has 'encrypt' set to true, but this type
        of journal can't be encrypted. Please fix your config file.
        """,
        ja="""
        ジャーナル "{journal_name}" の構成では 'encrypt' が true に設定されていますが、
        このタイプのジャーナルは暗号化できません。構成ファイルを修正してください。
        """,
        )
    DecryptionFailedGeneric = T(
        en="The decryption of journal data failed.",
        ja="ジャーナル データの復号化に失敗しました。",
        )
    KeyboardInterruptMsg = T(
        en="Aborted by user",
        ja="ユーザーによって中止しました",
        )
    CantReadTemplate = T(
        en="""
        Unable to find a template file {template_path}.

        The following paths were checked:
         * {jrnl_template_dir}{template_path}
         * {actual_template_path}
        """,
        ja="""
        テンプレート ファイル {template_path} が見つかりません。

        次のパスがチェックされました:
        * {jrnl_template_dir}{template_path}
        * {actual_template_path}
        """,
        )
    NoNamedJournal = T(
        en="No '{journal_name}' journal configured\n{journals}",
        ja="'{journal_name}' ジャーナルが設定されていません\n{journals}",
        )
    # is that \n{journals} supposed to be there?
    DoesNotExist = T(
        en="{name} does not exist",
        ja="{name} が存在しません",
        )

    # --- Journal status ---#
    JournalNotSaved = T(
        en="Entry NOT saved to journal",
        ja="エントリがジャーナルに保存されませんでした",
        )
    JournalEntryAdded = T(
        en="Entry added to {journal_name} journal",
        ja="エントリが {journal_name} ジャーナルに追加されました",
        )
    JournalCountAddedSingular = T(
        en="{num} entry added",
        ja="{num} 個のエントリが追加されました",
        )
    JournalCountModifiedSingular = T(
        en="{num} entry modified",
        ja="{num} 個のエントリが変更されました",
        )
    JournalCountDeletedSingular = T(
        en="{num} entry deleted",
        ja="{num} 個のエントリが削除されました",
        )
    JournalCountAddedPlural = T(
        en="{num} entries added",
        ja="{num} 個のエントリが追加されました",
        )
    JournalCountModifiedPlural = T(
        en="{num} entries modified",
        ja="{num} 個のエントリが変更されました",
        )
    JournalCountDeletedPlural = T(
        en="{num} entries deleted",
        ja="{num} 個のエントリが削除されました",
        )
    JournalCreated = T(
        en="Journal '{journal_name}' created at {filename}",
        ja="ジャーナル '{journal_name}' が {filename} に作成されました",
        )
    DirectoryCreated = T(
        en="Directory {directory_name} created",
        ja="ディレクトリ {directory_name} が作成されました",
        )
    JournalEncrypted = T(
        en="Journal will be encrypted",
        ja="ジャーナルは暗号化されます",
        )
    JournalEncryptedTo = T(
        en="Journal encrypted to {path}",
        ja="ジャーナルが {path} に暗号化されました",
        )
    JournalDecryptedTo = T(
        en="Journal decrypted to {path}",
        ja="ジャーナルが {path} に復号されました",
        )
    BackupCreated = T(
        en="Created a backup at {filename}",
        ja="{filename} にバックアップが作成されました",
        )

    # --- Editor ---#
    WritingEntryStart = T(
        en="""
        Writing Entry
        To finish writing, press {how_to_quit} on a blank line.
        """,
        ja="""
        エントリ書き込み中
        書き込みを終了するには、空白行で {how_to_quit} を押してください。
        """,
        )

    HowToQuitWindows = T(
        en="Ctrl+z and then Enter",
        ja="Ctrl+z を押してから Enter を押してください",
        )
    HowToQuitLinux = T(
        en="Ctrl+d",
        ja="Ctrl+d",
        )
    EditorMisconfigured = T(
        en="""
        No such file or directory: '{editor_key}'

        Please check the 'editor' key in your config file for errors:
            editor: '{editor_key}'
        """,
        ja="""
        このファイルまたはディレクトリはありません: '{editor_key}'

        構成ファイルの 'editor' キーにエラーがないか確認してください:
            エディター: '{editor_key}'
        """,
        )
    EditorNotConfigured = T(
        en="""
        There is no editor configured

        To use the --edit option, please specify an editor in your config file:
            {config_file}

        For examples of how to configure an external editor, see:
            https://jrnl.sh/en/stable/external-editors/
        """,
        ja="""
        エディターが設定されていません

        --edit オプションを使用するには、構成ファイルでエディターを指定してください:
            {config_file}

        外部エディタを設定する例については、次を見てください:
            https://jrnl.sh/en/stable/external-editors/
        """,
        )
    NoEditsReceivedJournalNotDeleted = T(
        en="""
        No text received from editor. Were you trying to delete all the entries?

        This seems a bit drastic, so the operation was cancelled.

        To delete all entries, use the --delete option.
        """,
        ja="""
        エディタからテキストを受信しませんでした。すべてのエントリを削除しようとしましたか?

        これは少し極端なため、操作はキャンセルされました。

        すべてのエントリを削除するには、--delete オプションを使用してください。
        """,
        )
    NoEditsReceived = T(
        en="No edits to save, because nothing was changed",
        ja="変更がなかったため、保存する編集はありません",
        )
    NoTextReceived = T(
        en="""
        No entry to save, because no text was received
        """,
        ja="""
        テキストが受信されてないため、保存するエントリがありません
        """,
        )
    NoChangesToTemplate = T(
        en="""
        No entry to save, because the template was not changed
        """,
        ja="""
        テンプレートが変更されていないため、保存するエントリがありません
        """,
        )

    # --- Upgrade --- #
    JournalFailedUpgrade = T(
        en="""
        The following journal{s} failed to upgrade:
        {failed_journals}

        Please tell us about this problem at the following URL:
        https://github.com/jrnl-org/jrnl/issues/new?title=JournalFailedUpgrade
        """,
        ja="""
        次のジャーナルはアップグレードに失敗しました:
        {failed_journals}

        この問題について、次の　URL　でお知らせください:
        https://github.com/jrnl-org/jrnl/issues/new?title=JournalFailedUpgrade
        """,
        )
    UpgradeAborted = T(
        en="jrnl was NOT upgraded",
        ja="jrnl はアップグレードされませんでした",
        )
    AbortingUpgrade = T(
        en="Aborting upgrade...",
        ja="アップグレードを中止しています...",
        )
    ImportAborted = T(
        en="Entries were NOT imported",
        ja="エントリがインポートされませんでした",
        )
    JournalsToUpgrade = T(
        en="""
        The following journals will be upgraded to jrnl {version}:

        """,
        ja="""
        次のジャーナルは jrnl {バージョン} にアップグレードされます:

        """,
        )
    JournalsToIgnore = T(
        en="""
        The following journals will not be touched:

        """,
        ja="""
        次のジャーナルは変更されません:

        """,
        )
    UpgradingJournal = T(
        en="""
        Upgrading '{journal_name}' journal stored in {path}...
        """,
        ja="""
        {path} に保存されている '{journal_name}' ジャーナルをアップグレードしています...
        """,
        )
    UpgradingConfig = T(
        en="Upgrading config...",
        ja="構成をアップグレードしています...",
        )
    PaddedJournalName = "{journal_name:{pad}} -> {path}"

    # -- Config --- #
    AltConfigNotFound = T(
        en="""
        Alternate configuration file not found at the given path:
            {config_file}
        """,
        ja="""
        指定されたパスに代替構成ファイルが見つかりません:
            {config_file}
        """,
        )
    ConfigUpdated = T(
        en="""
        Configuration updated to newest version at {config_path}
        """,
        ja="""
        {config_path} で構成が最新バージョンに更新されました
        """,
        )
    ConfigDoubleKeys = T(
        en="""
        There is at least one duplicate key in your configuration file.

        Details:
        {error_message}
        """,
        ja="""
        構成ファイル内に重複するキーが少なくとも 1 つあります。

        詳細:
        {error_message}
        """,
        )

    # --- Password --- #
    Password = T(
        en="Password:",
        ja="パスワード:",
        )
    PasswordFirstEntry = T(
        en="Enter password for journal '{journal_name}': ",
        ja="ジャーナル '{journal_name}' のパスワードを入力してください: ",
        )
    PasswordConfirmEntry = T(
        en="Enter password again: ",
        ja="パスワードをもう一度入力してくださいください: ",
        )
    PasswordMaxTriesExceeded = T(
        en="Too many attempts with wrong password",
        ja="間違ったパスワードで試行回数が多すぎます",
        )
    PasswordCanNotBeEmpty = T(
        en="Password can't be empty!",
        ja="パスワードを空にすることはできません！",
        )
    PasswordDidNotMatch = T(
        en="Passwords did not match, please try again",
        ja="パスワードが一致しませんでした、もう一度お試しください",
        )
    WrongPasswordTryAgain = T(
        en="Wrong password, try again",
        ja="パスワードが間違っています、やり直してください",
        )
    PasswordStoreInKeychain = T(
        en="Do you want to store the password in your keychain?",
        ja="パスワードをキーチェーンに保存しますか？",
        )

    # --- Search --- #
    NothingToDelete = T(
        en="""
        No entries to delete, because the search returned no results
        """,
        ja="""
        検索で結果が返されなかったため、削除するエントリはありません
        """,
        )
    NothingToModify = T(
        en="""
        No entries to modify, because the search returned no results
        """,
        ja="""
        検索で結果が返されなかったため、変更するエントリはありません
        """,
        )
    NoEntriesFound = T(
        en="no entries found",
        ja="エントリが見つかりません",
        )
    EntryFoundCountSingular = T(
        en="{num} entry found",
        ja="{num} 個のエントリが見つかりました",
        )
    EntryFoundCountPlural = T(
        en="{num} entries found",
        ja="{num} 個のエントリが見つかりました",
        )

    # --- Formats --- #
    HeadingsPastH6 = T(
        en="""
        Headings increased past H6 on export - {date} {title}
        """,
        ja="""
        エクスポート時に見出しが増えて H6 を超えました - {date} {title}
        """,
        )
    YamlMustBeDirectory = T(
        en="""
        YAML export must be to a directory, not a single file
        """,
        ja="""
        YAML エクスポートは、単一のファイルではなく、ディレクトリに行う必要があります
        """,
        )
    JournalExportedTo = T(
        en="Journal exported to {path}",
        ja="ジャーナルが {path} にエプスポートされました",
        )

    # --- Import --- #
    ImportSummary = T(
        en="""
        {count} imported to {journal_name} journal
        """,
        ja="""
        {count} 個が {journal_name} ジャーナルにインポートされました
        """,
        )
    
    # --- Color --- #
    InvalidColor = T(
        en="{key} set to invalid color: {color}",
        ja="{key} が無効な色に設定されています: {color}",
        )

    # --- Keyring --- #
    KeyringBackendNotFound = T(
        en="""
        Keyring backend not found.

        Please install one of the supported backends by visiting:
          https://pypi.org/project/keyring/
        """,
        ja="""
        キーリングのバックエンドが見つかりません。

        サポートされているバックエンドのいずれかをここからインストールしてください:
          https://pypi.org/project/keyring/
        """,
        )
    KeyringRetrievalFailure = T(
        en="Failed to retrieve keyring",
        ja="キーリングの取得に失敗しました",
        )

    # --- Deprecation --- #
    DeprecatedCommand = T(
        en="""
        The command {old_cmd} is deprecated and will be removed from jrnl soon.
        Please use {new_cmd} instead.
        """,
        ja="""
        コマンド {old_cmd} は非推奨であり、まもなく jrnl から削除されます。
        代わりに {new_cmd} を使用してください。
        """,
        )