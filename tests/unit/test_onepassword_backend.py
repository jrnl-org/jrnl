# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import json
import subprocess
from unittest.mock import patch

import pytest
from keyring.errors import PasswordDeleteError

from jrnl.encryption.OnePasswordBackend import OnePasswordBackend

SERVICE = "jrnl"
USERNAME = "default"
TITLE = "jrnl/default"


def completed(returncode=0, stdout="", stderr=""):
    return subprocess.CompletedProcess(
        args=[], returncode=returncode, stdout=stdout, stderr=stderr
    )


def patch_run(side_effect):
    return patch(
        "jrnl.encryption.OnePasswordBackend.subprocess.run", side_effect=side_effect
    )


class TestIsAvailable:
    def test_true_when_op_on_path(self):
        with patch("shutil.which", return_value="/usr/bin/op"):
            assert OnePasswordBackend.is_available() is True

    def test_false_when_op_missing(self):
        with patch("shutil.which", return_value=None):
            assert OnePasswordBackend.is_available() is False


class TestItemExists:
    def test_raises_when_not_authenticated(self):
        with patch_run([completed(returncode=1, stderr="not signed in")]):
            with pytest.raises(RuntimeError, match="not signed in"):
                OnePasswordBackend().item_exists(SERVICE, USERNAME)

    def test_true_when_item_exists(self):
        with patch_run([completed(returncode=0), completed(returncode=0)]) as run:
            assert OnePasswordBackend().item_exists(SERVICE, USERNAME) is True
            item_get_args = run.call_args_list[1].args[0]
            assert TITLE in item_get_args

    def test_false_when_item_missing(self):
        with patch_run([completed(returncode=0), completed(returncode=1)]):
            assert OnePasswordBackend().item_exists(SERVICE, USERNAME) is False


class TestGetPassword:
    def test_raises_when_not_authenticated(self):
        with patch_run([completed(returncode=1, stderr="not signed in")]):
            with pytest.raises(RuntimeError, match="not signed in"):
                OnePasswordBackend().get_password(SERVICE, USERNAME)

    def test_returns_none_when_item_not_found(self):
        with patch_run(
            [
                completed(returncode=0),  # whoami
                completed(returncode=1, stderr="isn't an item"),  # item get
            ]
        ):
            assert OnePasswordBackend().get_password(SERVICE, USERNAME) is None

    def test_returns_password_when_response_is_a_bare_field_object(self):
        # 'op item get --fields label=password --format json' returns a
        # single field object (not a list) when only one field is requested.
        # This is the shape jrnl's single-field request actually receives.
        field = json.dumps(
            {
                "id": "password",
                "type": "CONCEALED",
                "purpose": "PASSWORD",
                "label": "password",
                "value": "hunter2",
                "reference": "op://Private/jrnl-default/password",
            }
        )
        with patch_run(
            [
                completed(returncode=0),  # whoami
                completed(returncode=0, stdout=field),  # item get
            ]
        ):
            assert OnePasswordBackend().get_password(SERVICE, USERNAME) == "hunter2"

    def test_returns_password_when_response_is_a_list_of_fields(self):
        # When multiple --fields values are requested, 'op' returns a list
        # of field objects instead. jrnl only ever requests one field, but
        # the parser should tolerate this shape too.
        fields = json.dumps([{"label": "password", "value": "hunter2"}])
        with patch_run(
            [
                completed(returncode=0),  # whoami
                completed(returncode=0, stdout=fields),  # item get
            ]
        ):
            assert OnePasswordBackend().get_password(SERVICE, USERNAME) == "hunter2"

    def test_raises_on_malformed_response(self):
        with patch_run(
            [
                completed(returncode=0),  # whoami
                completed(returncode=0, stdout="not json"),  # item get
            ]
        ):
            with pytest.raises(RuntimeError, match="Unexpected response"):
                OnePasswordBackend().get_password(SERVICE, USERNAME)

    def test_raises_when_password_field_missing_from_bare_object(self):
        field = json.dumps({"label": "username", "value": "someone"})
        with patch_run(
            [
                completed(returncode=0),  # whoami
                completed(returncode=0, stdout=field),  # item get
            ]
        ):
            with pytest.raises(RuntimeError, match="Unexpected response"):
                OnePasswordBackend().get_password(SERVICE, USERNAME)

    def test_raises_when_password_field_missing_from_list(self):
        fields = json.dumps([{"label": "username", "value": "someone"}])
        with patch_run(
            [
                completed(returncode=0),  # whoami
                completed(returncode=0, stdout=fields),  # item get
            ]
        ):
            with pytest.raises(RuntimeError, match="Unexpected response"):
                OnePasswordBackend().get_password(SERVICE, USERNAME)

    def test_uses_service_slash_username_as_item_title(self):
        fields = json.dumps({"label": "password", "value": "hunter2"})
        with patch_run(
            [completed(returncode=0), completed(returncode=0, stdout=fields)]
        ) as run:
            OnePasswordBackend().get_password(SERVICE, USERNAME)
            item_get_args = run.call_args_list[1].args[0]
            assert TITLE in item_get_args


