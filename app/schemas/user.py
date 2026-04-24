from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import date


class LibraryCardResponse(BaseModel):
    id: int
    card_number: str
    issue_date: date
    expiry_date: date

    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    library_card: LibraryCardResponse | None = None

    model_config = ConfigDict(from_attributes=True)
