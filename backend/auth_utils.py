"""
auth_utils.py
-------------
Everything related to passwords and "who is logged in".

Beginner notes:
- We NEVER store the real password. We store a one-way "hash" of it.
- To log in, we hash the password the user typed and compare the hashes.
- After login we hand the frontend a random TOKEN. The frontend sends it back
  on every request in the header:  Authorization: Bearer <token>
- get_current_user() reads that header and finds the matching user.
- require_student() additionally blocks non-students with a 403 error.

We use only Python's built-in `hashlib`/`secrets` here, so there are no extra
packages to install for the security part.
"""

import hashlib
import secrets

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from db import repository
from db.database import get_db


# ---------------------------------------------------------------------------
# Passwords
# ---------------------------------------------------------------------------
def hash_password(password: str) -> str:
    """Return a string like '<salt>$<hash>'. The salt makes each hash unique."""
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), bytes.fromhex(salt), 100_000
    )
    return f"{salt}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    """Check a typed password against the stored '<salt>$<hash>' string."""
    try:
        salt, expected_hex = stored.split("$", 1)
    except (ValueError, AttributeError):
        return False
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), bytes.fromhex(salt), 100_000
    )
    # compare_digest avoids subtle timing attacks.
    return secrets.compare_digest(digest.hex(), expected_hex)


def create_token() -> str:
    """A random login token."""
    return secrets.token_hex(32)


# ---------------------------------------------------------------------------
# "Who is logged in?" dependencies for the routers
# ---------------------------------------------------------------------------
def get_current_user(
    authorization: str = Header(default=None),
    db: Session = Depends(get_db),
):
    """
    Reads the Authorization header, validates the token, returns the User.
    Raises 401 if there is no valid token.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated. Send 'Authorization: Bearer <token>'.",
        )
    token = authorization.split(" ", 1)[1].strip()
    user = repository.get_user_by_token(db, token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
        )
    return user


def require_student(current_user=Depends(get_current_user)):
    """
    Use this on student-only endpoints. Employer / Admin / Career Coach get 403.
    """
    if current_user.role != "Student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can access this resource.",
        )
    return current_user
