#!/bin/bash
deactivate
source /home/daiech/envs/generic/bin/activate
echo "====== RUN_PROJECT.SH ======="
export PYTHONPATH="$1"
export DJANGO_SETTINGS_MODULE="colegio.settings"
uwsgi --socket :$2 --wsgi-file ./colegio/wsgi.py -d logfile.log
echo "======/RUN_PROJECT.SH ======="