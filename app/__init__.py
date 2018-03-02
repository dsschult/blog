from flask import Flask
from flask import abort, redirect, url_for
from flask import render_template

from .entry import Entries
from .util import minify

blog_entries = Entries()

app = Flask(__name__, static_url_path='')

@app.route('/')
def main():
    e = blog_entries.get_last_n()
    return minify(render_template('main.html', entries=e))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/entries/<name>')
def entries(name):
    e = blog_entries.get(name)
    return render_template('entries.html', **e)
