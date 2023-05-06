# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html
from ruamel.yaml import YAML
import sys
from io import StringIO


def run(num=None):
    if num is None:
        num = sys.argv[1]

    my_str = "a" * int(num)
    my_dict = dict(a=my_str, b=dict(c=1, d=2))

    output = StringIO()
    YAML().dump(my_dict, output)
    return output.getvalue()
