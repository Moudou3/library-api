from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    biography = Column(Text, nullable=True)

    # One-to-Many avec Book
    books = relationship("Book", back_populates="author", cascade="all, delete-orphan")
