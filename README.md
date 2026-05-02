# 📘 Library API — FastAPI + MySQL + Docker

## 🚀 Description du projet

Library API est une application backend développée avec **FastAPI**, **SQLAlchemy** et **MySQL**, permettant la gestion complète d'un système de bibliothèque.

Elle permet de gérer :

- 📚 Livres
- ✍️ Auteurs
- 🏷️ Catégories
- 👤 Utilisateurs
- 📖 Emprunts

---

## 🧠 Objectifs techniques

Ce projet met en œuvre des concepts avancés de développement backend :

- Architecture en couches :
  - Routers (API)
  - Services (logique métier)
  - Repositories (accès aux données)

- Relations de base de données :
  - One-to-One (User ↔️ LibraryCard)
  - One-to-Many (Author → Book)
  - Many-to-Many (Book ↔️ Category)

Diagram → dans `diagram.png`

- API REST complète
- Validation avec Pydantic
- Conteneurisation avec Docker & Docker Compose
- Base de données MySQL

---

## 🗂️ Architecture

```
app/
├── main.py            # Point d'entrée FastAPI
├── models/            # Modèles SQLAlchemy
├── schemas/           # DTOs Pydantic
├── repositories/      # Accès aux données
├── services/          # Logique métier
├── routers/           # Endpoints API
├── exceptions/        # Gestion des erreurs
scripts/
├── init_data.sql      # Données de test initiales (chargées automatiquement)
├── seed.py            # Script de seed alternatif
tests/
├── test_books.py
├── test_users.py
├── test_loans.py
```

---

## 🐳 Lancer le projet avec Docker

### 1️⃣ Cloner le projet
--> bash
git clone https://github.com/Moudou3/library-api.git
cd library-api

### 2️⃣ Lancer les services
--> bash
docker compose up --build


### 3️⃣ Accéder à l'application
- Swagger UI : http://localhost:8000/docs

### 4️⃣ Arrêter le projet
--> bash
docker compose down


### 5️⃣ Reset complet de la base de données
--> bash
docker compose down -v
docker compose up --build


> ℹ️ Les données de test sont chargées automatiquement au premier démarrage via `scripts/init_data.sql`

> ⚠️ Supprimer le `-v` si vous ne voulez pas perdre vos données existantes

## 🗄️ Vérifier la base de données

--> bash
docker exec -it library-db mysql -u library_user -p

Mot de passe : `library_pass`

-->sql
USE librarydb;
SELECT * FROM authors;
SELECT * FROM books;
SELECT * FROM users;
SELECT * FROM loans;


## 📡 Routes de l'API

> ⚠️ Respecter l'ordre suivant pour les tests car chaque ressource dépend de la précédente.

### 1️⃣ Auteurs — `AUTHORS`

---
POST   /api/authors          Créer un auteur
GET    /api/authors          Récupérer tous les auteurs
GET    /api/authors/{id}     Récupérer un auteur spécifique
DELETE /api/authors/{id}     Supprimer un auteur
---

Exemple POST :
-->json
{
  "name": "Victor Hugo",
  "biography": "Écrivain français du XIXe siècle"
}

---

### 2️⃣ Catégories — `CATEGORIES`

---
POST   /api/categories        Créer une catégorie
GET    /api/categories        Récupérer toutes les catégories
GET    /api/categories/{id}   Récupérer une catégorie spécifique
DELETE /api/categories/{id}   Supprimer une catégorie
---


Exemple POST :
-->json
{
  "name": "Roman",
  "description": "Œuvres de fiction"
}


---

### 3️⃣ Livres — `BOOKS`

POST   /api/books        Créer un livre
GET    /api/books        Récupérer tous les livres
GET    /api/books/{id}   Récupérer un livre spécifique
DELETE /api/books/{id}   Supprimer un livre

Exemple POST :
-->json
{
  "isbn": "9782070409228",
  "title": "Les Misérables",
  "publication_year": 1862,
  "quantity": 3,
  "author_id": 1,
  "category_ids": [1]
}


### 4️⃣ Utilisateurs — `USERS`

---
POST   /api/users              Créer un utilisateur
GET    /api/users              Récupérer tous les utilisateurs
GET    /api/users/{id}         Récupérer un utilisateur spécifique
GET    /api/users/{id}/loans   Récupérer les emprunts d'un utilisateur
DELETE /api/users/{id}         Supprimer un utilisateur
--
Exemple POST :
-->json
{
  "email": "jean.dupont@email.com",
  "password": "1234",
  "first_name": "Jean",
  "last_name": "Dupont"
}

### 5️⃣ Emprunts — `LOANS`
---
POST /api/loans              Créer un emprunt
GET  /api/loans              Récupérer tous les emprunts
GET  /api/loans/{id}         Récupérer un emprunt spécifique
PUT  /api/loans/{id}/return  Retourner un livre


Exemple POST :
-->json
{
  "user_id": 1,
  "book_id": 1,
  "loan_date": "2024-01-20",
  "due_date": "2024-02-20"
}

## ✅ Lancer les tests automatisés

-->bash
pip install pytest httpx
pytest tests/

## 🐳 Image Docker Hub

L'image est disponible sur Docker Hub :
https://hub.docker.com/r/moudou/library-api-api

-->bash
docker pull moudou/library-api-api


> ⚠️ L'API nécessite MySQL. Utiliser Docker Compose pour lancer le projet complet.

> 📦 Un volume Docker `library_data` est utilisé pour la persistance des données MySQL.