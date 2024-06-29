from django.contrib import admin
# gestionapp/admin.py

from django.contrib import admin
from .models import Departement, Employe, Projet

@admin.register(Employe)
class EmployeAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'nom', 'email', 'departement')
    list_filter = ('departement',)
    search_fields = ('prenom', 'nom', 'email')

# Register your models here.
admin.site.register(Departement)
admin.site.register(Projet)

# Register your models here.
