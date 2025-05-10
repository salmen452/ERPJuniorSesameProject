from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, blank=True)
    adresse_postale = models.TextField(blank=True)
    date_adhesion = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username

class Absence(models.Model):
    membre = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_debut = models.DateField()
    date_fin = models.DateField()
    motif = models.TextField()
    certificat_medical = models.BooleanField(default=False)
    notif_retour = models.BooleanField(default=False)

class Formation(models.Model):
    membre = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    intitule = models.CharField(max_length=100)
    organisme = models.CharField(max_length=100)
    date_debut = models.DateField()
    date_fin = models.DateField()
    certification = models.BooleanField(default=False)

class Competence(models.Model):
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE)
    code = models.CharField(max_length=20)
    libelle = models.CharField(max_length=100)
    categorie = models.CharField(max_length=100)

class ExclusionDemission(models.Model):
    membre = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    date_effet = models.DateField()
    motif = models.TextField()
    document_reference = models.CharField(max_length=255)

class Responsable(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    poste = models.CharField(max_length=100)

class Performance(models.Model):
    membre = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    responsable = models.ForeignKey(Responsable, on_delete=models.SET_NULL, null=True)
    date_evaluation = models.DateField()
    note = models.FloatField()
    commentaires = models.TextField()
    objectifs_atteints = models.BooleanField(default=False)

class DocumentRH(models.Model):
    titre = models.CharField(max_length=200)
    type = models.CharField(max_length=100)
    date_creation = models.DateField()
    dernier_modif = models.DateField()
    version = models.CharField(max_length=20)
