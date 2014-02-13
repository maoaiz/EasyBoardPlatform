#!/bin/bash
uwsgi --socket :8088 --wsgi-file EB/wsgi.py -d logfile.log


