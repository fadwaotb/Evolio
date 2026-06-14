"""
routers/profile.py
------------------
Student profile + social links. Student-only (require_student).
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import schemas
from auth_utils import require_student
from db import repository
from db.database import get_db

router = APIRouter(prefix="/api/profile", tags=["profile"])


def _profile_to_dict(db, user, profile):
    """Turn a StudentProfile (+ its user and social links) into JSON data."""
    github = repository.get_social_link_by_type(db, profile.id, "GitHub")
    linkedin = repository.get_social_link_by_type(db, profile.id, "LinkedIn")
    return {
        "id": profile.id,
        "user_id": profile.user_id,
        "name": user.full_name,
        "email": user.email,
        "headline": profile.headline,
        "bio": profile.bio,
        "location": profile.location,
        "target_roles": profile.target_roles,
        "contact_email": profile.contact_email,
        "avatar_color": profile.avatar_color,
        "availability": profile.availability,
        "skills": repository.json_to_list(profile.skills_json),
        "github": github.url if github else "",
        "linkedin": linkedin.url if linkedin else "",
    }


@router.get("")
def get_my_profile(db: Session = Depends(get_db), user=Depends(require_student)):
    profile = repository.get_profile_by_user_id(db, user.id)
    if profile is None:
        # No profile row yet -> return just the basics from the user account so
        # the editor can pre-fill name + email.
        return {"name": user.full_name, "email": user.email}
    return _profile_to_dict(db, user, profile)


@router.put("")
def update_my_profile(
    payload: schemas.ProfileRequest,
    db: Session = Depends(get_db),
    user=Depends(require_student),
):
    # exclude_unset=True -> only send the fields the client actually filled in.
    data = payload.model_dump(exclude_unset=True)

    # "name" belongs to the User account, not the profile table.
    if "full_name" in data and data["full_name"] is not None:
        user.full_name = data["full_name"]
        db.commit()

    profile = repository.create_or_update_profile(db, user.id, data)

    # github / linkedin are stored as social links of a known type.
    if "github" in data:
        repository.upsert_social_link_by_type(db, profile.id, "GitHub", data["github"] or "")
    if "linkedin" in data:
        repository.upsert_social_link_by_type(db, profile.id, "LinkedIn", data["linkedin"] or "")

    return _profile_to_dict(db, user, profile)


# --------------------------- social links ---------------------------
def _ensure_profile(db, user):
    profile = repository.get_profile_by_user_id(db, user.id)
    if profile is None:
        # create an empty profile so links have a parent to attach to
        profile = repository.create_or_update_profile(db, user.id, {})
    return profile


@router.get("/social-links")
def list_social_links(db: Session = Depends(get_db), user=Depends(require_student)):
    profile = _ensure_profile(db, user)
    links = repository.get_social_links(db, profile.id)
    return [
        {"id": l.id, "type": l.type, "url": l.url, "label": l.label} for l in links
    ]


@router.post("/social-links")
def add_social_link(
    payload: schemas.SocialLinkRequest,
    db: Session = Depends(get_db),
    user=Depends(require_student),
):
    profile = _ensure_profile(db, user)
    link = repository.add_social_link(
        db, profile.id, payload.type, payload.url, payload.label
    )
    return {"id": link.id, "type": link.type, "url": link.url, "label": link.label}


@router.delete("/social-links/{link_id}")
def delete_social_link(
    link_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_student),
):
    profile = _ensure_profile(db, user)
    deleted = repository.delete_social_link(db, link_id, profile.id)
    if deleted is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Social link not found.")
    return {"deleted": True}
