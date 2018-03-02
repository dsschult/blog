from datetime import datetime

import htmlmin

def minify(html):
    try:
        html = htmlmin.minify(html, remove_comments=True, remove_empty_space=True)
    except Exception:
        pass
    return html


def timestamp_to_string(d):
    return datetime.fromtimestamp(d).strftime('%B %d, %Y')
def date_to_string(d):
    return datetime.strptime(d,'%Y-%m-%d').strftime('%B %d, %Y')
