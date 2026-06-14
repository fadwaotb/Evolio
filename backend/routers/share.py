"""
Shareable portfolio link routes.

A student generates a token-style link. Anyone (e.g. an employer) can open the
public link to view that student's portfolio data -- no login required.
Visibility and expiration are placeholders for now and are not enforced.
"""

import secrets

from fastapi import APIRouter, Depends, HTTPException

from auth.auth import require_student
from db.database import profiles, projects, share_links
from schemas import ShareLinkIn, ShareLinkOut, ShareSettingsIn

router = APIRouter(prefix="/api/share", tags=["share"])

# Base URL used to build the shareable link shown to the student (frontend).
FRONTEND_BASE = "http://localhost:5173"


def _find_link_for_user(user_id: int):
    for link in share_links.values():
        if link["owner_id"] == user_id:
            return link
    return None


@router.post("/generate", response_model=ShareLinkOut)
def generate_share_link(data: ShareLinkIn, user=Depends(require_student)):
    # Reuse an existing link for this student if one already exists.
    link = _find_link_for_user(user["id"])
    if link is None:
        token = secrets.token_urlsafe(12)
        link = {
            "token": token,
            "owner_id": user["id"],
            "visibility": data.visibility,
            "expires_at": data.expires_at,
        }
        share_links[token] = link
    else:
        link["visibility"] = data.visibility
        link["expires_at"] = data.expires_at

    return ShareLinkOut(
        token=link["token"],
        url=f"{FRONTEND_BASE}/portfolio/{link['token']}",
        visibility=link["visibility"],
        expires_at=link["expires_at"],
    )


@router.get("/{token}")
def get_public_portfolio(token: str):
    """Public endpoint: return the shared student's profile + projects."""
    link = share_links.get(token)
    if link is None:
        raise HTTPException(status_code=404, detail="Share link not found.")

    owner_id = link["owner_id"]
    profile = profiles.get(owner_id)
    owner_projects = [p for p in projects.values() if p["owner_id"] == owner_id]

    return {
        "token": token,
        "visibility": link["visibility"],
        "profile": profile,
        "projects": owner_projects,
    }


@router.put("/settings", response_model=ShareLinkOut)
def update_share_settings(data: ShareSettingsIn, user=Depends(require_student)):
    link = _find_link_for_user(user["id"])
    if link is None:
        raise HTTPException(
            status_code=404,
            detail="No share link yet. Generate one first.",
        )

    if data.visibility is not None:
        link["visibility"] = data.visibility
    if data.expires_at is not None:
        link["expires_at"] = data.expires_at

    return ShareLinkOut(
        token=link["token"],
        url=f"{FRONTEND_BASE}/portfolio/{link['token']}",
        visibility=link["visibility"],
        expires_at=link["expires_at"],
    )
