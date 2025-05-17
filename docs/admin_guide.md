# Guide d'Administration du Système de Gestion RH

## Introduction

Ce guide est destiné aux administrateurs du Système de Gestion des Ressources Humaines de Junior Entreprise Sesame. Il couvre les aspects techniques et la gestion avancée du système.

## Configuration Initiale

### Installation
```bash
# Cloner le dépôt
git clone https://github.com/ErrayDineri/ERPJuniorSesameProject
cd ERPJuniorSesameProject

# Installer les dépendances
pip install -r requirements.txt

# Initialiser la base de données
python manage.py makemigrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser
```

### Données de Test
Pour charger des données de test afin de faciliter la démonstration ou le développement:
```bash
python manage.py create_sample_data
```

## Structure du Projet

### Modèles Principaux
- `CustomUser`: Utilisateurs avec informations de contact étendues
- `Absence`: Gestion des absences des membres
- `Formation`: Suivi des formations suivies
- `Competence`: Compétences acquises par les membres
- `Responsable`: Profil des responsables RH
- `Performance`: Évaluations de performance
- `DocumentRH`: Gestion documentaire RH
- `ExclusionDemission`: Gestion des exclusions et démissions

### Vues et Templates
- `views.py`: Vues générales du système
- `views_rh.py`: Vues spécifiques au module RH
- Templates organisés par fonctionnalité dans le dossier `/templates`

## Gestion des Utilisateurs

### Groupes et Permissions
Le système utilise trois groupes principaux:
1. **Administrateurs**: Accès complet à toutes les fonctionnalités
2. **RH**: Gestion des ressources humaines, accès aux fonctions d'administration
3. **Membres**: Utilisateurs standard avec accès limité

Pour ajouter un utilisateur à un groupe:
1. Accédez à l'interface d'administration Django: `/admin/`
2. Naviguez vers "Utilisateurs"
3. Sélectionnez l'utilisateur à modifier
4. Dans la section "Groupes", ajoutez l'utilisateur au groupe approprié

### Désactivation de Compte
Pour désactiver un compte sans le supprimer:
1. Dans l'interface d'administration
2. Décochez la case "Actif" dans le profil de l'utilisateur
3. Sauvegardez les modifications

## Sauvegarde et Restauration

### Sauvegarde de la Base de Données
```bash
# Sauvegarde de la base de données SQLite
python manage.py dumpdata > backup_$(date +%Y%m%d).json

# Pour une sauvegarde par application
python manage.py dumpdata main > main_backup_$(date +%Y%m%d).json
```

### Restauration de la Base de Données
```bash
# Restauration complète
python manage.py loaddata backup_YYYYMMDD.json

# Restauration d'une application spécifique
python manage.py loaddata main_backup_YYYYMMDD.json
```

## Personnalisation du Système

### Ajout de Nouveaux Champs
1. Modifiez le modèle approprié dans `models.py`
2. Créez et appliquez les migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
3. Mettez à jour les formulaires dans `forms.py`
4. Modifiez les templates pour afficher les nouveaux champs

### Configuration des Emails
Pour configurer l'envoi d'emails:
1. Modifiez `settings.py`:
   ```python
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = 'smtp.example.com'
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = 'votre_email@example.com'
   EMAIL_HOST_PASSWORD = 'votre_mot_de_passe'
   ```

## Dépannage

### Problèmes de Migration
```bash
# Réinitialiser les migrations (développement uniquement)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
```

### Journal d'Erreurs
Activez la journalisation détaillée dans `settings.py`:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

## Mise à Jour du Système

Pour mettre à jour le système vers une nouvelle version:
```bash
# Mettre à jour depuis le dépôt Git
git pull

# Mettre à jour les dépendances
pip install -r requirements.txt --upgrade

# Appliquer les migrations
python manage.py migrate
```

## Support et Contact

En cas de problèmes techniques majeurs:
- Consultez la documentation technique Django: https://docs.djangoproject.com/
- Contactez le développeur principal: dev@sesame.com.tn
