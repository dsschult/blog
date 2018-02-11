import os
import sqlite3
from datetime import datetime

import markdown

basedir = os.path.dirname(os.path.abspath(__file__))

class Entries:
    def __init__(self):
        self.db = sqlite3.connect('entries.db')
        self.entries = {}
        self.init()

    def get(self, name):
        if name not in self.entries:
            raise KeyError('No such entry')
        ret = self.entries[name].copy()
        ret['data'] = get_entry(name)
        return ret

    def get_last_n(self, n=10):
        names = sorted(self.entries, key=lambda x:self.entries[x]['date_created'])[:n]
        ret = []
        for name in names:
            r = self.entries[name].copy()
            r['name'] = name
            r['data'] = get_entry_teaser(name)
            ret.append(r)
        return ret

    def init(self):
        with self.db:
            self.db.execute('CREATE TABLE IF NOT EXISTS entries (name, date_created, date_modified, size)')

        entries = set(list_entries())

        cur = self.db.cursor()
        cur.execute('SELECT * FROM entries')
        db_entries = {}
        for name,dc,dm,s in cur.fetchall():
            db_entries[name] = {'date_created':dc,
                                'date_modified':dm,
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

            sql = 'INSERT INTO entries (name, date_created, date_modified, size) VALUES (?,?,?,?)'
            for name in insert_entries:
                md = get_entry_metadata(name)
                bindings = (name,md['date_created'],md['date_modified'],md['size'])
                cur.execute(sql, bindings)
                self.entries[name] = md

            sql = 'UPDATE entries SET date_created=?, date_modified=?, size=? WHERE name=?'
            for name in update_entries:
                bindings = (md['date_created'],md['date_modified'],md['size'],name)
                cur.execute(sql, bindings)


### raw functions ###

def list_entries():
    return [x.replace('.md','') for x in os.listdir(os.path.join(basedir,'entries')) if x.endswith('.md')]

def get_entry(name):
    with open(os.path.join(basedir,'entries',name+'.md')) as f:
        return markdown.markdown(f.read(), output_format='html5')

def get_entry_teaser(name):
    with open(os.path.join(basedir,'entries',name+'.md')) as f:
        data = ''
        i = 0
        for line in f:
            if i > 10 and not line.strip():
                break
            data += line+'\n'
            i += 1
        data = data.rstrip()+' ...'
        return markdown.markdown(data, output_format='html5')

def get_entry_metadata(name):
    path = os.path.join(basedir,'entries',name+'.md')
    dc = os.path.getctime(path)
    dm = os.path.getmtime(path)
    s = os.path.getsize(path)
    return {'date_created': dc,
            'date_modified': dm,
            'size': s}
