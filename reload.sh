#!/bin/bash
ps -Af | grep uwsgi | grep -v grep | grep 8088 | awk '{ print $2 }' | xargs kill
echo Stopped...
echo Wait...
sleep 1
uwsgi --socket :8088 --wsgi-file colegio/wsgi.py -d logfile.log
echo Started...




