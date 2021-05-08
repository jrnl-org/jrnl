import os
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

base_dir = os.path.dirname(os.path.abspath(__file__))


def get_version(filename="jrnl/contrib/exporter/rot13.py"):
    with open(os.path.join(base_dir, filename), encoding="utf-8") as initfile:
        for line in initfile.readlines():
            m = re.match("__version__ *= *['\"](.*)['\"]", line)
            if m:
                return m.group(1)


setup(
    name="jrnl-demo-plugins",
    version=get_version(),
    description="Demonstration custom plugins for jrnl",
    long_description="\n\n".join([open(os.path.join(base_dir, "README.md")).read()]),
    long_description_content_type="text/markdown",
    author="W. Minchin",
    author_email="w_minchin@hotmail.com",
    url="https://github.com/jrnl-org/jrnl/tree/develop/tests/external_plugins_src",
    packages=["jrnl", "jrnl.contrib", "jrnl.contrib.exporter", "jrnl.contrib.importer"],
    include_package_data=True,
    install_requires=[
        "jrnl",
    ],
    zip_safe=False,  # use wheels instead
)
