#!/bin/bash
source /home/daiech/envs/generic/bin/activate
echo "====== RUN_PROJECT.SH ======="
echo $PATH
export PYTHONPATH=$1:$PYTHONPATH
# export DJANGO_SETTINGS_MODULE="colegio.settings"
uwsgi -s :$2 --wsgi-file ./colegio/wsgi.py -d logfile.log
echo "Proyecto corriendo en :$2"
echo "======/RUN_PROJECT.SH ======="