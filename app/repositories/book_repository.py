from sqlalchemy.orm import Session, joinedload
from app.models.book import Book
from app.models.category import Category


class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Book]:
        return (
            self.db.query(Book)
            .options(joinedload(Book.author), joinedload(Book.categories))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id(self, book_id: int) -> Book | None:
        return (
            self.db.query(Book)
            .options(joinedload(Book.author), joinedload(Book.categories))
            .filter(Book.id == book_id)
            .first()
        )

    def get_by_isbn(self, isbn: str) -> Book | None:
        return self.db.query(Book).filter(Book.isbn == isbn).first()

    def get_by_author(self, author_id: int) -> list[Book]:
        return self.db.query(Book).filter(Book.author_id == author_id).all()

    def search_by_title(self, title: str) -> list[Book]:
        return (
            self.db.query(Book)
            .options(joinedload(Book.author))
            .filter(Book.title.ilike(f"%{title}%"))
            .all()
        )

    def create(self, book: Book, category_ids: list[int]) -> Book:
        if category_ids:
            categories = self.db.query(Category).filter(Category.id.in_(category_ids)).all()
            book.categories = categories
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book

    def update(self, book: Book) -> Book:
        self.db.commit()
        self.db.refresh(book)
        return book

    def delete(self, book: Book) -> None:
        self.db.delete(book)
        self.db.commit()
