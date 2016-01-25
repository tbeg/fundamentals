from django.contrib import admin
from django.contrib.gis import admin
from models import House

admin.site.register(House, admin.OSMGeoAdmin)