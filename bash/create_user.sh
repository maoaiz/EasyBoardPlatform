#!/bin/bash
source /home/daiech/envs/generic/bin/activate
echo 'Agregando PYTHONPATH:' $1
export PYTHONPATH="$1"
echo 'Creando usuario'
django-admin.py loaddata $2 --settings=colegio.settings
echo 'Usuario creado'