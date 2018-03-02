#!/bin/bash
python3 -m virtualenv venv
. venv/bin/activate
pip install Flask gunicorn markdown pygments htmlmin slimit
