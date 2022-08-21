# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from enum import Enum
from typing import Callable
from typing import NamedTuple

from rich import box
from rich.panel import Panel

from jrnl.messages.MsgText import MsgText


class MsgStyle(Enum):
    class _Color(NamedTuple):
        """
        String representing a standard color to display
        see: https://rich.readthedocs.io/en/stable/appendix/colors.html
        """

        color: str

    class _Decoration(Enum):
        NONE = {
            "callback": lambda x, **_: x,
            "args": {},
        }
        BOX = {
            "callback": Panel,
            "args": {
                "expand": False,
                "padding": (0, 2),
                "title_align": "left",
                "box": box.HEAVY,
            },
        }

        @property
        def callback(self) -> Callable:
            return self.value["callback"]

        @property
        def args(self) -> dict:
            return self.value["args"]

    PROMPT = {
        "decoration": _Decoration.NONE,
        "color": _Color("white"),
        "append_space": True,
    }
    TITLE = {
        "decoration": _Decoration.BOX,
        "color": _Color("cyan"),
    }
    NORMAL = {
        "decoration": _Decoration.BOX,
        "color": _Color("white"),
    }
    WARNING = {
        "decoration": _Decoration.BOX,
        "color": _Color("yellow"),
    }
    ERROR = {
        "decoration": _Decoration.BOX,
        "color": _Color("red"),
        "box_title": str(MsgText.Error),
    }
    ERROR_ON_NEW_LINE = {
        "decoration": _Decoration.BOX,
        "color": _Color("red"),
        "prepend_newline": True,
        "box_title": str(MsgText.Error),
    }

    @property
    def decoration(self) -> _Decoration:
        return self.value["decoration"]

    @property
    def color(self) -> _Color:
        return self.value["color"].color

    @property
    def prepend_newline(self) -> bool:
        return self.value.get("prepend_newline", False)

    @property
    def append_space(self) -> bool:
        return self.value.get("append_space", False)

    @property
    def box_title(self) -> MsgText:
        return self.value.get("box_title", None)
