from sqlalchemy.orm import Session, joinedload
from app.models.loan import Loan, LoanStatus


class LoanRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Loan]:
        return (
            self.db.query(Loan)
            .options(joinedload(Loan.user), joinedload(Loan.book))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id(self, loan_id: int) -> Loan | None:
        return (
            self.db.query(Loan)
            .options(joinedload(Loan.user), joinedload(Loan.book))
            .filter(Loan.id == loan_id)
            .first()
        )

    def get_by_user(self, user_id: int) -> list[Loan]:
        return self.db.query(Loan).filter(Loan.user_id == user_id).all()

    def get_active_by_book(self, book_id: int) -> list[Loan]:
        return (
            self.db.query(Loan)
            .filter(Loan.book_id == book_id, Loan.status == LoanStatus.ACTIVE)
            .all()
        )

    def create(self, loan: Loan) -> Loan:
        self.db.add(loan)
        self.db.commit()
        self.db.refresh(loan)
        return loan

    def update(self, loan: Loan) -> Loan:
        self.db.commit()
        self.db.refresh(loan)
        return loan
