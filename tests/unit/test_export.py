# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from ruamel.yaml import YAML

from jrnl.exception import JrnlException
from jrnl.Journal import PlainJournal
from jrnl.plugins.fancy_exporter import check_provided_linewrap_viability
from jrnl.plugins.yaml_exporter import YAMLExporter


@pytest.fixture()
def datestr():
    yield "2020-10-20 16:59"


@pytest.fixture()
def simple_journal():
    with open("tests/data/configs/simple.yaml") as f:
        yaml = YAML(typ="safe")
        config = yaml.load(f)
    return PlainJournal("simple_journal", **config).open()


def build_card_header(datestr):
    top_left_corner = "┎─╮"
    content = top_left_corner + datestr
    return content


class TestFancy:
    def test_too_small_linewrap(self, datestr):

        journal = "test_journal"
        content = build_card_header(datestr)

        total_linewrap = 12

        with pytest.raises(JrnlException):
            check_provided_linewrap_viability(total_linewrap, [content], journal)


class TestYaml:
    def test_export_to_nonexisting_folder(self, simple_journal):
        with TemporaryDirectory() as tmpdir:
            p = Path(tmpdir / "non_existing_folder")
            with pytest.raises(JrnlException):
                YAMLExporter.write_file(simple_journal, p)
            assert not p.exists()
