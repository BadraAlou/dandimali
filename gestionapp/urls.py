from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('employes/', views.liste_employes, name='liste_employes'),
    path('departements/', views.liste_departements, name='liste_departements'),
    path('projets/', views.liste_projets, name='liste_projets'),
]
