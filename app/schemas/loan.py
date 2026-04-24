from pydantic import BaseModel, ConfigDict
from datetime import date
from app.models.loan import LoanStatus


class LoanCreate(BaseModel):
    user_id: int
    book_id: int
    due_date: date


class LoanResponse(BaseModel):
    id: int
    loan_date: date
    due_date: date
    return_date: date | None
    status: LoanStatus
    user_id: int
    book_id: int
    book_title: str | None = None
    user_name: str | None = None

    model_config = ConfigDict(from_attributes=True)