class TestSetPassword:
    def test_raises_when_not_authenticated(self):
        with patch_run([completed(returncode=1, stderr="not signed in")]):
            with pytest.raises(RuntimeError, match="not signed in"):
                OnePasswordBackend().set_password(SERVICE, USERNAME, "hunter2")

    def test_creates_item_when_it_does_not_exist(self):
        with patch_run(
            [
                completed(returncode=0),  # whoami
                completed(returncode=1),  # item get (existence check) -> not found
                completed(returncode=0),  # item create
            ]
        ) as run:
            OnePasswordBackend().set_password(SERVICE, USERNAME, "hunter2")
            create_args = run.call_args_list[2].args[0]
            assert "create" in create_args
            assert "password=hunter2" in create_args
            assert not any(arg.startswith("username=") for arg in create_args)

    def test_edits_item_when_it_already_exists(self):
        with patch_run(
            [
                completed(returncode=0),  # whoami
                completed(returncode=0),  # item get (existence check) -> found
                completed(returncode=0),  # item edit
            ]
        ) as run:
            OnePasswordBackend().set_password(SERVICE, USERNAME, "hunter2")
            edit_args = run.call_args_list[2].args[0]
            assert "edit" in edit_args
            assert "password=hunter2" in edit_args
            assert not any(arg.startswith("username=") for arg in edit_args)

    def test_raises_when_create_fails(self):
        with patch_run(
            [
                completed(returncode=0),  # whoami
                completed(returncode=1),  # item get -> not found
                completed(returncode=1, stderr="boom"),  # item create fails
            ]
        ):
            with pytest.raises(RuntimeError, match="boom"):
                OnePasswordBackend().set_password(SERVICE, USERNAME, "hunter2")


class TestDeletePassword:
    def test_raises_when_not_authenticated(self):
        with patch_run([completed(returncode=1, stderr="not signed in")]):
            with pytest.raises(RuntimeError, match="not signed in"):
                OnePasswordBackend().delete_password(SERVICE, USERNAME)

    def test_raises_password_delete_error_when_item_missing(self):
        with patch_run(
            [
                completed(returncode=0),  # whoami
                completed(returncode=1),  # item get -> not found
            ]
        ):
            with pytest.raises(PasswordDeleteError):
                OnePasswordBackend().delete_password(SERVICE, USERNAME)

    def test_deletes_existing_item(self):
        with patch_run(
            [
                completed(returncode=0),  # whoami
                completed(returncode=0),  # item get -> found
                completed(returncode=0),  # item delete
            ]
        ) as run:
            OnePasswordBackend().delete_password(SERVICE, USERNAME)
            delete_args = run.call_args_list[2].args[0]
            assert "delete" in delete_args

    def test_raises_when_delete_command_fails(self):
        with patch_run(
            [
                completed(returncode=0),  # whoami
                completed(returncode=0),  # item get -> found
                completed(returncode=1, stderr="boom"),  # item delete fails
            ]
        ):
            with pytest.raises(RuntimeError, match="boom"):
                OnePasswordBackend().delete_password(SERVICE, USERNAME)
