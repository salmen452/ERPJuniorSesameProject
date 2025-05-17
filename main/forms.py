from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _

from .models import (
    CustomUser, Absence, Formation, Competence, ExclusionDemission, 
    Responsable, Performance, DocumentRH, HistoriqueDocument,
    NotificationRetour, ObjectifMembre
)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'telephone', 'adresse_postale', 'date_adhesion']

UserModel = get_user_model()

class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput(attrs={'autofocus': True}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': _("Please enter a correct email and password."),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            try:
                user_obj = UserModel.objects.get(email__iexact=email)
            except UserModel.DoesNotExist:
                user_obj = None
            if user_obj:
                self.user_cache = authenticate(self.request,username=user_obj.username,password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                )
            else:
                if not self.user_cache.is_active:
                    raise forms.ValidationError(
                        self.error_messages['inactive'],
                        code='inactive',
                    )
        return self.cleaned_data

    def get_user(self):
        return self.user_cache

# Additional forms for HR management

class AbsenceForm(forms.ModelForm):
    class Meta:
        model = Absence
        fields = ['date_debut', 'date_fin', 'motif', 'details_motif', 'certificat_medical']
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
        }

class NotificationRetourForm(forms.ModelForm):
    class Meta:
        model = NotificationRetour
        fields = ['message']
        
class FormationForm(forms.ModelForm):
    class Meta:
        model = Formation
        fields = ['intitule', 'organisme', 'date_debut', 'date_fin', 'niveau', 'certification', 'description', 'document_certification']
        widgets = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
        }
        
class CompetenceForm(forms.ModelForm):
    class Meta:
        model = Competence
        fields = ['code', 'libelle', 'categorie', 'niveau']

class ExclusionDemissionForm(forms.ModelForm):
    class Meta:
        model = ExclusionDemission
        fields = ['type', 'date_effet', 'motif', 'document_reference', 'document_file', 'notes_additionnelles']
        widgets = {
            'date_effet': forms.DateInput(attrs={'type': 'date'}),
        }
        
class PerformanceForm(forms.ModelForm):
    class Meta:
        model = Performance
        fields = ['note', 'commentaires', 'forces', 'axes_amelioration', 'objectifs', 'objectifs_atteints', 'date_prochain_suivi']
        widgets = {
            'date_prochain_suivi': forms.DateInput(attrs={'type': 'date'}),
        }
        
class ObjectifMembreForm(forms.ModelForm):
    class Meta:
        model = ObjectifMembre
        fields = ['description', 'date_echeance', 'status', 'commentaires']
        widgets = {
            'date_echeance': forms.DateInput(attrs={'type': 'date'}),
        }
        
class DocumentRHForm(forms.ModelForm):
    class Meta:
        model = DocumentRH
        fields = ['titre', 'type', 'description', 'fichier', 'version', 'accessible_a']
        
class HistoriqueDocumentForm(forms.ModelForm):
    class Meta:
        model = HistoriqueDocument
        fields = ['version', 'description_changements']

class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'telephone', 'adresse_postale']
