from django.shortcuts import render
from django.conf import settings
from django.views.generic.base import View
from .utils import *


class HomeView(View):

	def get(self, request):
		# sync_database(settings.CUSTOMERS_DIR + "/lina")
		msj = "Esta es la plataforma!!!"
		return render(request, "base.html", locals())

	def post(self, request):
		PROJECT_NAME = request.POST.get("name")
		if PROJECT_NAME:
			created, errors = create_new_project(PROJECT_NAME, num_users=500, email="usuario@gmail.com") # Ojo! usar Sellery Django
			if created:
				project_url = created['url']
				username = created['user']
				password = created['password']
				msj = "Nuevo proyecto '%s' creado con exito." % PROJECT_NAME
			else:
				msj = "No se creo el proyecto"
				print errors
		else:
			msj = "No hay nombre de proyecto"
		return render(request, "show_new_project.html", locals())
