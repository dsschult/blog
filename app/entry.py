import os
import re
import sqlite3
import logging
from functools import partial

import markdown

from .util import timestamp_to_string, date_to_string

basedir = os.path.dirname(os.path.abspath(__file__))

markdown_extensions = [
    'markdown.extensions.codehilite',
    'markdown.extensions.nl2br',
    'markdown.extensions.meta',
]
markdown_extension_configs = {
    'markdown.extensions.codehilite': {
        'guess_lang': True,
        'linenums': False
    },
}
def to_html(data):
    md = markdown.Markdown(output_format='html5',
                           extensions=markdown_extensions,
                           extension_configs=markdown_extension_configs)
    html = md.convert(data)
    meta = {}
    for key in md.Meta:
        if not md.Meta[key]:
            meta[key] = ''
        elif len(md.Meta[key]) == 1:
            meta[key] = md.Meta[key][0]
        else:
            meta[key] = ', '.join(md.Meta[key])
    return (meta, html)

class Entries:
    def __init__(self):
        self.entries = {}
        for name in list_entries():
            self.entries[name] = get_entry_metadata(name)

    def get(self, name):
        if name not in self.entries:
            raise KeyError('No such entry')
        return self._process(name, get_entry)

    def get_names(self):
        return self.entries.keys()

    def get_last_n(self, n=10):
        names = sorted(self.entries, key=lambda x:self.entries[x]['mtime'], reverse=True)[:n*2]
        ret = []
        for name in names:
            ret.append(self._process(name, get_entry_teaser))
        return sorted(ret, key=lambda x:x['date_posted'], reverse=True)[:n]

    def _process(self, name, func):
        ret = self.entries[name].copy()
        meta, data = func(name)
        ret['url'] = name+'.html'
        ret['data'] = data
        ret['name'] = name
        ret['title'] = meta.get('title', name.title())
        ret['date_posted'] = date_to_string(meta['date']) if 'date' in meta else timestamp_to_string(ret['mtime'])
        ret['date_modified'] = date_to_string(meta['date']) if 'modified' in meta else timestamp_to_string(ret['mtime'])
        return ret

### raw functions ###

def list_entries():
    return [x.replace('.md','') for x in os.listdir(os.path.join(basedir,'entries')) if x.endswith('.md')]

def get_entry(name):
    with open(os.path.join(basedir,'entries',name+'.md'),'r') as f:
        return to_html(f.read())

def get_entry_teaser(name):
    with open(os.path.join(basedir,'entries',name+'.md'),'r') as f:
        data = ''
        i = 0
        for line in f:
            if i > 10 and not line.strip():
                break
            data += line
            i += 1
        data = data.rstrip()+'\n<a href="/entries/'+name+'.html">&raquo;more</a>'
        return to_html(data)

def get_entry_metadata(name):
    path = os.path.join(basedir,'entries',name+'.md')
    dm = os.path.getmtime(path)
    s = os.path.getsize(path)
    return {'mtime': dm,
            'size': s}
