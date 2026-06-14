"""
routers/auth.py
---------------
Register, login, and "who am I" endpoints.

All four roles (Student, Employer, Admin, Career Coach) can register and login.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import auth_utils
import schemas
from db import repository
from db.database import get_db
from db.model import ALLOWED_ROLES

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=schemas.AuthResponse)
def register(payload: schemas.RegisterRequest, db: Session = Depends(get_db)):
    # 1. Role must be one of the four allowed roles.
    if payload.role not in ALLOWED_ROLES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Role must be one of: {', '.join(ALLOWED_ROLES)}",
        )

    # 2. Email must be unique.
    if repository.get_user_by_email(db, payload.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists.",
        )

    # 3. Create the user with a hashed password.
    user = repository.create_user(
        db,
        email=payload.email,
        password_hash=auth_utils.hash_password(payload.password),
        full_name=payload.full_name,
        role=payload.role,
    )

    # 4. Log them in right away by handing back a token.
    token = auth_utils.create_token()
    repository.set_user_token(db, user, token)
    return {"token": token, "user": user}


@router.post("/login", response_model=schemas.AuthResponse)
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = repository.get_user_by_email(db, payload.email)
    if user is None or not auth_utils.verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong email or password.",
        )

    token = auth_utils.create_token()
    repository.set_user_token(db, user, token)
    return {"token": token, "user": user}


@router.get("/me", response_model=schemas.UserOut)
def me(current_user=Depends(auth_utils.get_current_user)):
    """Returns the currently logged-in user and their role."""
    return current_user
