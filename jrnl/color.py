# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import re
from string import punctuation
from string import whitespace

import colorama

from jrnl.os_compat import on_windows

if on_windows():
    colorama.init()


def colorize(string, color, bold=False):
    """Returns the string colored with colorama.Fore.color. If the color set by
    the user is "NONE" or the color doesn't exist in the colorama.Fore attributes,
    it returns the string without any modification."""
    color_escape = getattr(colorama.Fore, color.upper(), None)
    if not color_escape:
        return string
    elif not bold:
        return color_escape + string + colorama.Fore.RESET
    else:
        return colorama.Style.BRIGHT + color_escape + string + colorama.Style.RESET_ALL


def highlight_tags_with_background_color(entry, text, color, is_title=False):
    """
    Takes a string and colorizes the tags in it based upon the config value for
    color.tags, while colorizing the rest of the text based on `color`.
    :param entry: Entry object, for access to journal config
    :param text: Text to be colorized
    :param color: Color for non-tag text, passed to colorize()
    :param is_title: Boolean flag indicating if the text is a title or not
    :return: Colorized str
    """

    def colorized_text_generator(fragments):
        """Efficiently generate colorized tags / text from text fragments.
        Taken from @shobrook. Thanks, buddy :)
        :param fragments: List of strings representing parts of entry (tag or word).
        :rtype: List of tuples
        :returns [(colorized_str, original_str)]"""
        for part in fragments:
            if part and part[0] not in config["tagsymbols"]:
                yield (colorize(part, color, bold=is_title), part)
            elif part:
                yield (colorize(part, config["colors"]["tags"], bold=True), part)

    config = entry.journal.config
    if config["highlight"]:  # highlight tags
        text_fragments = re.split(entry.tag_regex(config["tagsymbols"]), text)

        # Colorizing tags inside of other blocks of text
        final_text = ""
        previous_piece = ""
        for colorized_piece, piece in colorized_text_generator(text_fragments):
            # If this piece is entirely punctuation or whitespace or the start
            # of a line or the previous piece was a tag or this piece is a tag,
            # then add it to the final text without a leading space.
            if (
                all(char in punctuation + whitespace for char in piece)
                or previous_piece.endswith("\n")
                or (previous_piece and previous_piece[0] in config["tagsymbols"])
                or piece[0] in config["tagsymbols"]
            ):
                final_text += colorized_piece
            else:
                # Otherwise add a leading space and then append the piece.
                final_text += " " + colorized_piece

            previous_piece = piece
        return final_text.lstrip()
    else:
        return text
