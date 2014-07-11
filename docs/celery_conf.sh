#Copy this content in /etc/default/celeryd


# Names of nodes to start
#   most will only start one node:
CELERYD_NODES="worker"
#   but you can also start multiple and configure settings
#   for each in CELERYD_OPTS (see `celery multi --help` for examples).
###CELERYD_NODES="worker1 worker2 worker3"

# Absolute or relative path to the 'celery' command:
###CELERY_BIN="/usr/local/bin/celery"
# CELERY_BIN="/home/daiech/envs/eb/bin/celery"
CELERY_BIN="/home/del/entornos/ebplatform/bin/celery"

# App instance to use
# comment out this line if you don't use an app
CELERY_APP="EB"
# or fully qualified:
#CELERY_APP="proj.tasks:app"

# Where to chdir at start.
# CELERYD_CHDIR="/home/daiech/www/django/EasyBoard/EasyBoardPlatform"
CELERYD_CHDIR="/home/del/proyectos/EasyBoardPlatform"

# Extra command-line arguments to the worker
CELERYD_OPTS="--time-limit=300 --concurrency=8"

# %N will be replaced with the first part of the nodename.
CELERYD_LOG_FILE="/var/log/celery/%N.log"
CELERYD_PID_FILE="/var/run/celery/%N.pid"

# Workers should run as an unprivileged user.
#   You need to create this user manually (or you can choose
#   a user/group combination that already exists, e.g. nobody).
CELERYD_USER="del"
CELERYD_GROUP="del"

# If enabled pid and log directories will be created if missing,
# and owned by the userid/group configured.
CELERY_CREATE_DIRS=1

# DJANGO_SETTINGS_MODULE = "EB.settings"