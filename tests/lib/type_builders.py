# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from parse_type import TypeBuilder

should_choice = TypeBuilder.make_enum(
    {
        "should": True,
        "should not": False,
    }
)
