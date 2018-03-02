from datetime import datetime

import htmlmin
from slimmer import html_slimmer # or xhtml_slimmer, css_slimmer

def minify(html):
    try:
        html = htmlmin.minify(html, remove_comments=True, remove_empty_space=True)
    except Exception:
        html = html_slimmer(html.strip().replace('\n',' ').replace('\t',' ').replace('\r',' '))
    return html


def timestamp_to_string(d):
    return datetime.fromtimestamp(d).strftime('%B %d, %Y')
def date_to_string(d):
    return datetime.strptime(d,'%Y-%m-%d').strftime('%B %d, %Y')