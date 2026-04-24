from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base

# Table d'association pour Many-to-Many
book_category = Table(
    "book_category",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id"), primary_key=True)
)


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    isbn = Column(String(13), unique=True, nullable=False, index=True)
    title = Column(String(300), nullable=False, index=True)
    publication_year = Column(Integer, nullable=True)
    quantity = Column(Integer, default=1)

    # Many-to-One avec Author
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    author = relationship("Author", back_populates="books")

    # Many-to-Many avec Category
    categories = relationship("Category", secondary=book_category, back_populates="books")

    # One-to-Many avec Loan
    loans = relationship("Loan", back_populates="book")
