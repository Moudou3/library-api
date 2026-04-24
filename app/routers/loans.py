from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.loan_service import LoanService
from app.schemas.loan import LoanCreate, LoanResponse

router = APIRouter(prefix="/api/loans", tags=["Loans"])


@router.get("", response_model=list[LoanResponse])
def get_all_loans(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    service = LoanService(db)
    loans = service.get_all(skip, limit)
    return [_loan_to_response(loan) for loan in loans]


@router.get("/{loan_id}", response_model=LoanResponse)
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    service = LoanService(db)
    loan = service.get_by_id(loan_id)
    return _loan_to_response(loan)


@router.post("", response_model=LoanResponse, status_code=status.HTTP_201_CREATED)
def create_loan(data: LoanCreate, db: Session = Depends(get_db)):
    service = LoanService(db)
    loan = service.create(data)
    return _loan_to_response(loan)


@router.put("/{loan_id}/return", response_model=LoanResponse)
def return_book(loan_id: int, db: Session = Depends(get_db)):
    service = LoanService(db)
    loan = service.return_book(loan_id)
    return _loan_to_response(loan)


def _loan_to_response(loan) -> LoanResponse:
    return LoanResponse(
        id=loan.id,
        loan_date=loan.loan_date,
        due_date=loan.due_date,
        return_date=loan.return_date,
        status=loan.status,
        user_id=loan.user_id,
        book_id=loan.book_id,
        book_title=loan.book.title if loan.book else None,
        user_name=f"{loan.user.first_name} {loan.user.last_name}" if loan.user else None
    )
