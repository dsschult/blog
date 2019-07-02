#!/bin/bash
python3 -m virtualenv -p python3 venv
. venv/bin/activate
pip install jinja2 markdown pygments htmlmin slimit
