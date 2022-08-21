# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import json
import os
import pathlib
import subprocess

import requests
import xmltodict

DOCS_URL = "http://127.0.0.1:8000"
SITEMAP_FILENAME = "sitemap.xml"
CONFIG_FILENAME = "config.json"


def delete_files(files):
    for file in files:
        pathlib.Path(file).unlink(missing_ok=True)


def run_shell(command):
    # Required to run NPM commands in Windows and *nix
    subprocess.call(command, shell=True)


def generate_sitemap():
    sitemap = requests.get(f"{DOCS_URL}/{SITEMAP_FILENAME}")
    with open(SITEMAP_FILENAME, "wb") as f:
        f.write(sitemap.content)


def generate_pa11y_config_from_sitemap():
    with open(SITEMAP_FILENAME) as f:
        xml_sitemap = xmltodict.parse(f.read())

    urls = [
        f"{DOCS_URL}/",
        f"{DOCS_URL}/search.html?q=jrnl",
    ]
    urls += [url["loc"] for url in xml_sitemap["urlset"]["url"]]

    with open(CONFIG_FILENAME, "w") as f:
        f.write(json.dumps({"urls": urls}))


def output_file(file):
    if not os.getenv("CI", False):
        return

    print(f"::group::{file}")

    with open(file) as f:
        print(f.read())

    print("::endgroup::")
