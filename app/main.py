from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.database import engine, Base
from app.routers import books, authors, categories, users, loans
from app.exceptions import NotFoundException, ConflictException, BadRequestException
from app.exceptions.handlers import (
    not_found_handler,
    conflict_handler,
    bad_request_handler
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Création des tables au démarrage
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Library API",
    description="API RESTful de gestion de bibliothèque",
    version="1.0.0",
    lifespan=lifespan
)

# Enregistrer les handlers d'exceptions
app.add_exception_handler(NotFoundException, not_found_handler)
app.add_exception_handler(ConflictException, conflict_handler)
app.add_exception_handler(BadRequestException, bad_request_handler)

# Enregistrer les routers
app.include_router(books.router)
app.include_router(authors.router)
app.include_router(categories.router)
app.include_router(users.router)
app.include_router(loans.router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "healthy", "service": "Library API"}


@app.get("/api", tags=["Health"])
def api_info():
    return {
        "name": "Library API",
        "version": "1.0.0",
        "endpoints": [
            "/api/books",
            "/api/authors",
            "/api/categories",
            "/api/users",
            "/api/loans"
        ]
    }
