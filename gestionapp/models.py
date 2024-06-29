from django.db import models
from django.db import models

class Departement(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Employe(models.Model):
    prenom = models.CharField(max_length=50)
    nom = models.CharField(max_length=50)
    email = models.EmailField()
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.prenom} {self.nom}'

class Projet(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    date_de_debut = models.DateField()
    date_de_fin = models.DateField(null=True, blank=True)
    employes = models.ManyToManyField(Employe)

    def __str__(self):
        return self.nom

# Create your models here.
