from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.db.models import Q

from .models import (
    CustomUser, Absence, Formation, Competence, ExclusionDemission, 
    Responsable, Performance, DocumentRH, HistoriqueDocument,
    NotificationRetour, ObjectifMembre
)
from .forms import (
    AbsenceForm, NotificationRetourForm, FormationForm, CompetenceForm,
    ExclusionDemissionForm, PerformanceForm, ObjectifMembreForm,
    DocumentRHForm, HistoriqueDocumentForm, CustomUserUpdateForm
)
from .views import is_admin

# Helper functions
def is_responsable(user):
    return hasattr(user, 'profil_responsable')

# Member Contact Information views
@login_required
def profil_view(request):
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès.')
            return redirect('profil')
    else:
        form = CustomUserUpdateForm(instance=request.user)
    
    return render(request, 'profil.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def member_list_view(request):
    membres = CustomUser.objects.all()
    return render(request, 'member_list.html', {'membres': membres})

@login_required
@user_passes_test(is_admin)
def member_detail_view(request, user_id):
    membre = get_object_or_404(CustomUser, id=user_id)
    absences = Absence.objects.filter(membre=membre)
    formations = Formation.objects.filter(membre=membre)
    performances = Performance.objects.filter(membre=membre)
    competences = Competence.objects.filter(membre=membre)
    exclusions = ExclusionDemission.objects.filter(membre=membre)
    objectifs = ObjectifMembre.objects.filter(membre=membre)
    
    return render(request, 'member_detail.html', {
        'membre': membre,
        'absences': absences,
        'formations': formations,
        'performances': performances,
        'competences': competences,
        'exclusions': exclusions,
        'objectifs': objectifs
    })

# Absence Management views
@login_required
def absence_list_view(request):
    if is_admin(request.user):
        absences = Absence.objects.all().order_by('-date_debut')
    else:
        absences = Absence.objects.filter(membre=request.user).order_by('-date_debut')
    
    return render(request, 'absence/list.html', {'absences': absences})

@login_required
def absence_create_view(request):
    if request.method == 'POST':
        form = AbsenceForm(request.POST)
        if form.is_valid():
            absence = form.save(commit=False)
            absence.membre = request.user
            absence.save()
            messages.success(request, 'Votre absence a été enregistrée avec succès.')
            return redirect('absence_list')
    else:
        form = AbsenceForm()
    
    return render(request, 'absence/create.html', {'form': form})

@login_required
def absence_detail_view(request, absence_id):
    absence = get_object_or_404(Absence, id=absence_id)
    
    # Verify user is admin or the absence owner
    if not is_admin(request.user) and absence.membre != request.user:
        messages.error(request, 'Vous n\'êtes pas autorisé à accéder à cette page.')
        return redirect('absence_list')
    
    notifications = NotificationRetour.objects.filter(absence=absence)
    
    return render(request, 'absence/detail.html', {
        'absence': absence,
        'notifications': notifications
    })

@login_required
@user_passes_test(is_admin)
def absence_notification_view(request, absence_id):
    absence = get_object_or_404(Absence, id=absence_id)
    
    if request.method == 'POST':
        form = NotificationRetourForm(request.POST)
        if form.is_valid():
            notification = form.save(commit=False)
            notification.absence = absence
            notification.envoye_par = request.user
            notification.save()
            
            # Update absence notification status
            absence.notif_retour = True
            absence.date_notification = timezone.now()
            absence.save()
            
            messages.success(request, 'Notification de retour envoyée avec succès.')
            return redirect('absence_detail', absence_id=absence.id)
    else:
        form = NotificationRetourForm()
    
    return render(request, 'absence/notification.html', {
        'form': form,
        'absence': absence
    })

@login_required
@user_passes_test(is_admin)
def absence_verify_return_view(request, absence_id):
    absence = get_object_or_404(Absence, id=absence_id)
    
    absence.retour_verifie = True
    absence.save()
    
    messages.success(request, 'Le retour a été vérifié avec succès.')
    return redirect('absence_detail', absence_id=absence.id)

# Training and Skills Management views
@login_required
def formation_list_view(request):
    if is_admin(request.user):
        formations = Formation.objects.all().order_by('-date_debut')
    else:
        formations = Formation.objects.filter(membre=request.user).order_by('-date_debut')
    
    return render(request, 'formation/list.html', {'formations': formations})

@login_required
def formation_create_view(request):
    if request.method == 'POST':
        form = FormationForm(request.POST, request.FILES)
        if form.is_valid():
            formation = form.save(commit=False)
            formation.membre = request.user
            formation.save()
            messages.success(request, 'La formation a été enregistrée avec succès.')
            return redirect('formation_list')
    else:
        form = FormationForm()
    
    return render(request, 'formation/create.html', {'form': form})

@login_required
def formation_detail_view(request, formation_id):
    formation = get_object_or_404(Formation, id=formation_id)
    
    # Verify user is admin or the formation owner
    if not is_admin(request.user) and formation.membre != request.user:
        messages.error(request, 'Vous n\'êtes pas autorisé à accéder à cette page.')
        return redirect('formation_list')
    
    competences = Competence.objects.filter(formation=formation)
    
    return render(request, 'formation/detail.html', {
        'formation': formation,
        'competences': competences
    })

@login_required
def competence_create_view(request, formation_id):
    formation = get_object_or_404(Formation, id=formation_id)
    
    # Verify user is admin or the formation owner
    if not is_admin(request.user) and formation.membre != request.user:
        messages.error(request, 'Vous n\'êtes pas autorisé à accéder à cette page.')
        return redirect('formation_list')
    
    if request.method == 'POST':
        form = CompetenceForm(request.POST)
        if form.is_valid():
            competence = form.save(commit=False)
            competence.formation = formation
            competence.membre = formation.membre
            competence.save()
            messages.success(request, 'La compétence a été ajoutée avec succès.')
            return redirect('formation_detail', formation_id=formation.id)
    else:
        form = CompetenceForm()
    
    return render(request, 'competence/create.html', {
        'form': form,
        'formation': formation
    })

@login_required
def competence_list_view(request):
    if is_admin(request.user):
        competences = Competence.objects.all()
    else:
        competences = Competence.objects.filter(membre=request.user)
    
    return render(request, 'competence/list.html', {'competences': competences})

# Exclusion and Resignation Management views
@login_required
@user_passes_test(is_admin)
def exclusion_list_view(request):
    exclusions = ExclusionDemission.objects.all().order_by('-date_effet')
    return render(request, 'exclusion/list.html', {'exclusions': exclusions})

@login_required
@user_passes_test(is_admin)
def exclusion_create_view(request, user_id):
    membre = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        form = ExclusionDemissionForm(request.POST, request.FILES)
        if form.is_valid():
            exclusion = form.save(commit=False)
            exclusion.membre = membre
            exclusion.traite_par = request.user
            exclusion.save()
            messages.success(request, f'{exclusion.get_type_display()} enregistrée avec succès.')
            return redirect('exclusion_list')
    else:
        form = ExclusionDemissionForm()
    
    return render(request, 'exclusion/create.html', {
        'form': form,
        'membre': membre
    })

@login_required
@user_passes_test(is_admin)
def exclusion_detail_view(request, exclusion_id):
    exclusion = get_object_or_404(ExclusionDemission, id=exclusion_id)
    return render(request, 'exclusion/detail.html', {'exclusion': exclusion})

# Performance Management views
@login_required
def performance_list_view(request):
    if is_admin(request.user) or is_responsable(request.user):
        performances = Performance.objects.all().order_by('-date_evaluation')
    else:
        performances = Performance.objects.filter(membre=request.user).order_by('-date_evaluation')
    
    return render(request, 'performance/list.html', {'performances': performances})

@login_required
@user_passes_test(lambda u: is_admin(u) or is_responsable(u))
def performance_create_view(request, user_id):
    membre = get_object_or_404(CustomUser, id=user_id)
    responsable = get_object_or_404(Responsable, utilisateur=request.user) if is_responsable(request.user) else None
    
    if request.method == 'POST':
        form = PerformanceForm(request.POST)
        if form.is_valid():
            performance = form.save(commit=False)
            performance.membre = membre
            performance.responsable = responsable
            performance.date_evaluation = timezone.now().date()
            performance.save()
            messages.success(request, 'L\'évaluation a été enregistrée avec succès.')
            return redirect('performance_list')
    else:
        form = PerformanceForm()
    
    return render(request, 'performance/create.html', {
        'form': form,
        'membre': membre
    })

@login_required
def performance_detail_view(request, performance_id):
    performance = get_object_or_404(Performance, id=performance_id)
    
    # Verify user is admin, responsable or the performance owner
    if not (is_admin(request.user) or is_responsable(request.user)) and performance.membre != request.user:
        messages.error(request, 'Vous n\'êtes pas autorisé à accéder à cette page.')
        return redirect('performance_list')
    
    objectifs = ObjectifMembre.objects.filter(membre=performance.membre)
    
    return render(request, 'performance/detail.html', {
        'performance': performance,
        'objectifs': objectifs
    })

@login_required
@user_passes_test(lambda u: is_admin(u) or is_responsable(u))
def objectif_create_view(request, user_id):
    membre = get_object_or_404(CustomUser, id=user_id)
    responsable = get_object_or_404(Responsable, utilisateur=request.user) if is_responsable(request.user) else None
    
    if request.method == 'POST':
        form = ObjectifMembreForm(request.POST)
        if form.is_valid():
            objectif = form.save(commit=False)
            objectif.membre = membre
            objectif.responsable_suivi = responsable
            objectif.save()
            messages.success(request, 'L\'objectif a été créé avec succès.')
            return redirect('member_detail', user_id=membre.id)
    else:
        form = ObjectifMembreForm()
    
    return render(request, 'objectif/create.html', {
        'form': form,
        'membre': membre
    })

@login_required
def objectif_detail_view(request, objectif_id):
    objectif = get_object_or_404(ObjectifMembre, id=objectif_id)
    
    # Verify user is admin, responsable or the objectif owner
    if not (is_admin(request.user) or is_responsable(request.user)) and objectif.membre != request.user:
        messages.error(request, 'Vous n\'êtes pas autorisé à accéder à cette page.')
        return redirect('dashboard')
    
    return render(request, 'objectif/detail.html', {'objectif': objectif})

@login_required
@user_passes_test(lambda u: is_admin(u) or is_responsable(u))
def objectif_update_status_view(request, objectif_id):
    objectif = get_object_or_404(ObjectifMembre, id=objectif_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in [choice[0] for choice in ObjectifMembre.STATUS_CHOICES]:
            objectif.status = new_status
            objectif.save()
            messages.success(request, 'Le statut de l\'objectif a été mis à jour avec succès.')
        else:
            messages.error(request, 'Statut invalide.')
    
    return redirect('objectif_detail', objectif_id=objectif.id)

# HR Document Management views
@login_required
@user_passes_test(is_admin)
def document_list_view(request):
    documents = DocumentRH.objects.all().order_by('-dernier_modif')
    return render(request, 'document/list.html', {'documents': documents})

@login_required
def document_accessible_list_view(request):
    # Get documents accessible to the user's groups
    user_groups = request.user.groups.all()
    documents = DocumentRH.objects.filter(accessible_a__in=user_groups).distinct()
    
    return render(request, 'document/accessible_list.html', {'documents': documents})

@login_required
@user_passes_test(is_admin)
def document_create_view(request):
    if request.method == 'POST':
        form = DocumentRHForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.cree_par = request.user
            document.modifie_par = request.user
            document.save()
            
            # Save many-to-many relationships
            form.save_m2m()
            
            # Create first version in history
            HistoriqueDocument.objects.create(
                document=document,
                version=document.version,
                modifie_par=request.user,
                description_changements="Création initiale du document"
            )
            
            messages.success(request, 'Le document a été créé avec succès.')
            return redirect('document_list')
    else:
        form = DocumentRHForm()
    
    return render(request, 'document/create.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def document_update_view(request, document_id):
    document = get_object_or_404(DocumentRH, id=document_id)
    
    if request.method == 'POST':
        form = DocumentRHForm(request.POST, request.FILES, instance=document)
        history_form = HistoriqueDocumentForm(request.POST)
        
        if form.is_valid() and history_form.is_valid():
            # Update document
            updated_document = form.save(commit=False)
            updated_document.modifie_par = request.user
            updated_document.save()
            form.save_m2m()
            
            # Add history entry
            history = history_form.save(commit=False)
            history.document = document
            history.modifie_par = request.user
            history.save()
            
            messages.success(request, 'Le document a été mis à jour avec succès.')
            return redirect('document_detail', document_id=document.id)
    else:
        form = DocumentRHForm(instance=document)
        history_form = HistoriqueDocumentForm(initial={'version': f"{float(document.version) + 0.1:.1f}"})
    
    return render(request, 'document/update.html', {
        'form': form,
        'history_form': history_form,
        'document': document
    })

@login_required
def document_detail_view(request, document_id):
    document = get_object_or_404(DocumentRH, id=document_id)
    
    # Check if user has access to the document
    user_groups = request.user.groups.all()
    if not is_admin(request.user) and not document.accessible_a.filter(id__in=user_groups.values_list('id', flat=True)).exists():
        messages.error(request, 'Vous n\'êtes pas autorisé à accéder à ce document.')
        return redirect('document_accessible_list')
    
    historique = HistoriqueDocument.objects.filter(document=document).order_by('-date_modification')
    
    return render(request, 'document/detail.html', {
        'document': document,
        'historique': historique
    })

@login_required
def document_download_view(request, document_id):
    document = get_object_or_404(DocumentRH, id=document_id)
    
    # Check if user has access to the document
    user_groups = request.user.groups.all()
    if not is_admin(request.user) and not document.accessible_a.filter(id__in=user_groups.values_list('id', flat=True)).exists():
        messages.error(request, 'Vous n\'êtes pas autorisé à télécharger ce document.')
        return redirect('document_accessible_list')
    
    # Serve the file
    response = HttpResponse(document.fichier, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename="{document.fichier.name.split("/")[-1]}"'
    return response
