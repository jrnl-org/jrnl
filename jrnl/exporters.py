#!/usr/bin/env python
# encoding: utf-8

try: import simplejson as json
except ImportError: import json
import webbrowser
# TODO: add markdown to dependency
import markdown
import tempfile
import os
import codecs

html_skeleton = '''
<html>
<head>
    <title>%s</title>
</head>
<body>
    %s
</body>
</html>'''


def to_json(journal):
    """Returns a JSON representation of the Journal."""
    return json.dumps([e.to_dict() for e in journal.entries], indent=2)

def to_md(journal):
    """Returns a markdown representation of the Journal"""
    out = []
    year, month = -1, -1
    for e in journal.entries:
        if not e.date.year == year:
            year = e.date.year
            out.append(str(year))
            out.append("=" * len(str(year)) + "\n")
        if not e.date.month == month:
            month = e.date.month
            out.append(e.date.strftime("%B"))
            out.append('-' * len(e.date.strftime("%B")) + "\n")
        out.append(e.to_md())
    return "\n".join(out)

def to_html(journal, open_in_browser=False):
    """renders the given journal to html
        and can open it in the default browser"""
    bla = to_md(journal)
    html_body = markdown.markdown(bla.decode('utf-8'))
    print html_body
    tmp_file = os.path.join(tempfile.gettempdir(), "pretty.html")
    url = 'file://' + tmp_file
    output_file = codecs.open(tmp_file, "w", encoding="utf8")
    output_file.write(html_skeleton % (journal.config['journal'], html_body))
    webbrowser.open(url)
