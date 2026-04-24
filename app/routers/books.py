from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.book_service import BookService
from app.schemas.book import BookCreate, BookUpdate, BookResponse

router = APIRouter(prefix="/api/books", tags=["Books"])


@router.get("", response_model=list[BookResponse])
def get_all_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    service = BookService(db)
    return service.get_all(skip, limit)


@router.get("/search", response_model=list[BookResponse])
def search_books(
    title: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    service = BookService(db)
    return service.search(title)


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    service = BookService(db)
    return service.get_by_id(book_id)


@router.post("", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(data: BookCreate, db: Session = Depends(get_db)):
    service = BookService(db)
    return service.create(data)


@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, data: BookUpdate, db: Session = Depends(get_db)):
    service = BookService(db)
    return service.update(book_id, data)


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    service = BookService(db)
    service.delete(book_id)
