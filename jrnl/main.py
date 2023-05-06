# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html
from ruamel import yaml

def run():
    my_dict = dict(a='a' * 80, b=dict(c=1, d=2))
    return yaml.dump(my_dict)
