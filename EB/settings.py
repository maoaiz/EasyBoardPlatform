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


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p17&j3ifpre^^gu6czrjxi2szkm!vqn3yr@&j3^6&)2ics@63k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'website'
)

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
    ADMIN_PASSWORD = "123456"
    
try:
    from .local_settings import ADMIN_EMAIL
except ImportError:
    ADMIN_EMAIL = "soporte@del.com.co"
    
try:
    from .local_settings import ADMIN_EMAIL_PASS
except ImportError:
    ADMIN_EMAIL_PASS = ""
