#!/bin/bash
source ~/envs/eb/bin/activate
export PYTHONPATH="$1"
uwsgi --socket :$2 --wsgi-file colegio/wsgi.py -d logfile.log