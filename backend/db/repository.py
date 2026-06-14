"""
repository.py
-------------
These are small, simple helper functions that read from and write to the
database. The routers (the API endpoints) call these functions so the
endpoints stay short and easy to read.

Beginner notes:
- Every function takes `db` (a database session) as its first argument.
- "commit" = save the changes permanently.
- "refresh" = reload the row so we get the new id / timestamps back.
- We keep these functions tiny on purpose.
"""

import json
import secrets
from datetime import datetime

from sqlalchemy.orm import Session

from db import model


# ===========================================================================
# Small helpers for the JSON-string list fields (skills, tech stack, ...)
# ===========================================================================
def list_to_json(value):
    """Turn a Python list into a JSON string for storage. None -> None."""
    if value is None:
        return None
    return json.dumps(value)


def json_to_list(value):
    """Turn a stored JSON string back into a Python list. None -> []."""
    if not value:
        return []
    try:
        return json.loads(value)
    except (ValueError, TypeError):
        return []


# ===========================================================================
# AUTH
# ===========================================================================
def create_user(db: Session, email: str, password_hash: str, full_name: str, role: str):
    user = model.User(
        email=email,
        password_hash=password_hash,
        full_name=full_name,
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_email(db: Session, email: str):
    return db.query(model.User).filter(model.User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(model.User).filter(model.User.id == user_id).first()


def get_user_by_token(db: Session, token: str):
    """Used to figure out who is logged in, from their Bearer token."""
    if not token:
        return None
    return db.query(model.User).filter(model.User.auth_token == token).first()


def set_user_token(db: Session, user: model.User, token: str):
    """Save a fresh login token on the user (called at login)."""
    user.auth_token = token
    db.commit()
    db.refresh(user)
    return user


def verify_user_role(user: model.User, allowed_roles) -> bool:
    """True if the user's role is in the allowed list. (Handy in routers.)"""
    return user is not None and user.role in allowed_roles


# ===========================================================================
# STUDENT PROFILE
# ===========================================================================
def get_profile_by_user_id(db: Session, user_id: int):
    return (
        db.query(model.StudentProfile)
        .filter(model.StudentProfile.user_id == user_id)
        .first()
    )


def create_or_update_profile(db: Session, user_id: int, data: dict):
    """
    If the user already has a profile, update it. Otherwise create one.
    `data` is a plain dict of the fields to set. `skills` (a list) is stored
    in skills_json automatically.
    """
    profile = get_profile_by_user_id(db, user_id)
    if profile is None:
        profile = model.StudentProfile(user_id=user_id)
        db.add(profile)

    # Simple, explicit field-by-field update.
    profile.headline = data.get("headline", profile.headline)
    profile.bio = data.get("bio", profile.bio)
    profile.location = data.get("location", profile.location)
    profile.target_roles = data.get("target_roles", profile.target_roles)
    profile.contact_email = data.get("contact_email", profile.contact_email)
    profile.avatar_color = data.get("avatar_color", profile.avatar_color)
    profile.availability = data.get("availability", profile.availability)

    if "skills" in data:
        profile.skills_json = list_to_json(data.get("skills"))

    db.commit()
    db.refresh(profile)
    return profile


# ----- Social links (children of a profile) -----
def add_social_link(db: Session, profile_id: int, type_: str, url: str, label: str):
    link = model.SocialLink(
        student_profile_id=profile_id, type=type_, url=url, label=label
    )
    db.add(link)
    db.commit()
    db.refresh(link)
    return link


def get_social_links(db: Session, profile_id: int):
    return (
        db.query(model.SocialLink)
        .filter(model.SocialLink.student_profile_id == profile_id)
        .all()
    )


def get_social_link_by_type(db: Session, profile_id: int, type_: str):
    return (
        db.query(model.SocialLink)
        .filter(
            model.SocialLink.student_profile_id == profile_id,
            model.SocialLink.type == type_,
        )
        .first()
    )


def upsert_social_link_by_type(db: Session, profile_id: int, type_: str, url: str):
    """
    Convenience used by the profile editor for GitHub / LinkedIn.
    - empty url  -> delete the link if it exists
    - has a url  -> update the existing one, or create a new one
    """
    link = get_social_link_by_type(db, profile_id, type_)
    if not url:
        if link:
            db.delete(link)
            db.commit()
        return None
    if link:
        link.url = url
    else:
        link = model.SocialLink(
            student_profile_id=profile_id, type=type_, url=url, label=type_
        )
        db.add(link)
    db.commit()
    db.refresh(link)
    return link


def delete_social_link(db: Session, link_id: int, profile_id: int):
    link = (
        db.query(model.SocialLink)
        .filter(
            model.SocialLink.id == link_id,
            model.SocialLink.student_profile_id == profile_id,
        )
        .first()
    )
    if link:
        db.delete(link)
        db.commit()
    return link


# ===========================================================================
# RESUME
# ===========================================================================
def get_resume_by_user_id(db: Session, user_id: int):
    return db.query(model.Resume).filter(model.Resume.user_id == user_id).first()


def save_resume_metadata(db: Session, user_id: int, meta: dict):
    """Create or replace the resume metadata row for this user."""
    resume = get_resume_by_user_id(db, user_id)
    if resume is None:
        resume = model.Resume(user_id=user_id)
        db.add(resume)

    resume.original_name = meta["original_name"]
    resume.stored_name = meta["stored_name"]
    resume.file_path = meta["file_path"]
    resume.content_type = meta.get("content_type")
    resume.size_bytes = meta.get("size_bytes")
    resume.uploaded_at = datetime.utcnow()

    db.commit()
    db.refresh(resume)
    return resume


def delete_resume_metadata(db: Session, user_id: int):
    resume = get_resume_by_user_id(db, user_id)
    if resume:
        db.delete(resume)
        db.commit()
    return resume


# ===========================================================================
# PROJECTS
# ===========================================================================
def create_project(db: Session, user_id: int, data: dict):
    project = model.Project(
        user_id=user_id,
        title=data.get("title", "Untitled Project"),
        summary=data.get("summary"),
        description=data.get("description"),
        role=data.get("role"),
        duration=data.get("duration"),
        github_link=data.get("github_link"),
        demo_link=data.get("demo_link"),
        results=data.get("results"),
        status=data.get("status", "Draft"),
        tech_stack_json=list_to_json(data.get("tech_stack")),
        skills_json=list_to_json(data.get("skills")),
        collaborators_json=list_to_json(data.get("collaborators")),
        is_featured=data.get("is_featured", False),
        sort_order=data.get("sort_order", 0),
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def get_projects_by_user_id(db: Session, user_id: int):
    return (
        db.query(model.Project)
        .filter(model.Project.user_id == user_id)
        .order_by(model.Project.sort_order, model.Project.id)
        .all()
    )


def get_project_by_id(db: Session, project_id: int):
    return db.query(model.Project).filter(model.Project.id == project_id).first()


def update_project(db: Session, project: model.Project, data: dict):
    """Update only the fields that were provided in `data`."""
    simple_fields = [
        "title", "summary", "description", "role", "duration",
        "github_link", "demo_link", "results", "status", "is_featured", "sort_order",
    ]
    for field in simple_fields:
        if field in data:
            setattr(project, field, data[field])

    if "tech_stack" in data:
        project.tech_stack_json = list_to_json(data["tech_stack"])
    if "skills" in data:
        project.skills_json = list_to_json(data["skills"])
    if "collaborators" in data:
        project.collaborators_json = list_to_json(data["collaborators"])

    db.commit()
    db.refresh(project)
    return project


def save_project_content(db: Session, project: model.Project, content: str):
    """Save the Markdown / rich-text body of a project."""
    project.description = content
    db.commit()
    db.refresh(project)
    return project


def delete_project(db: Session, project: model.Project):
    db.delete(project)
    db.commit()
    return project


# ===========================================================================
# PROJECT IMAGES
# ===========================================================================
def save_project_image_metadata(db: Session, project_id: int, meta: dict):
    image = model.ProjectImage(
        project_id=project_id,
        original_name=meta["original_name"],
        stored_name=meta["stored_name"],
        file_path=meta["file_path"],
        content_type=meta.get("content_type"),
        size_bytes=meta.get("size_bytes"),
        caption=meta.get("caption"),
    )
    db.add(image)
    db.commit()
    db.refresh(image)
    return image


def get_project_images(db: Session, project_id: int):
    return (
        db.query(model.ProjectImage)
        .filter(model.ProjectImage.project_id == project_id)
        .all()
    )


def get_project_image_by_id(db: Session, image_id: int):
    return (
        db.query(model.ProjectImage)
        .filter(model.ProjectImage.id == image_id)
        .first()
    )


def delete_project_image(db: Session, image: model.ProjectImage):
    db.delete(image)
    db.commit()
    return image


# ===========================================================================
# SHARE LINKS
# ===========================================================================
def create_share_link(db: Session, user_id: int, visibility: str = "private"):
    token = secrets.token_urlsafe(16)        # a random, hard-to-guess string
    link = model.ShareLink(user_id=user_id, token=token, visibility=visibility)
    db.add(link)
    db.commit()
    db.refresh(link)
    return link


def get_share_link_by_token(db: Session, token: str):
    return db.query(model.ShareLink).filter(model.ShareLink.token == token).first()


def get_share_link_by_user_id(db: Session, user_id: int):
    return (
        db.query(model.ShareLink)
        .filter(model.ShareLink.user_id == user_id)
        .order_by(model.ShareLink.id.desc())
        .first()
    )


def update_share_settings(db: Session, link: model.ShareLink, data: dict):
    if "visibility" in data:
        link.visibility = data["visibility"]
    if "is_active" in data:
        link.is_active = data["is_active"]
    if "expires_at" in data:
        link.expires_at = data["expires_at"]
    db.commit()
    db.refresh(link)
    return link


# ===========================================================================
# REVIEW WORKFLOW
# ===========================================================================
def _get_or_create_review(db: Session, user_id: int):
    review = (
        db.query(model.PortfolioReview)
        .filter(model.PortfolioReview.user_id == user_id)
        .first()
    )
    if review is None:
        review = model.PortfolioReview(user_id=user_id, status="Draft")
        db.add(review)
        db.commit()
        db.refresh(review)
    return review


def submit_review(db: Session, user_id: int, status: str = "Ready", feedback: str = None):
    """
    Student submits their portfolio for review. Sets the status and stamps
    submitted_at. Creates the review row if it does not exist yet.
    """
    review = _get_or_create_review(db, user_id)
    review.status = status
    if feedback is not None:
        review.feedback = feedback
    review.submitted_at = datetime.utcnow()
    db.commit()
    db.refresh(review)
    return review


def get_review_status(db: Session, user_id: int):
    review = _get_or_create_review(db, user_id)
    return review.status


def get_review_feedback(db: Session, user_id: int):
    review = _get_or_create_review(db, user_id)
    return review.feedback
