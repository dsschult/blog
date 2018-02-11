from flask import Flask
from flask import abort, redirect, url_for
from flask import render_template

from .entry import Entries

entries = Entries()

app = Flask(__name__, static_url_path='')

@app.route('/')
def main():
    e = entries.get_last_n()
    return render_template('main.html', entries=e)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/post/<name>')
def post(name):
    e = entries.get_entry(name)
    return render_template('post.html', **e)
