from django.shortcuts import render
from .models import Employe, Departement, Projet

def index(request):
    return render(request, 'gestionapp/index.html')

def liste_employes(request):
    employes = Employe.objects.all()
    return render(request, 'employes.html', {'employes': employes})

def liste_departements(request):
    departements = Departement.objects.all()
    return render(request, 'departements.html', {'departements': departements})

def liste_projets(request):
    projets = Projet.objects.all()
    return render(request, 'projets.html', {'projets': projets})
