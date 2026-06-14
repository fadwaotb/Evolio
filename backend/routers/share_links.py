"""
routers/share_links.py
-----------------------
Generate and manage the shareable portfolio link. Student-only to CREATE/EDIT,
but viewing by token is PUBLIC (that's the whole point of a shareable link).
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import schemas
from auth_utils import require_student
from db import repository
from db.database import get_db

router = APIRouter(prefix="/api/share-link", tags=["share-link"])


def _link_to_dict(link):
    return {
        "id": link.id,
        "token": link.token,
        "visibility": link.visibility,
        "is_active": link.is_active,
        "expires_at": link.expires_at,
    }


@router.get("")
def get_my_share_link(db: Session = Depends(get_db), user=Depends(require_student)):
    link = repository.get_share_link_by_user_id(db, user.id)
    if link is None:
        return None
    return _link_to_dict(link)


@router.post("")
def create_share_link(
    payload: schemas.ShareLinkRequest,
    db: Session = Depends(get_db),
    user=Depends(require_student),
):
    link = repository.create_share_link(db, user.id, payload.visibility)
    return _link_to_dict(link)


@router.put("")
def update_share_link(
    payload: schemas.ShareSettingsRequest,
    db: Session = Depends(get_db),
    user=Depends(require_student),
):
    link = repository.get_share_link_by_user_id(db, user.id)
    if link is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No share link yet. Create one first.")
    link = repository.update_share_settings(db, link, payload.model_dump(exclude_unset=True))
    return _link_to_dict(link)


# ---- PUBLIC: anyone with the token can view (no login required) ----
@router.get("/view/{token}")
def view_shared_portfolio(token: str, db: Session = Depends(get_db)):
    link = repository.get_share_link_by_token(db, token)
    if link is None or not link.is_active:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Portfolio link not found or disabled.")

    if link.visibility != "public":
        # Private links exist but this simple version only serves public ones.
        raise HTTPException(status.HTTP_403_FORBIDDEN, "This portfolio is private.")

    owner = repository.get_user_by_id(db, link.user_id)
    profile = repository.get_profile_by_user_id(db, link.user_id)
    projects = repository.get_projects_by_user_id(db, link.user_id)

    return {
        "owner": {
            "full_name": owner.full_name if owner else None,
            "email": owner.email if owner else None,
        },
        "profile": {
            "headline": profile.headline if profile else None,
            "bio": profile.bio if profile else None,
            "location": profile.location if profile else None,
            "skills": repository.json_to_list(profile.skills_json) if profile else [],
        },
        "projects": [
            {
                "id": p.id,
                "title": p.title,
                "summary": p.summary,
                "github_link": p.github_link,
                "demo_link": p.demo_link,
            }
            for p in projects
        ],
    }
