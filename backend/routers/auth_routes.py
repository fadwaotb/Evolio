"""
Auth routes: register, login, and "who am I".

Only students and employers are supported. Users are stored in the in-memory
`users` dict for now.
"""

from fastapi import APIRouter, Depends, HTTPException

from auth.auth import (
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
)
from db.database import get_user_by_email, next_id, users
from schemas import LoginRequest, RegisterRequest, TokenResponse, UserOut

router = APIRouter(prefix="/api/auth", tags=["auth"])

# The only roles this limited backend accepts.
ALLOWED_ROLES = {"student", "employer"}


def _normalize_role(role: str) -> str:
    """
    Accept the frontend's display values ("Student", "Employer") as well as
    lowercase values, and return a clean lowercase role.
    """
    return (role or "").strip().lower()


@router.post("/register", response_model=UserOut)
def register(data: RegisterRequest):
    role = _normalize_role(data.role)
    if role not in ALLOWED_ROLES:
        raise HTTPException(
            status_code=400,
            detail="Only Student and Employer accounts can be created.",
        )

    if get_user_by_email(data.email):
        raise HTTPException(
            status_code=400,
            detail="An account with this email already exists.",
        )

    user_id = next_id()
    user = {
        "id": user_id,
        "name": data.name,
        "email": data.email,
        "hashed_password": hash_password(data.password),
        "role": role,
    }
    users[user_id] = user
    return UserOut(**user)


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):
    user = get_user_by_email(data.email)
    if user is None or not verify_password(data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    # If the frontend sent a role, make sure it matches the stored one.
    if data.role:
        requested_role = _normalize_role(data.role)
        if requested_role not in ALLOWED_ROLES:
            raise HTTPException(
                status_code=400,
                detail="Only Student and Employer accounts can sign in.",
            )
        if requested_role != user["role"]:
            raise HTTPException(
                status_code=401,
                detail=f"This account is registered as a {user['role']}.",
            )

    token = create_access_token({"sub": str(user["id"]), "role": user["role"]})
    return TokenResponse(access_token=token, role=user["role"])


@router.get("/me", response_model=UserOut)
def me(user=Depends(get_current_user)):
    return UserOut(**user)
