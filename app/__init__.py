from flask import Flask
from flask import abort, redirect, url_for
from flask import render_template

app = Flask(__name__, static_url_path='')

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/about')
def about():
    return render_template('about.html')

