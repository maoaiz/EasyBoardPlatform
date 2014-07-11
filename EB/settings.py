"""
Django settings for EB project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_NAME = "EasyBoard"
PRINCIPAL_DOMAIN = "easyboard.com.co"
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p17&j3ifpre^^gu6czrjxi2szkm!vqn3yr@&j3^6&)2ics@63k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['easyboard.com.co']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'website',
    'djcelery',
    'kombu.transport.django',
)

import djcelery
djcelery.setup_loader()
BROKER_URL = "django://"
EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
CELERY_EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'EB.urls'

WSGI_APPLICATION = 'EB.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

try:
    from .local_settings import DATABASES
except Exception, e:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'ebdb.sqlite3'),
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATICFILES_DIRS = (
    os.sep.join([BASE_DIR, 'public/static']),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'


MEDIA_ROOT = os.sep.join([BASE_DIR, 'public/media'])
MEDIA_URL  = '/media/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)


LOGIN_URL = "/login"
LOGOUT_URL = "/logout"
LOGIN_REDIRECT_URL = "/"


##################### EasyBoard vars ########################
CORE_NUM_USERS = 1000
INITIAL_PORT = 9001
try:
    from .local_settings import CORE_DIR
except ImportError:
    CORE_DIR = "/home/daiech/www/django/EasyBoard/EasyBoardDEL"
try:
    from .local_settings import CORE_STATIC_DIR
except ImportError:
    CORE_STATIC_DIR = "%s/public/static" % CORE_DIR
try:
    from .local_settings import CUSTOMERS_DIR
except ImportError:
    CUSTOMERS_DIR = "/home/daiech/www/django/EasyBoard/Customers"
try:
    from .local_settings import PROJECT_TEMPLATE_DIR
except ImportError:
    PROJECT_TEMPLATE_DIR = os.sep.join([BASE_DIR, 'templates/project_template'])

NGINX_SITES_AVAILABLE='/etc/nginx/sites-available'
NGINX_SITES_ENABLED='/etc/nginx/sites-enabled'


#var to put in the new projects
try:
    from .local_settings import ADMIN_USERNAME
except ImportError:
    ADMIN_USERNAME = "del"
    
try:
    from .local_settings import ADMIN_PASSWORD
except ImportError:
    ADMIN_PASSWORD = "DelServer2014"
    
try:
    from .local_settings import ADMIN_EMAIL
except ImportError:
    ADMIN_EMAIL = "soporte@del.com.co"
    
try:
    from .local_settings import ADMIN_EMAIL_PASS
except ImportError:
    ADMIN_EMAIL_PASS = ""

############# VARS TO SEND EMAILS #############
try:
    from .local_settings import EMAIL_HOST_USER
except ImportError:
    EMAIL_HOST_USER = ""

try:
    from .local_settings import EMAIL_HOST_PASSWORD
except ImportError:
    EMAIL_HOST_PASSWORD = ""

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True


################### #######################

try:
    from .local_settings import POSTGRES_DB_USER
except ImportError:
    POSTGRES_DB_USER = "del"
    
try:
    from .local_settings import POSTGRES_DB_USER_PASS
except ImportError:
    POSTGRES_DB_USER_PASS = "DelServer2014"

try:
    from .local_settings import ENV_DIR
except ImportError:
    ENV_DIR = "/home/del/entornos/generic/bin/activate"