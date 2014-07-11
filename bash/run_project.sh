#!/bin/bash
source $3
echo "====== RUN_PROJECT.SH ======="
export PYTHONPATH=$1:$PYTHONPATH
# export DJANGO_SETTINGS_MODULE="colegio.settings"
uwsgi -s :$2 --wsgi-file ./colegio/wsgi.py -d logfile.log
echo "Proyecto corriendo en :$2"
echo "======/RUN_PROJECT.SH ======="