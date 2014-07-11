from __future__ import absolute_import

from celery import shared_task
from django.conf import settings
from website.utils import create_new_project
from website.send_email import sendEmail
from django.utils.translation import ugettext as _


@shared_task
def create_school(project_name, num_users=settings.CORE_NUM_USERS, owner=None):
    print "======================= CREANDO PROYECTO ======================="
    created, error = create_new_project(project_name, num_users=num_users, owner=owner)
    if created:
        full_name = _("Usuario")
        email = settings.ADMIN_EMAIL
        if owner:
            full_name = owner.get_full_name()
            email = owner.email if owner.email != "" else email
        ctx = {
            "full_name": full_name,
            "school_url": created['url'],
            "username": created['user'],
            "password": created['password'],
        }
        is_sent = sendEmail("#SEND_CREDENTIALS", ctx, to=[email])
    print "======================= PROYECTO CREADO ========================"
	