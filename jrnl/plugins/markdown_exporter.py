# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import os
import re

from jrnl.messages import Message
from jrnl.messages import MsgStyle
from jrnl.messages import MsgText
from jrnl.output import print_msg
from jrnl.plugins.text_exporter import TextExporter


class MarkdownExporter(TextExporter):
    """This Exporter can convert entries and journals into Markdown."""

    names = ["md", "markdown"]
    extension = "md"

    @classmethod
    def export_entry(cls, entry, to_multifile=True):
        """Returns a markdown representation of a single entry."""
        date_str = entry.date.strftime(entry.journal.config["timeformat"])
        body_wrapper = "\n" if entry.body else ""
        body = body_wrapper + entry.body

        if to_multifile is True:
            heading = "#"
        else:
            heading = "###"

        """Increase heading levels in body text"""
        newbody = ""
        previous_line = ""
        warn_on_heading_level = False
        for line in body.splitlines(True):
            if re.match(r"^#+ ", line):
                """ATX style headings"""
                newbody = newbody + previous_line + heading + line
                if re.match(r"^#######+ ", heading + line):
                    warn_on_heading_level = True
                line = ""
            elif re.match(r"^=+$", line.rstrip()) and not re.match(
                r"^$", previous_line.strip()
            ):
                """Setext style H1"""
                newbody = newbody + heading + "# " + previous_line
                line = ""
            elif re.match(r"^-+$", line.rstrip()) and not re.match(
                r"^$", previous_line.strip()
            ):
                """Setext style H2"""
                newbody = newbody + heading + "## " + previous_line
                line = ""
            else:
                newbody = newbody + previous_line
            previous_line = line
        newbody = newbody + previous_line  # add very last line

        # make sure the export ends with a blank line
        if previous_line not in ["\r", "\n", "\r\n", "\n\r"]:
            newbody = newbody + os.linesep

        if warn_on_heading_level is True:
            print_msg(
                Message(
                    MsgText.HeadingsPastH6,
                    MsgStyle.WARNING,
                    {"date": date_str, "title": entry.title},
                )
            )

        return f"{heading} {date_str} {entry.title}\n{newbody} "

    @classmethod
    def export_journal(cls, journal):
        """Returns a Markdown representation of an entire journal."""
        out = []
        year, month = -1, -1
        for e in journal.entries:
            if not e.date.year == year:
                year = e.date.year
                out.append("# " + str(year))
                out.append("")
            if not e.date.month == month:
                month = e.date.month
                out.append("## " + e.date.strftime("%B"))
                out.append("")
            out.append(cls.export_entry(e, False))
        result = "\n".join(out)
        return result
