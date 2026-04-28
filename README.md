# 📘 Library API — FastAPI + MySQL + Docker

## 🚀 Description du projet

Library API est une application backend développée avec **FastAPI**, **SQLAlchemy** et **MySQL**, permettant la gestion complète d’un système de bibliothèque.

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
  - One-to-One (User ↔ LibraryCard)
  - One-to-Many (Author → Book)
  - Many-to-Many (Book ↔ Category)
Diagram --> dans Diagram.png

- API REST complète
- Validation avec Pydantic
- Conteneurisation avec Docker & Docker Compose
- Base de données MySQL

---

## Architecture 

app/
├── main.py            # Point d’entrée FastAPI
├── models/            # Modèles SQLAlchemy
├── schemas/           # DTOs Pydantic
├── repositories/      # Accès aux données
├── services/          # Logique métier
├── routers/           # Endpoints API
├── exceptions/        # Gestion des erreurs

## 🐳 Lancer le projet avec Docker

# 1️⃣ Cloner le projet

### bash
git clone https://github.com/Moudou3/library-api.git
cd library-api

# 2️⃣ Lancer les services
docker compose up --build

# 3️⃣ Accéder à l’application
Dans le terminal uvicorn app.main:app --reload

Swagger UI : http://localhost:8000/docs

# 4️⃣ Arrêter le projet
docker compose down

