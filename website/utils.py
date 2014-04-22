from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from .models import Projects
import distutils.core
from subprocess import call
import os
from os.path import normpath, basename
import sys


def copy_tree(from_dir, to_dir):
    return distutils.dir_util.copy_tree(from_dir, to_dir)


def create_file(folder_dir, content):    
    f = open(folder_dir, "w")
    f.write(content.encode('UTF-8'))
    f.close()
    return f


def delete_file(file_dir):
    if os.path.isfile(file_dir):
        os.remove(file_dir)
    else:    ## Show an error ##
        print("Error: '%s' file not found" % file_dir)


def get_json_for_new_user(platform_dir, project_name, id=1, username=settings.ADMIN_USERNAME, password=settings.ADMIN_PASSWORD, email=settings.ADMIN_EMAIL):
    current_dir = os.getcwd()
    os.chdir(platform_dir)
    password = make_password(password)
    json = render_to_string(platform_dir + "/templates/fixtures/initial_data.json.template", locals())
    f = create_file(platform_dir + "/temp/" + project_name + ".json", json)
    os.chdir(current_dir)
    return f.name


def create_postgresdb(project_name):
    """Crea una bd en el motor postgresql y retorna las credenciales"""
    db_name = "db_" + project_name
    db_user = settings.POSTGRES_DB_USER
    db_pass = settings.POSTGRES_DB_USER_PASS
    print "... creando base de datos"
    return db_name, db_user, db_pass


def create_settings_file(project_dir, num_users=settings.CORE_NUM_USERS):
    core_dir = settings.CORE_DIR
    secret_key = get_random_string(50, 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)')
    settings_file = render_to_string("project_template/colegio/settings.py.template", locals())
    create_file(project_dir + "/colegio/settings.py", settings_file)
    # remove template
    delete_file(project_dir + "/colegio/settings.py.template")


def create_local_settings_file(project_dir):
    db_name, db_user, db_pass = create_postgresdb(basename(normpath(project_dir)))
    db_engine = "postgresql_psycopg2"
    db_host = ""
    db_port = ""
    email_host_user = settings.ADMIN_EMAIL
    email_host_password = settings.ADMIN_EMAIL_PASS
    local_settings_file = render_to_string("project_template/colegio/local_settings.py.template", locals())
    create_file(project_dir + "/colegio/local_settings.py", local_settings_file)
    # remove template
    delete_file(project_dir + "/colegio/local_settings.py.template")


def config_project(project_dir, num_users=settings.CORE_NUM_USERS):
    create_settings_file(project_dir, num_users=num_users)
    create_local_settings_file(project_dir)


def sync_database(project_dir, email=settings.ADMIN_EMAIL):
    platform_dir = os.getcwd()
    os.chdir(project_dir)
    # Syncdb with initial fixtures (No users charged)
    call(["/bin/bash", platform_dir + "/bash/syncdb.sh", project_dir])

    #### CREATE USERS ####
    # admin DEL, id = 1
    json_dir = get_json_for_new_user(platform_dir, basename(normpath(project_dir)))  # Json para hacer load_data de un usuario
    call(["/bin/bash", platform_dir + "/bash/create_user.sh", project_dir, json_dir])
    delete_file(json_dir)

    # admin school
    id = 2
    username = "admin"
    psw = get_random_string(8, 'abcdefghijklmnopqrstuvwxyz0123456789')
    email = email
    json_dir = get_json_for_new_user(platform_dir, basename(normpath(project_dir)), id=id, username=username, password=psw, email=email)
    call(["/bin/bash", platform_dir + "/bash/create_user.sh", project_dir, json_dir])
    delete_file(json_dir)

    os.chdir(platform_dir)
    return username, psw
    

def create_bash_scripts(project_dir, port):
    _reload = render_to_string("nginx/reload.sh.template", locals())
    create_file(project_dir + "/reload.sh", _reload)

    _start = render_to_string("nginx/start.sh.template", locals())
    create_file(project_dir + "/start.sh", _start)
    
    _stop = render_to_string("nginx/stop.sh.template", locals())
    create_file(project_dir + "/stop.sh", _stop)


def get_available_port():
    last = Projects.objects.get_last_port()
    if last:
        return int(last) + 1
    else:
        return settings.INITIAL_PORT


def create_vhost(subdomain, aux_port):
    media_url = "{customers_dir}/{project_name}/public/media".format(customers_dir=settings.CUSTOMERS_DIR, project_name=subdomain)
    static_url = settings.CORE_STATIC_DIR
    content = render_to_string("nginx/vhost.conf.template", locals())
    f = create_file(os.getcwd() + "/temp/" + subdomain + ".conf", content)
    return f


def run_server(project_dir, name):
    port = get_available_port() # uWSGI port
    
    # create scritps to run project
    create_bash_scripts(project_dir, port)

    vhost = create_vhost(name, port)
    
    vhost_dir = vhost.name
    vhost_name = name + ".conf"

    os.system( " ".join(["sudo", "/usr/bin/eb.sh", vhost_dir, vhost_name]) )  # This script config the nginx vhost
    
    platform_dir = os.getcwd()
    os.chdir(project_dir)
    os.system( " ".join(["env", "-i", "/bin/bash", platform_dir + "/bash/run_project.sh", "`pwd`", str(port)]) )
    os.chdir(platform_dir)
    return port



def create_new_project(project_name, num_users=settings.CORE_NUM_USERS, owner=None):
    """run this project in a new port (uwsgi)"""
    email = settings.ADMIN_EMAIL
    if owner:
        email = owner.email
    name = slugify(project_name) # WARNIGN!!!! Validate project_name
    project_dir = settings.CUSTOMERS_DIR + "/" + name

    #copy the project template:
    copy_tree(settings.PROJECT_TEMPLATE_DIR, project_dir)

    #config data into project
    config_project(project_dir, num_users=num_users)

    #syncronize the data base
    user, psw = sync_database(project_dir, email=email)

    #Nginx configuration
    port = run_server(project_dir, name)

    url = "http://" + name + "." + settings.PRINCIPAL_DOMAIN
    if user and psw:
        Projects.objects.create(user_owner=owner, project_name=project_name, project_url=name, port=port, num_members=num_users)
        return {"user": user, "password": psw, "url": url}, False
    else:
        return False, "No se pudo crear el colegio, contacte con el adminitrador"
