from django.urls import path
from .views import custom_login_view, signup_view, dashboard_view, test_filters_view
from django.contrib.auth.views import LogoutView
from . import views_rh

urlpatterns = [
    # Authentication and Main Views
    path('signup/', signup_view, name='signup'),
    path('login/', custom_login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', dashboard_view, name='dashboard'),
    path('test-filters/', test_filters_view, name='test_filters'),
    
    # User Profile Management
    path('profil/', views_rh.profil_view, name='profil'),
    path('membres/', views_rh.member_list_view, name='member_list'),
    path('membres/<int:user_id>/', views_rh.member_detail_view, name='member_detail'),
    
    # Absence Management
    path('absences/', views_rh.absence_list_view, name='absence_list'),
    path('absences/creer/', views_rh.absence_create_view, name='absence_create'),
    path('absences/<int:absence_id>/', views_rh.absence_detail_view, name='absence_detail'),
    path('absences/<int:absence_id>/notifier/', views_rh.absence_notification_view, name='absence_notification'),
    path('absences/<int:absence_id>/verifier-retour/', views_rh.absence_verify_return_view, name='absence_verify_return'),
    
    # Training and Skills Management
    path('formations/', views_rh.formation_list_view, name='formation_list'),
    path('formations/creer/', views_rh.formation_create_view, name='formation_create'),
    path('formations/<int:formation_id>/', views_rh.formation_detail_view, name='formation_detail'),
    path('formations/<int:formation_id>/competence/ajouter/', views_rh.competence_create_view, name='competence_create'),
    path('competences/', views_rh.competence_list_view, name='competence_list'),
    
    # Exclusion and Resignation Management
    path('exclusions/', views_rh.exclusion_list_view, name='exclusion_list'),
    path('exclusions/creer/<int:user_id>/', views_rh.exclusion_create_view, name='exclusion_create'),
    path('exclusions/<int:exclusion_id>/', views_rh.exclusion_detail_view, name='exclusion_detail'),
    
    # Performance Management
    path('performances/', views_rh.performance_list_view, name='performance_list'),
    path('performances/creer/<int:user_id>/', views_rh.performance_create_view, name='performance_create'),
    path('performances/<int:performance_id>/', views_rh.performance_detail_view, name='performance_detail'),
    path('objectifs/creer/<int:user_id>/', views_rh.objectif_create_view, name='objectif_create'),
    path('objectifs/<int:objectif_id>/', views_rh.objectif_detail_view, name='objectif_detail'),
    path('objectifs/<int:objectif_id>/statut/', views_rh.objectif_update_status_view, name='objectif_update_status'),
    
    # HR Document Management
    path('documents/', views_rh.document_list_view, name='document_list'),
    path('documents/accessibles/', views_rh.document_accessible_list_view, name='document_accessible_list'),
    path('documents/creer/', views_rh.document_create_view, name='document_create'),
    path('documents/<int:document_id>/', views_rh.document_detail_view, name='document_detail'),    path('documents/<int:document_id>/modifier/', views_rh.document_update_view, name='document_update'),
    path('documents/<int:document_id>/telecharger/', views_rh.document_download_view, name='document_download'),
]
