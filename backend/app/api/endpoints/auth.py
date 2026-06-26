from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ...database import get_db
from ...schemas import UserCreate, UserResponse, Token
from ...services import user_service
from ...core.security import verify_password, create_access_token
from ...models import User
from ..dependencies import get_current_user

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    - Validates email format via Pydantic.
    - Checks if the email is already registered.
    - Hashes the password and saves the user.
    - Returns the user profile (excluding the password).
    """
    # 1. Check if email is unique
    existing_user = user_service.get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # 2. Create the user
    new_user = user_service.create_user(db=db, user=user)
    
    # 3. Return secure response (Pydantic's response_model strips out hashed_password)
    return new_user

@router.post("/login", response_model=Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate a user and return a JWT access token.
    - Uses OAuth2 password flow (expects form data: username and password).
    - Validates credentials against the database.
    """
    # 1 & 2. Verify email exists (in OAuth2 flow, the email is sent as 'username')
    user = user_service.get_user_by_email(db, email=form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Verify password
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 4 & 5. Generate and return JWT
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Get current logged in user.
    - Requires a valid JWT access token.
    - Extracts the user from the token payload.
    - Returns the secure user profile.
    """
    return current_user
