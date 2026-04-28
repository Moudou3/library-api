"""
Script de seed — remplit la base de données avec des données de test.
À placer dans scripts/seed.py et lancer depuis la racine du projet :

    python scripts/seed.py
"""

import sys
import os
from datetime import date

# Permet d'importer les modules app/ depuis la racine du projet
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.database import SessionLocal, engine, Base
from app.models.author import Author
from app.models.category import Category
from app.models.book import Book
from app.models.user import User
from app.models.library_card import LibraryCard
from app.models.loan import Loan, LoanStatus

# Nécessaire pour que Base.metadata connaisse toutes les tables
import app.models.author
import app.models.category
import app.models.book
import app.models.user
import app.models.library_card
import app.models.loan


def seed():
    # Crée les tables si elles n'existent pas encore
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Vérifie si la base est déjà remplie pour éviter les doublons
        if db.query(Author).first():
            print("⚠️  La base contient déjà des données. Seed ignoré.")
            return

        print("🌱 Insertion des données de test...")

        # ── Auteurs ────────────────────────────────────────────────────────────
        victor_hugo = Author(
            name="Victor Hugo",
            biography="Écrivain français du XIXe siècle, auteur des Misérables."
        )
        albert_camus = Author(
            name="Albert Camus",
            biography="Écrivain et philosophe français, prix Nobel de littérature 1957."
        )
        simone_beauvoir = Author(
            name="Simone de Beauvoir",
            biography="Philosophe et romancière française, figure du féminisme."
        )
        db.add_all([victor_hugo, albert_camus, simone_beauvoir])
        db.flush()  # récupère les IDs sans commit
        print("  ✓ Auteurs ajoutés")

        # ── Catégories ─────────────────────────────────────────────────────────
        cat_roman     = Category(name="Roman",       description="Œuvres de fiction narratives")
        cat_philo     = Category(name="Philosophie", description="Ouvrages philosophiques")
        cat_classique = Category(name="Classique",   description="Grands classiques de la littérature")
        cat_essai     = Category(name="Essai",       description="Essais et réflexions")
        db.add_all([cat_roman, cat_philo, cat_classique, cat_essai])
        db.flush()
        print("  ✓ Catégories ajoutées")

        # ── Livres (Many-to-Many avec catégories) ──────────────────────────────
        les_miserables = Book(
            isbn="9782070409228",
            title="Les Misérables",
            publication_year=1862,
            quantity=3,
            author=victor_hugo,
            categories=[cat_roman, cat_classique]
        )
        l_etranger = Book(
            isbn="9782070360024",
            title="L'Étranger",
            publication_year=1942,
            quantity=2,
            author=albert_camus,
            categories=[cat_roman, cat_classique]
        )
        deuxieme_sexe = Book(
            isbn="9782070368792",
            title="Le Deuxième Sexe",
            publication_year=1949,
            quantity=2,
            author=simone_beauvoir,
            categories=[cat_philo, cat_essai]
        )
        notre_dame = Book(
            isbn="9782070411580",
            title="Notre-Dame de Paris",
            publication_year=1831,
            quantity=1,
            author=victor_hugo,
            categories=[cat_roman, cat_classique]
        )
        la_peste = Book(
            isbn="9782070360192",
            title="La Peste",
            publication_year=1947,
            quantity=2,
            author=albert_camus,
            categories=[cat_roman, cat_classique]
        )
        db.add_all([les_miserables, l_etranger, deuxieme_sexe, notre_dame, la_peste])
        db.flush()
        print("  ✓ Livres ajoutés")

        # ── Utilisateurs ───────────────────────────────────────────────────────
        jean = User(
            email="jean.dupont@email.com",
            password_hash="hashed_password_1",
            first_name="Jean",
            last_name="Dupont"
        )
        marie = User(
            email="marie.martin@email.com",
            password_hash="hashed_password_2",
            first_name="Marie",
            last_name="Martin"
        )
        db.add_all([jean, marie])
        db.flush()
        print("  ✓ Utilisateurs ajoutés")

        # ── Cartes de bibliothèque (One-to-One avec User) ──────────────────────
        card_jean = LibraryCard(
            card_number="LIB-ABC12345",
            issue_date=date(2024, 1, 15),
            expiry_date=date(2025, 1, 15),
            user=jean
        )
        card_marie = LibraryCard(
            card_number="LIB-DEF67890",
            issue_date=date(2024, 3, 20),
            expiry_date=date(2025, 3, 20),
            user=marie
        )
        db.add_all([card_jean, card_marie])
        db.flush()
        print("  ✓ Cartes de bibliothèque ajoutées")

        # ── Emprunts (One-to-Many avec User et Book) ───────────────────────────
        loan1 = Loan(
            loan_date=date(2024, 11, 1),
            due_date=date(2024, 11, 15),
            return_date=date(2024, 11, 13),
            status=LoanStatus.RETURNED,
            user=jean,
            book=les_miserables
        )
        loan2 = Loan(
            loan_date=date(2024, 12, 1),
            due_date=date(2024, 12, 15),
            return_date=None,
            status=LoanStatus.ACTIVE,
            user=marie,
            book=l_etranger
        )
        db.add_all([loan1, loan2])

        db.commit()
        print("\n✅ Seed terminé avec succès !")
        print(f"   - {db.query(Author).count()} auteurs")
        print(f"   - {db.query(Category).count()} catégories")
        print(f"   - {db.query(Book).count()} livres")
        print(f"   - {db.query(User).count()} utilisateurs")
        print(f"   - {db.query(LibraryCard).count()} cartes")
        print(f"   - {db.query(Loan).count()} emprunts")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Erreur lors du seed : {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()