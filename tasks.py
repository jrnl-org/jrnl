# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

DOCS_URL = "http://127.0.0.1:8000"
SITEMAP_FILENAME = "sitemap.xml"
CONFIG_FILENAME = "config.json"

def delete_files(files):
    import pathlib

    for file in files:
        pathlib.Path(file).unlink(missing_ok=True)


def generate_sitemap():
    import requests

    sitemap = requests.get(f"{DOCS_URL}/{SITEMAP_FILENAME}")
    with open(SITEMAP_FILENAME, 'wb') as f:
        f.write(sitemap.content)


def generate_pa11y_config_from_sitemap():
    import xmltodict
    import json

    with open(SITEMAP_FILENAME) as f:
        xml_sitemap = xmltodict.parse(f.read())

    urls = [
        f"{DOCS_URL}/",
        f"{DOCS_URL}/search.html?q=jrnl",
    ]
    urls += [url["loc"] for url in xml_sitemap["urlset"]["url"]]

    with open(CONFIG_FILENAME, 'w') as f:
        f.write(json.dumps({"urls": urls}))


def output_file(file):
    import os

    if not os.getenv("CI", False):
        return

    print(f"::group::{file}")

    with open(file) as f:
        print(f.read())

    print('::endgroup::')

