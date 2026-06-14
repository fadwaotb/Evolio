"""
Auth routes: register, login, and "who am I".

Students, employers, admins, and career coaches can all register and log in.
(Only the auth flow is shared -- admin/coach-specific features are not built.)
Users are stored in the in-memory `users` dict for now.
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

# Roles this backend accepts for auth. Note: only "student" gets access to the
# student-only endpoints -- the other roles can sign in but have no extra
# features in this phase.
ALLOWED_ROLES = {"student", "employer", "admin", "coach"}

# Map frontend display values to canonical role tokens.
ROLE_ALIASES = {"career coach": "coach"}


def _normalize_role(role: str) -> str:
    """
    Accept the frontend's display values ("Student", "Career Coach", ...) and
    return a clean canonical role token (e.g. "career coach" -> "coach").
    """
    cleaned = (role or "").strip().lower()
    return ROLE_ALIASES.get(cleaned, cleaned)


@router.post("/register", response_model=UserOut)
def register(data: RegisterRequest):
    role = _normalize_role(data.role)
    if role not in ALLOWED_ROLES:
        raise HTTPException(
            status_code=400,
            detail="Invalid account role.",
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
                detail="Invalid account role.",
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
