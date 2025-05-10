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
   ├──urls.py (defines the website endpoints)
   ├──forms.py (defines requests' forms)
```

## 🔧 Features

* RH functionalities

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
python manage.py migrate //create db from models
python manage.py runserver
```