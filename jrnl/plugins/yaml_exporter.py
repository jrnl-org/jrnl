# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import os
import re

from jrnl.exception import JrnlException
from jrnl.messages import Message
from jrnl.messages import MsgStyle
from jrnl.messages import MsgText
from jrnl.output import print_msg
from jrnl.plugins.text_exporter import TextExporter


class YAMLExporter(TextExporter):
    """This Exporter can convert entries and journals into Markdown formatted text with YAML front matter."""

    names = ["yaml"]
    extension = "md"

    @classmethod
    def export_entry(cls, entry, to_multifile=True):
        """Returns a markdown representation of a single entry, with YAML front matter."""
        if to_multifile is False:
            raise JrnlException(Message(MsgText.YamlMustBeDirectory, MsgStyle.ERROR))

        date_str = entry.date.strftime(entry.journal.config["timeformat"])
        body_wrapper = "\n" if entry.body else ""
        body = body_wrapper + entry.body

        tagsymbols = entry.journal.config["tagsymbols"]
        # see also Entry.Entry.rag_regex
        multi_tag_regex = re.compile(rf"(?u)^\s*([{tagsymbols}][-+*#/\w]+\s*)+$")

        """Increase heading levels in body text"""
        newbody = ""
        heading = "#"
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
            elif multi_tag_regex.match(line):
                """Tag only lines"""
                line = ""
            else:
                newbody = newbody + previous_line
            previous_line = line
        newbody = newbody + previous_line  # add very last line

        # make sure the export ends with a blank line
        if previous_line not in ["\r", "\n", "\r\n", "\n\r"]:
            newbody = newbody + os.linesep

        # set indentation for YAML body block
        spacebody = "\t"
        for line in newbody.splitlines(True):
            spacebody = spacebody + "\t" + line

        if warn_on_heading_level is True:
            print_msg(
                Message(
                    MsgText.HeadingsPastH6,
                    MsgStyle.WARNING,
                    {"date": date_str, "title": entry.title},
                )
            )

        dayone_attributes = ""
        if hasattr(entry, "uuid"):
            dayone_attributes += "uuid: " + entry.uuid + "\n"
        if (
            hasattr(entry, "creator_device_agent")
            or hasattr(entry, "creator_generation_date")
            or hasattr(entry, "creator_host_name")
            or hasattr(entry, "creator_os_agent")
            or hasattr(entry, "creator_software_agent")
        ):
            dayone_attributes += "creator:\n"
            if hasattr(entry, "creator_device_agent"):
                dayone_attributes += f"    device agent: {entry.creator_device_agent}\n"
            if hasattr(entry, "creator_generation_date"):
                dayone_attributes += "    generation date: {}\n".format(
                    str(entry.creator_generation_date)
                )
            if hasattr(entry, "creator_host_name"):
                dayone_attributes += f"    host name: {entry.creator_host_name}\n"
            if hasattr(entry, "creator_os_agent"):
                dayone_attributes += f"    os agent: {entry.creator_os_agent}\n"
            if hasattr(entry, "creator_software_agent"):
                dayone_attributes += (
                    f"    software agent: {entry.creator_software_agent}\n"
                )

        # TODO: copy over pictures, if present
        # source directory is  entry.journal.config['journal']
        # output directory is...?

        return "{start}\ntitle: {title}\ndate: {date}\nstarred: {starred}\ntags: {tags}\n{dayone}body: |{body}{end}".format(
            start="---",
            date=date_str,
            title=entry.title,
            starred=entry.starred,
            tags=", ".join([tag[1:] for tag in entry.tags]),
            dayone=dayone_attributes,
            body=spacebody,
            end="...",
        )

    @classmethod
    def export_journal(cls, journal):
        """Returns an error, as YAML export requires a directory as a target."""
        raise JrnlException(Message(MsgText.YamlMustBeDirectory, MsgStyle.ERROR))
