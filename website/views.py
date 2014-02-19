from django.shortcuts import render
from django.http import Http404
from django.conf import settings
from django.views.generic.base import View
from django.template.defaultfilters import slugify
from .tasks import *
from .models import *


class HomeView(View):

	def get(self, request):
		projects = Projects.objects.filter(is_active=True)
		msj = ""
		return render(request, "home.html", locals())

	def post(self, request):
		if request.user.is_authenticated():  # TRATAR DE USAR loggin_required
			PROJECT_NAME = request.POST.get("name")
			if PROJECT_NAME:
				create_school.delay(PROJECT_NAME, num_users=750, owner=request.user) # Ojo! usar Celery Django
				project_url = "http://" + slugify(PROJECT_NAME) + "." + settings.PRINCIPAL_DOMAIN
				msj = u"El proyecto '%s' se esta creando. Se le enviara un correo electronico" % PROJECT_NAME
			else:
				msj = "No hay nombre de proyecto"
			return render(request, "show_new_project.html", locals())
		else:
			raise Http404
