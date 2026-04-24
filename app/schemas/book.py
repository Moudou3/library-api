from pydantic import BaseModel, ConfigDict
from app.schemas.author import AuthorResponse
from app.schemas.category import CategoryResponse


class BookBase(BaseModel):
    isbn: str
    title: str
    publication_year: int | None = None
    quantity: int = 1


class BookCreate(BookBase):
    author_id: int
    category_ids: list[int] = []


class BookUpdate(BaseModel):
    title: str | None = None
    publication_year: int | None = None
    quantity: int | None = None
    category_ids: list[int] | None = None


class BookResponse(BookBase):
    id: int
    author: AuthorResponse
    categories: list[CategoryResponse] = []

    model_config = ConfigDict(from_attributes=True)


class BookListResponse(BaseModel):
    id: int
    isbn: str
    title: str
    author_name: str
    quantity: int

    model_config = ConfigDict(from_attributes=True)
