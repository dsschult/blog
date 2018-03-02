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
        self.db = sqlite3.connect('entries.db')
        self.entries = {}
        self.init()

    def get(self, name):
        if name not in self.entries:
            raise KeyError('No such entry')
        return self._process(name, get_entry)

    def get_last_n(self, n=10):
        names = sorted(self.entries, key=lambda x:self.entries[x]['date_modified'], reverse=True)[:n]
        ret = []
        for name in names:
            ret.append(self._process(name, get_entry_teaser))
        return ret

    def _process(self, name, func):
        ret = self.entries[name].copy()
        meta, data = func(name)
        ret['url'] = name
        ret['data'] = data
        ret['name'] = name
        ret['title'] = meta.get('title', name.title())
        ret['date_modified'] = timestamp_to_string(ret['date_modified'])
        ret['date_posted'] = date_to_string(meta['date']) if 'date' in meta else ret['date_modified']
        return ret

    def init(self):
        with self.db:
            self.db.execute('CREATE TABLE IF NOT EXISTS entries (name, date_modified, size)')

        entries = set(list_entries())

        cur = self.db.cursor()
        cur.execute('SELECT * FROM entries')
        db_entries = {}
        for name,dm,s in cur.fetchall():
            db_entries[name] = {'date_modified':dm,
                                'size':s}

        db_entries_set = set(db_entries)
        insert_entries = entries - db_entries_set
        delete_entries = db_entries_set - entries
        update_entries = {}
        for name in db_entries_set & entries:
            md = get_entry_metadata(name)
            if db_entries[name] != md:
                update_entries[name] = md
                self.entries[name] = md
            else:
                self.entries[name] = db_entries[name]

        with self.db:
            sql = 'DELETE FROM entries WHERE name=?'
            for name in delete_entries:
                cur.execute(sql, (name,))

            sql = 'INSERT INTO entries (name, date_modified, size) VALUES (?,?,?)'
            for name in insert_entries:
                md = get_entry_metadata(name)
                bindings = (name,md['date_modified'],md['size'])
                cur.execute(sql, bindings)
                self.entries[name] = md

            sql = 'UPDATE entries SET date_modified=?, size=? WHERE name=?'
            for name in update_entries:
                bindings = (md['date_modified'],md['size'],name)
                cur.execute(sql, bindings)


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
        data = data.rstrip()+'\n<a href="/entries/'+name+'">&raquo;more</a>'
        return to_html(data)

def get_entry_metadata(name):
    path = os.path.join(basedir,'entries',name+'.md')
    dm = os.path.getmtime(path)
    s = os.path.getsize(path)
    return {'date_modified': dm,
            'size': s}
