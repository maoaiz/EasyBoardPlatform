from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.conf import settings
import distutils.core
import os
import sys
import pprint
from os.path import normpath, basename
from django.utils.crypto import get_random_string


def copy_tree(from_dir, to_dir):
    return distutils.dir_util.copy_tree(from_dir, to_dir)


def create_settings_file(project_dir):
    core_dir = settings.CORE_DIR
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    secret_key = get_random_string(50, chars)  # it should be calculate
    settings_file = render_to_string("project_template/colegio/settings.py.template", locals())
    return create_file(project_dir + "/colegio/settings.py", settings_file)


def create_local_settings_file(project_dir):
    db_engine = "sqlite3" # "postgresql_psycopg2"
    db_name = basename(normpath(project_dir))
    db_user = ""
    db_pass = ""
    db_host = ""
    db_port = ""
    email_host_user = ""
    email_host_password = ""
    local_settings_file = render_to_string("project_template/colegio/local_settings.py.template", locals())
    return create_file(project_dir + "/colegio/local_settings.py", local_settings_file)


def config_project(project_dir):
    print create_settings_file(project_dir)
    print create_local_settings_file(project_dir)


def create_file(folder_dir, content):    
    f = open(folder_dir, "w")
    f.write(content.encode('UTF-8'))
    f.close()
    return f


def sync_database(project_dir):
    platform_dir = os.getcwd()
    os.chdir(project_dir)
    from subprocess import call
    call(["/bin/bash", platform_dir + "/bash/syncdb.sh", project_dir])
    os.chdir(platform_dir)


def create_new_project(name, num_users=settings.CORE_NUM_USERS):
    """run this project in a new port (uwsgi)"""
    name = slugify(name)
    port = "9001" # uWSGI port, it should be calculated

    print "CREATING PROJECT:", name
    print "uWSGI PORT:", port

    project_dir = settings.CUSTOMERS_DIR + "/" + name

    #copy the project template:
    copy_tree(settings.PROJECT_TEMPLATE_DIR, project_dir)

    config_project(project_dir)

    sync_database(project_dir)
    

    #Nginx configuration
    aux_port = port
    subdomain = name
    media_url = "{customers_dir}/{project_name}/public/media".format(customers_dir=settings.CUSTOMERS_DIR, project_name=name)
    static_url = settings.CORE_STATIC_DIR
    
    vhost_conf = render_to_string("nginx/vhost.conf.template", locals())
    print vhost_conf

    # create_file(settings.NGINX_CONFIG, vhost_conf)
    
    return True, False
