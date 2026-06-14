"""
Simple JWT-style authentication utilities.

For this phase everything works against the in-memory `users` dict in
db/database.py. The structure (hashing + bearer token + dependency) is the same
one we will keep when SQLite is added later, so the routers will not need to
change.
"""

from datetime import datetime, timedelta

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

from db.database import users


# --- Configuration ----------------------------------------------------------

# NOTE: hard-coded for local development only. Move to an env variable later.
SECRET_KEY = "evolio-dev-secret-change-me"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

# Reads the "Authorization: Bearer <token>" header.
bearer_scheme = HTTPBearer(auto_error=False)


# --- Password helpers (bcrypt) ----------------------------------------------

# bcrypt only looks at the first 72 bytes of a password, so we truncate to keep
# it happy on every version.

def hash_password(password: str) -> str:
    pw_bytes = password.encode("utf-8")[:72]
    return bcrypt.hashpw(pw_bytes, bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    pw_bytes = plain_password.encode("utf-8")[:72]
    return bcrypt.checkpw(pw_bytes, hashed_password.encode("utf-8"))


# --- Token helpers ----------------------------------------------------------

def create_access_token(data: dict) -> str:
    """Create a signed JWT containing the given data plus an expiry."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    """Decode a JWT. Raises JWTError if invalid or expired."""
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


# --- Dependencies -----------------------------------------------------------

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    """
    Return the logged-in user (from the in-memory store) based on the bearer
    token. Raises 401 if the token is missing, invalid, or the user no longer
    exists.
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated. Please log in.",
        )

    try:
        payload = decode_token(credentials.credentials)
        user_id = payload.get("sub")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
        )

    # "sub" is stored as a string in the token; our keys are integers.
    user = users.get(int(user_id)) if user_id is not None else None
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
        )
    return user


def require_student(user=Depends(get_current_user)):
    """Allow only students through. Used for portfolio-editing routes."""
    if user["role"] != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can perform this action.",
        )
    return user


def require_employer(user=Depends(get_current_user)):
    """Allow only employers through."""
    if user["role"] != "employer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only employers can perform this action.",
        )
    return user
