from django.contrib import admin
from clinica.models import * 

admin.site.register([Worker, Client, Location, Service, Appointement])