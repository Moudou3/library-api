from sqlalchemy.orm import Session
from datetime import date
from app.models.loan import Loan, LoanStatus
from app.repositories.loan_repository import LoanRepository
from app.services.book_service import BookService
from app.schemas.loan import LoanCreate
from app.exceptions import NotFoundException, BadRequestException


class LoanService:
    def __init__(self, db: Session):
        self.repository = LoanRepository(db)
        self.book_service = BookService(db)
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Loan]:
        return self.repository.get_all(skip, limit)

    def get_by_id(self, loan_id: int) -> Loan:
        loan = self.repository.get_by_id(loan_id)
        if not loan:
            raise NotFoundException(f"Loan with id {loan_id} not found")
        return loan

    def get_by_user(self, user_id: int) -> list[Loan]:
        return self.repository.get_by_user(user_id)

    def create(self, data: LoanCreate) -> Loan:
        book = self.book_service.get_by_id(data.book_id)

        # Vérifier disponibilité
        active_loans = self.repository.get_active_by_book(data.book_id)
        if len(active_loans) >= book.quantity:
            raise BadRequestException(f"No copies available for book '{book.title}'")

        loan = Loan(
            user_id=data.user_id,
            book_id=data.book_id,
            loan_date=date.today(),
            due_date=data.due_date,
            status=LoanStatus.ACTIVE
        )
        return self.repository.create(loan)

    def return_book(self, loan_id: int) -> Loan:
        loan = self.get_by_id(loan_id)

        if loan.status == LoanStatus.RETURNED:
            raise BadRequestException("This loan has already been returned")

        loan.return_date = date.today()
        loan.status = LoanStatus.RETURNED
        return self.repository.update(loan)
