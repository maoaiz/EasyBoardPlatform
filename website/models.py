#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User


class ProjectsManager(models.Manager):

    def get_last_port(self):
        obj = self.all().order_by("-port")
        if obj.count() > 0:
            return obj[0].port
        else:
            return None


class Projects(models.Model):
    user_owner = models.ForeignKey(User,null=True, blank=True, related_name='%(class)s_user_owner')
    project_name = models.CharField(max_length=150, verbose_name="Project name")
    project_url = models.CharField(max_length=150, verbose_name="Project url")
    port = models.CharField(max_length=150, verbose_name="port")
    num_members = models.IntegerField(max_length=4, verbose_name="Numero de usuarios")

    objects = ProjectsManager()

    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s:%s" % (self.project_name, self.port)
