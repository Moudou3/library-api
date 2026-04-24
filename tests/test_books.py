import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)


def test_create_author(client):
    response = client.post(
        "/api/authors",
        json={"name": "Test Author", "biography": "A test biography"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Author"
    assert "id" in data


def test_create_and_get_book(client):
    # Créer un auteur d'abord
    author_response = client.post(
        "/api/authors",
        json={"name": "Test Author"}
    )
    author_id = author_response.json()["id"]

    # Créer un livre
    book_response = client.post(
        "/api/books",
        json={
            "isbn": "9781234567890",
            "title": "Test Book",
            "publication_year": 2024,
            "quantity": 2,
            "author_id": author_id,
            "category_ids": []
        }
    )
    assert book_response.status_code == 201
    book_data = book_response.json()
    assert book_data["title"] == "Test Book"

    # Récupérer le livre
    get_response = client.get(f"/api/books/{book_data['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["isbn"] == "9781234567890"


def test_get_nonexistent_book(client):
    response = client.get("/api/books/999")
    assert response.status_code == 404
