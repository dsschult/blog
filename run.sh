#!/bin/bash
source venv/bin/activate

gunicorn app:app -b 127.0.0.1:5000 -w 2
