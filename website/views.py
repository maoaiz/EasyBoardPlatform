from django.shortcuts import render
from django.http import Http404
from django.conf import settings
from django.views.generic.base import View
from .utils import *
from .models import *


class HomeView(View):

	def get(self, request):
		# sync_database(settings.CUSTOMERS_DIR + "/lina")
		projects = Projects.objects.filter(is_active=True)
		msj = ""
		return render(request, "home.html", locals())

	def post(self, request):
		if request.user.is_authenticated():  # TRATAR DE USAR loggin_required
			PROJECT_NAME = request.POST.get("name")
			if PROJECT_NAME:
				created, errors = create_new_project(PROJECT_NAME, num_users=750, owner=request.user) # Ojo! usar Sellery Django
				if created:
					project_url = created['url']
					username = created['user']
					password = created['password']
					# send email
					msj = "Nuevo proyecto '%s' creado con exito." % PROJECT_NAME
				else:
					msj = "No se creo el proyecto"
					print errors
			else:
				msj = "No hay nombre de proyecto"
			return render(request, "show_new_project.html", locals())
		else:
			raise Http404
