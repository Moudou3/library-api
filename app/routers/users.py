from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session, joinedload
from datetime import date, timedelta
import uuid

from app.database import get_db
from app.models.user import User
from app.models.library_card import LibraryCard
from app.schemas.user import UserCreate, UserResponse
from app.schemas.loan import LoanResponse
from app.services.loan_service import LoanService
from app.exceptions import NotFoundException, ConflictException

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("", response_model=list[UserResponse])
def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return (
        db.query(User)
        .options(joinedload(User.library_card))
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = (
        db.query(User)
        .options(joinedload(User.library_card))
        .filter(User.id == user_id)
        .first()
    )
    if not user:
        raise NotFoundException(f"User with id {user_id} not found")
    return user


@router.get("/{user_id}/loans", response_model=list[LoanResponse])
def get_user_loans(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFoundException(f"User with id {user_id} not found")

    service = LoanService(db)
    loans = service.get_by_user(user_id)

    return [
        LoanResponse(
            id=loan.id,
            loan_date=loan.loan_date,
            due_date=loan.due_date,
            return_date=loan.return_date,
            status=loan.status,
            user_id=loan.user_id,
            book_id=loan.book_id
        )
        for loan in loans
    ]


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise ConflictException(f"User with email {data.email} already exists")

    user = User(
        email=data.email,
        password_hash=data.password,  # En production, hasher le mot de passe
        first_name=data.first_name,
        last_name=data.last_name
    )

    # Créer automatiquement une carte de bibliothèque (One-to-One)
    library_card = LibraryCard(
        card_number=f"LIB-{uuid.uuid4().hex[:8].upper()}",
        issue_date=date.today(),
        expiry_date=date.today() + timedelta(days=365)
    )
    user.library_card = library_card

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFoundException(f"User with id {user_id} not found")
    db.delete(user)
    db.commit()
