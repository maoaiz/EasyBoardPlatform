#!/bin/bash
uwsgi --socket :8001 --wsgi-file EB/wsgi.py -d logfile.log


