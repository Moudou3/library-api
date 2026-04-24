from sqlalchemy.orm import Session
from app.models.book import Book
from app.models.category import Category
from app.repositories.book_repository import BookRepository
from app.schemas.book import BookCreate, BookUpdate
from app.exceptions import NotFoundException, ConflictException


class BookService:
    def __init__(self, db: Session):
        self.repository = BookRepository(db)
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Book]:
        return self.repository.get_all(skip, limit)

    def get_by_id(self, book_id: int) -> Book:
        book = self.repository.get_by_id(book_id)
        if not book:
            raise NotFoundException(f"Book with id {book_id} not found")
        return book

    def search(self, title: str) -> list[Book]:
        return self.repository.search_by_title(title)

    def create(self, data: BookCreate) -> Book:
        existing = self.repository.get_by_isbn(data.isbn)
        if existing:
            raise ConflictException(f"Book with ISBN {data.isbn} already exists")

        book = Book(
            isbn=data.isbn,
            title=data.title,
            publication_year=data.publication_year,
            quantity=data.quantity,
            author_id=data.author_id
        )
        return self.repository.create(book, data.category_ids)

    def update(self, book_id: int, data: BookUpdate) -> Book:
        book = self.get_by_id(book_id)

        if data.title is not None:
            book.title = data.title
        if data.publication_year is not None:
            book.publication_year = data.publication_year
        if data.quantity is not None:
            book.quantity = data.quantity
        if data.category_ids is not None:
            categories = self.db.query(Category).filter(
                Category.id.in_(data.category_ids)
            ).all()
            book.categories = categories

        return self.repository.update(book)

    def delete(self, book_id: int) -> None:
        book = self.get_by_id(book_id)
        self.repository.delete(book)
