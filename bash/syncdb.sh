#!/bin/bash
source $2
# echo 'Agregando PYTHONPATH:' $1
export PYTHONPATH="$1"
echo 'Sincronizando base de datos'
django-admin.py syncdb --noinput --settings=colegio.settings
echo '********************Sincronizacion terminada********************'