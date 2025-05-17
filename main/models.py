from django.db import models
from django.contrib.auth.models import AbstractUser, Group

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, blank=True)
    adresse_postale = models.TextField(blank=True)
    date_adhesion = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username

class Absence(models.Model):
    MOTIF_CHOICES = [
        ('maladie', 'Maladie'),
        ('congé', 'Congé'),
        ('formation', 'Formation Externe'),
        ('familial', 'Raison Familiale'),
        ('autre', 'Autre'),
    ]
    
    membre = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='absences')
    date_debut = models.DateField()
    date_fin = models.DateField()
    motif = models.CharField(max_length=50, choices=MOTIF_CHOICES)
    details_motif = models.TextField(blank=True)
    certificat_medical = models.BooleanField(default=False)
    notif_retour = models.BooleanField(default=False)
    retour_verifie = models.BooleanField(default=False)
    date_notification = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.membre.username} - {self.date_debut} à {self.date_fin}"
        
    class Meta:
        verbose_name = "Absence"
        verbose_name_plural = "Absences"

class Formation(models.Model):
    NIVEAU_CHOICES = [
        ('debutant', 'Débutant'),
        ('intermediaire', 'Intermédiaire'),
        ('avance', 'Avancé'),
        ('expert', 'Expert'),
    ]
    
    membre = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='formations')
    intitule = models.CharField(max_length=100)
    organisme = models.CharField(max_length=100)
    date_debut = models.DateField()
    date_fin = models.DateField()
    certification = models.BooleanField(default=False)
    niveau = models.CharField(max_length=20, choices=NIVEAU_CHOICES, default='debutant')
    description = models.TextField(blank=True)
    document_certification = models.FileField(upload_to='certifications/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.intitule} - {self.membre.username}"
        
    class Meta:
        verbose_name = "Formation"
        verbose_name_plural = "Formations"

class Competence(models.Model):
    CATEGORIES = [
        ('technique', 'Compétence Technique'),
        ('soft', 'Soft Skill'),
        ('management', 'Management'),
        ('langue', 'Langue'),
        ('autre', 'Autre'),
    ]
    
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, related_name='competences', null=True, blank=True)
    membre = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='competences', null=True)
    code = models.CharField(max_length=20)
    libelle = models.CharField(max_length=100)
    categorie = models.CharField(max_length=100, choices=CATEGORIES)
    niveau = models.IntegerField(default=1, choices=[(i, i) for i in range(1, 6)])  # Niveau de 1 à 5
    date_acquisition = models.DateField(auto_now_add=False, default='2023-01-01')
    
    def __str__(self):
        return f"{self.libelle} ({self.categorie}) - Niveau {self.niveau}"
        
    class Meta:
        verbose_name = "Compétence"
        verbose_name_plural = "Compétences"

class ExclusionDemission(models.Model):
    TYPE_CHOICES = [
        ('exclusion', 'Exclusion'),
        ('demission', 'Démission'),
    ]
    
    membre = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='exclusions_demissions')
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    date_effet = models.DateField()
    motif = models.TextField()
    document_reference = models.CharField(max_length=255)
    document_file = models.FileField(upload_to='documents_exclusion/', null=True, blank=True)
    notes_additionnelles = models.TextField(blank=True)
    traite_par = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='exclusions_traitees')
    
    def __str__(self):
        return f"{self.get_type_display()} - {self.membre.username} ({self.date_effet})"
        
    class Meta:
        verbose_name = "Exclusion ou Démission"
        verbose_name_plural = "Exclusions et Démissions"

class Responsable(models.Model):
    utilisateur = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profil_responsable')
    poste = models.CharField(max_length=100)
    departement = models.CharField(max_length=100)
    date_nomination = models.DateField()
    
    def __str__(self):
        return f"{self.utilisateur.get_full_name()} - {self.poste}"
        
    class Meta:
        verbose_name = "Responsable"
        verbose_name_plural = "Responsables"

class Performance(models.Model):
    NOTES_CHOICES = [(i/2, i/2) for i in range(0, 11)]  # Notes de 0 à 5 par 0.5
    
    membre = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='performances')
    responsable = models.ForeignKey(Responsable, on_delete=models.SET_NULL, null=True, related_name='evaluations')
    date_evaluation = models.DateField()
    note = models.FloatField(choices=NOTES_CHOICES)
    commentaires = models.TextField()
    forces = models.TextField(blank=True)
    axes_amelioration = models.TextField(blank=True)
    objectifs = models.TextField()
    objectifs_atteints = models.BooleanField(default=False)
    date_prochain_suivi = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"Évaluation de {self.membre.username} - {self.date_evaluation}"
        
    class Meta:
        verbose_name = "Performance"
        verbose_name_plural = "Performances"

class DocumentRH(models.Model):
    TYPE_CHOICES = [
        ('politique', 'Politique RH'),
        ('procedure', 'Procédure'),
        ('formulaire', 'Formulaire'),
        ('contrat', 'Contrat'),
        ('autre', 'Autre'),
    ]
    
    titre = models.CharField(max_length=200)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    description = models.TextField(blank=True)
    fichier = models.FileField(upload_to='documents_rh/')
    date_creation = models.DateField(auto_now_add=True)
    dernier_modif = models.DateField(auto_now=True)
    version = models.CharField(max_length=20)
    cree_par = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='documents_crees')
    modifie_par = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='documents_modifies')
    accessible_a = models.ManyToManyField(Group, related_name='documents_accessibles')
    
    def __str__(self):
        return f"{self.titre} (v{self.version})"
        
    class Meta:
        verbose_name = "Document RH"
        verbose_name_plural = "Documents RH"

# New models for HR management
class HistoriqueDocument(models.Model):
    document = models.ForeignKey(DocumentRH, on_delete=models.CASCADE, related_name='historique')
    version = models.CharField(max_length=20)
    date_modification = models.DateTimeField(auto_now_add=True)
    modifie_par = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    description_changements = models.TextField()
    
    def __str__(self):
        return f"{self.document.titre} - v{self.version} ({self.date_modification})"
    
    class Meta:
        verbose_name = "Historique de document"
        verbose_name_plural = "Historique des documents"
        ordering = ['-date_modification']

class NotificationRetour(models.Model):
    absence = models.ForeignKey(Absence, on_delete=models.CASCADE, related_name='notifications')
    date_envoi = models.DateField(auto_now_add=True)
    message = models.TextField()
    envoye_par = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='notifications_envoyees')
    
    def __str__(self):
        return f"Notification pour {self.absence.membre.username} ({self.date_envoi})"
    
    class Meta:
        verbose_name = "Notification de retour"
        verbose_name_plural = "Notifications de retour"
        
class ObjectifMembre(models.Model):
    STATUS_CHOICES = [
        ('non_commence', 'Non commencé'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('annule', 'Annulé'),
    ]
    
    membre = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='objectifs')
    description = models.TextField()
    date_creation = models.DateField(auto_now_add=True)
    date_echeance = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='non_commence')
    responsable_suivi = models.ForeignKey(Responsable, on_delete=models.SET_NULL, null=True, related_name='objectifs_suivis')
    commentaires = models.TextField(blank=True)
    
    def __str__(self):
        return f"Objectif de {self.membre.username} - {self.status}"
    
    class Meta:
        verbose_name = "Objectif membre"
        verbose_name_plural = "Objectifs membres"
