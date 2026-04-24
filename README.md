# Library API 📚

API RESTful de gestion de bibliothèque développée avec FastAPI, SQLAlchemy et MySQL.

## Fonctionnalités

- **Gestion des livres** : CRUD complet, recherche par titre
- **Gestion des auteurs** : CRUD, consultation des livres par auteur
- **Gestion des catégories** : Classification des livres
- **Gestion des utilisateurs** : Inscription avec carte de bibliothèque automatique
- **Système d'emprunts** : Création, retour, historique

## Relations implémentées

| Type | Entités |
|------|---------|
| One-to-One | User ↔ LibraryCard |
| One-to-Many | Author → Book |
| Many-to-Many | Book ↔ Category |

## Prérequis

- Docker et Docker Compose

## Lancement

```bash
# Cloner le dépôt
git clone [github.com](https://github.com/votre-compte/library-api.git)
cd library-api

# Lancer l'application
docker compose up --build

# L'API est disponible sur [localhost](http://localhost:8000)
# Documentation Swagger : [localhost](http://localhost:8000/docs)
# Documentation ReDoc : [localhost](http://localhost:8000/redoc)
