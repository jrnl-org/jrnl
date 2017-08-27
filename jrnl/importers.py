#!/usr/bin/env python
import os
import json
import sys
from . import util

def import_json(path, jrnl_config):
    json_data = util.load_and_fix_json(path, "JSON")

    new_jrnl = open(jrnl_config["journal"], "w")
    for element in json_data["entries"]:
        new_jrnl.write(
            element["date"] + 
            " " +
            element["time"] + 
            " " +
            element["title"] + 
            "\n" +
            element["body"]
        )
    new_jrnl.close()
