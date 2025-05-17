# Projet Junior Entreprise Sesame

## 📄 Key Files

```
ERPJuniorSesameProject
├──main/
   ├──templates
      ├──base.html (define the base html of the website: navbar, footer)
      ├──*.html
   ├──models.py (defines the tables)
   ├──views.py (implements the website logic)
   ├──views_rh.py (implements the HR module logic)
   ├──urls.py (defines the website endpoints)
   ├──forms.py (defines requests' forms)
```

## 🔧 Features

### Système de Gestion des Ressources Humaines

#### Gestion des Membres
* Informations de contact (email, téléphone, adresse postale)
* Profils utilisateurs complets
* Affichage détaillé des membres
* Recherche et filtrage des membres

#### Gestion des Absences
* Suivi complet des absences (maladie, congés, etc.)
* Système de notification de retour
* Vérification des retours
* Support pour documents médicaux

#### Gestion des Exclusions et Démissions
* Suivi des procédures d'exclusion
* Gestion des démissions
* Documentation associée
* Processus de validation

#### Formations et Compétences
* Suivi des formations suivies
* Gestion des certifications
* Niveaux de compétence
* Catégorisation des compétences

#### Évaluations de Performance
* Système d'évaluation détaillé
* Feedback et commentaires
* Suivi des points forts et axes d'amélioration
* Objectifs et évaluations périodiques

#### Gestion Documentaire RH
* Stockage centralisé des documents RH
* Contrôle d'accès par groupe
* Historique des versions
* Catégorisation des documents

## 📦 Requirements

* Python 3.7+
* `django`

## Installation:

```bash
git clone https://github.com/ErrayDineri/ERPJuniorSesameProject
cd ERPJuniorSesameProject
pip install -r requirements.txt
```

## 🚀 Usage

```bash
python manage.py makemigrations
python manage.py migrate # create db from models
python manage.py runserver
```

## Utilisation du Système

### Création d'un compte administrateur
```bash
python manage.py createsuperuser
```

### Création de données de test
Pour tester rapidement les fonctionnalités avec des données d'exemple :
```bash
python manage.py create_sample_data
```

### Accès au système
- Interface d'administration: `http://localhost:8000/admin/`
- Interface utilisateur: `http://localhost:8000/`

### Comptes de test (après création des données test)
- Administrateur: admin@sesame.com.tn / password
- Responsable RH: responsable@sesame.com.tn / password123
- Membres: membre1@sesame.com.tn, membre2@sesame.com.tn / password123