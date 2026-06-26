from sqlalchemy.orm import Session
from ..models import User
from ..schemas import UserCreate
from ..core.security import get_password_hash

def get_user_by_email(db: Session, email: str):
    """Fetch a user by their email address."""
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    """Hash the password and store the new user in the database."""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
