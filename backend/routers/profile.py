"""
Student profile routes: get and update the logged-in student's own profile.
"""

from fastapi import APIRouter, Depends

from auth.auth import require_student
from db.database import profiles
from schemas import ProfileIn, ProfileOut

router = APIRouter(prefix="/api/profile", tags=["profile"])


def _default_profile(user) -> dict:
    """A blank profile pre-filled with the account name/email."""
    return {
        "user_id": user["id"],
        "name": user["name"],
        "headline": "",
        "bio": "",
        "skills": [],
        "location": "",
        "github": "",
        "linkedin": "",
        "contact_email": user["email"],
        "availability": "Open to work",
    }


@router.get("", response_model=ProfileOut)
def get_profile(user=Depends(require_student)):
    # Create a default profile the first time it is requested.
    profile = profiles.get(user["id"])
    if profile is None:
        profile = _default_profile(user)
        profiles[user["id"]] = profile
    return ProfileOut(**profile)


@router.put("", response_model=ProfileOut)
def update_profile(data: ProfileIn, user=Depends(require_student)):
    profile = data.model_dump()
    profile["user_id"] = user["id"]
    profiles[user["id"]] = profile
    return ProfileOut(**profile)
