from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.conf import settings
import distutils.core
import os
import sys
import pprint

def copy_tree(from_dir, to_dir):
    return distutils.dir_util.copy_tree(from_dir, to_dir)


def sync_database(project_dir):
    from django.core.management import call_command
    print "==========================syncdb====================================="
    print os.getcwd()
    print os.chdir(project_dir)
    print os.getcwd()
    # pprint.pprint(sys.path)
    sys.path.insert(0, project_dir)
    # print "NEW PATH========================="
    # pprint.pprint(sys.path)
    from subprocess import call
    # print call(["ls"])
    # print call(["cat", "manage.py"])
    print call(["django-admin.py", "syncdb", "--noinput", "--settings=django_crud_example.settings"])
    # print call(["python", project_dir + "/manage.py", "syncdb", "--noinput"])
    # print call_command('syncdb', interactive=False)
    print "==========================/syncdb===================================="


def create_new_project(name):
    """run this project in a new port (uwsgi)"""
    name = slugify(name)
    port = "9001" # uWSGI port, it should be calculated

    new_project_dir = settings.CUSTOMERS_DIR + "/" + name

    print "CREATING PROJECT:", name
    print "uWSGI PORT:", port

    #copy the project template:
    copy_tree(settings.PROJECT_TEMPLATE_DIR, new_project_dir)
    sync_database(new_project_dir)

    aux_port = port
    subdomain = name
    media_url = "{customers_dir}/{project_name}/media".format(customers_dir=settings.CUSTOMERS_DIR, project_name=name)
    

    vhost_conf = render_to_string("nginx/vhost.conf.template", locals())
    print vhost_conf
    
    # copy_tree(settings.BASE_DIR + "/templates/nginx", settings.NGINX_CONFIG)
    return True, False
