from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from main.models import (
    CustomUser, Absence, Formation, Competence, 
    ExclusionDemission, Responsable, Performance, 
    DocumentRH, HistoriqueDocument, NotificationRetour, 
    ObjectifMembre
)
from django.utils import timezone
import datetime
import random

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')
        
        # Create user groups
        admin_group, _ = Group.objects.get_or_create(name='Administrateurs')
        member_group, _ = Group.objects.get_or_create(name='Membres')
        rh_group, _ = Group.objects.get_or_create(name='RH')
        
        # Create sample users
        users = []
        if not CustomUser.objects.filter(username='membre1').exists():
            user1 = CustomUser.objects.create_user(
                username='membre1',
                email='membre1@sesame.com.tn',
                password='password123',
                first_name='Ahmed',
                last_name='Ben Ali',
                telephone='70123456',
                adresse_postale='123 Rue Principale, Tunis',
                date_adhesion=timezone.now().date() - datetime.timedelta(days=365)
            )
            user1.groups.add(member_group)
            users.append(user1)
            
        if not CustomUser.objects.filter(username='membre2').exists():
            user2 = CustomUser.objects.create_user(
                username='membre2',
                email='membre2@sesame.com.tn',
                password='password123',
                first_name='Fatma',
                last_name='Jebali',
                telephone='70789012',
                adresse_postale='56 Avenue Habib Bourguiba, Sousse',
                date_adhesion=timezone.now().date() - datetime.timedelta(days=180)
            )
            user2.groups.add(member_group)
            users.append(user2)
            
        if not CustomUser.objects.filter(username='responsable').exists():
            resp_user = CustomUser.objects.create_user(
                username='responsable',
                email='responsable@sesame.com.tn',
                password='password123',
                first_name='Sami',
                last_name='Trabelsi',
                telephone='70456789',
                adresse_postale='78 Rue Ibn Khaldoun, Sfax',
                date_adhesion=timezone.now().date() - datetime.timedelta(days=730)
            )
            resp_user.groups.add(rh_group)
            resp_user.is_staff = True
            resp_user.save()
            users.append(resp_user)
            
            # Create responsable profile
            if not Responsable.objects.filter(utilisateur=resp_user).exists():
                Responsable.objects.create(
                    utilisateur=resp_user,
                    poste='Responsable RH',
                    departement='Ressources Humaines',
                    date_nomination=timezone.now().date() - datetime.timedelta(days=365)
                )
        
        # Create absences
        absences = []
        for user in users[:2]:  # Only for regular members
            for i in range(1, 4):
                start_date = timezone.now().date() - datetime.timedelta(days=random.randint(10, 100))
                end_date = start_date + datetime.timedelta(days=random.randint(1, 5))
                
                motifs = ['maladie', 'congé', 'formation', 'familial', 'autre']
                
                absence = Absence.objects.create(
                    membre=user,
                    date_debut=start_date,
                    date_fin=end_date,
                    motif=random.choice(motifs),
                    details_motif=f"Détails pour l'absence {i} de {user.username}",
                    certificat_medical=random.choice([True, False]),
                    notif_retour=random.choice([True, False]),
                    retour_verifie=random.choice([True, False])
                )
                absences.append(absence)
                
                # Create notification for some absences
                if absence.notif_retour:
                    NotificationRetour.objects.create(
                        absence=absence,
                        message=f"Notification de retour pour {user.first_name}",
                        envoye_par=CustomUser.objects.get(username='responsable')
                    )
        
        # Create formations
        formations = []
        for user in users[:2]:
            for i in range(1, 3):
                start_date = timezone.now().date() - datetime.timedelta(days=random.randint(30, 180))
                end_date = start_date + datetime.timedelta(days=random.randint(1, 5))
                
                niveaux = ['debutant', 'intermediaire', 'avance', 'expert']
                
                formation = Formation.objects.create(
                    membre=user,
                    intitule=f"Formation {i} pour {user.username}",
                    organisme=f"Organisme {i}",
                    date_debut=start_date,
                    date_fin=end_date,
                    certification=random.choice([True, False]),
                    niveau=random.choice(niveaux),
                    description=f"Description de la formation {i} pour {user.username}"
                )
                formations.append(formation)
                
        # Create competences
        for user in users[:2]:
            for i in range(1, 4):
                categories = ['technique', 'soft', 'management', 'langue', 'autre']
                
                formation = None
                if formations and random.choice([True, False]):
                    formation = random.choice(formations)
                
                Competence.objects.create(
                    formation=formation,
                    membre=user,
                    code=f"COMP{i}{user.id}",
                    libelle=f"Compétence {i} de {user.username}",
                    categorie=random.choice(categories),
                    niveau=random.randint(1, 5),
                    date_acquisition=timezone.now().date() - datetime.timedelta(days=random.randint(10, 365))
                )
        
        # Create performances
        responsable = Responsable.objects.first()
        for user in users[:2]:
            for i in range(1, 3):
                eval_date = timezone.now().date() - datetime.timedelta(days=random.randint(10, 180))
                suivi_date = eval_date + datetime.timedelta(days=90)
                
                Performance.objects.create(
                    membre=user,
                    responsable=responsable,
                    date_evaluation=eval_date,
                    note=random.choice([1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]),
                    commentaires=f"Commentaires pour l'évaluation {i} de {user.username}",
                    forces=f"Forces: bonne communication, travail d'équipe",
                    axes_amelioration=f"À améliorer: gestion du temps, priorisation",
                    objectifs=f"Objectifs pour les 3 prochains mois",
                    objectifs_atteints=random.choice([True, False]),
                    date_prochain_suivi=suivi_date
                )
                
        # Create objectives
        for user in users[:2]:
            for i in range(1, 3):
                statuts = ['non_commence', 'en_cours', 'termine', 'annule']
                
                ObjectifMembre.objects.create(
                    membre=user,
                    description=f"Objectif {i} pour {user.username}",
                    date_echeance=timezone.now().date() + datetime.timedelta(days=random.randint(30, 180)),
                    status=random.choice(statuts),
                    responsable_suivi=responsable,
                    commentaires=f"Commentaires sur l'objectif {i}"
                )
                
        # Create documents
        types_doc = ['politique', 'procedure', 'formulaire', 'contrat', 'autre']
        resp_user = CustomUser.objects.get(username='responsable')
        
        for i in range(1, 5):
            doc = DocumentRH.objects.create(
                titre=f"Document RH {i}",
                type=random.choice(types_doc),
                description=f"Description du document {i}",
                fichier=f"document{i}.pdf",  # Placeholder, no actual file
                version=f"1.{i}",
                cree_par=resp_user,
                modifie_par=resp_user
            )
            
            # Add groups that can access this document
            doc.accessible_a.add(admin_group)
            if random.choice([True, False]):
                doc.accessible_a.add(rh_group)
            if random.choice([True, False]) and i > 2:
                doc.accessible_a.add(member_group)
                
            # Create document history
            HistoriqueDocument.objects.create(
                document=doc,
                version=f"1.0",
                modifie_par=resp_user,
                description_changements="Version initiale"
            )
            
            if i == 1:
                HistoriqueDocument.objects.create(
                    document=doc,
                    version=f"1.1",
                    modifie_par=resp_user,
                    description_changements="Mise à jour mineure"
                )
                
        # Create an exclusion/démission
        if random.choice([True, False]) and len(users) > 2:
            ExclusionDemission.objects.create(
                membre=users[1],
                type=random.choice(['exclusion', 'demission']),
                date_effet=timezone.now().date() + datetime.timedelta(days=30),
                motif="Raisons personnelles",
                document_reference="REF-123456",
                notes_additionnelles="Notes additionnelles sur cette démission",
                traite_par=resp_user
            )
            
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
