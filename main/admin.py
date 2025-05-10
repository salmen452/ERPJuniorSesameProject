from django.contrib import admin
from .models import CustomUser, Absence, Formation, Performance, Competence,ExclusionDemission, Responsable, Performance, DocumentRH

admin.site.register(CustomUser)
admin.site.register(Absence)
admin.site.register(Formation)
admin.site.register(Performance)
admin.site.register(Competence)
admin.site.register(ExclusionDemission)
admin.site.register(Responsable)
admin.site.register(DocumentRH)


# Register your models here.
