#!/bin/bash
ps -Af | grep uwsgi | grep -v grep | grep 8088 | awk '{ print $2 }' | xargs kill



