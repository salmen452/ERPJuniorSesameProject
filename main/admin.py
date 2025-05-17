from django.contrib import admin
from .models import (
    CustomUser, Absence, Formation, Performance, Competence, 
    ExclusionDemission, Responsable, DocumentRH, HistoriqueDocument,
    NotificationRetour, ObjectifMembre
)

class AbsenceAdmin(admin.ModelAdmin):
    list_display = ('membre', 'date_debut', 'date_fin', 'motif', 'notif_retour')
    list_filter = ('motif', 'notif_retour', 'certificat_medical')
    search_fields = ('membre__username', 'membre__email', 'motif')

class FormationAdmin(admin.ModelAdmin):
    list_display = ('intitule', 'membre', 'organisme', 'date_debut', 'date_fin', 'certification')
    list_filter = ('certification', 'niveau')
    search_fields = ('intitule', 'membre__username', 'organisme')

class CompetenceAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'categorie', 'niveau', 'membre')
    list_filter = ('categorie', 'niveau')
    search_fields = ('libelle', 'membre__username')

class ExclusionDemissionAdmin(admin.ModelAdmin):
    list_display = ('membre', 'type', 'date_effet', 'traite_par')
    list_filter = ('type',)
    search_fields = ('membre__username', 'motif')

class PerformanceAdmin(admin.ModelAdmin):
    list_display = ('membre', 'responsable', 'date_evaluation', 'note', 'objectifs_atteints')
    list_filter = ('objectifs_atteints', 'date_evaluation')
    search_fields = ('membre__username', 'responsable__utilisateur__username')

class DocumentRHAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type', 'version', 'date_creation', 'dernier_modif')
    list_filter = ('type',)
    search_fields = ('titre', 'description')

admin.site.register(CustomUser)
admin.site.register(Absence, AbsenceAdmin)
admin.site.register(Formation, FormationAdmin)
admin.site.register(Performance, PerformanceAdmin)
admin.site.register(Competence, CompetenceAdmin)
admin.site.register(ExclusionDemission, ExclusionDemissionAdmin)
admin.site.register(Responsable)
admin.site.register(DocumentRH, DocumentRHAdmin)
admin.site.register(HistoriqueDocument)
admin.site.register(NotificationRetour)
admin.site.register(ObjectifMembre)
