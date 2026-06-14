"""
routers/projects.py
--------------------
Create / read / update / delete projects, save the editor content, and manage
project images. Student-only, and a student can only touch THEIR OWN projects.
"""

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

import schemas
import storage
from auth_utils import require_student
from db import repository
from db.database import get_db

router = APIRouter(prefix="/api/projects", tags=["projects"])


def _image_url(image):
    # The uploads folder is served as static files in main.py.
    return f"/uploads/project_images/{image.stored_name}"


def _project_to_dict(project):
    return {
        "id": project.id,
        "user_id": project.user_id,
        "title": project.title,
        "summary": project.summary,
        "description": project.description,
        "role": project.role,
        "duration": project.duration,
        "github_link": project.github_link,
        "demo_link": project.demo_link,
        "results": project.results,
        "status": project.status,
        "tech_stack": repository.json_to_list(project.tech_stack_json),
        "skills": repository.json_to_list(project.skills_json),
        "collaborators": repository.json_to_list(project.collaborators_json),
        "is_featured": project.is_featured,
        "sort_order": project.sort_order,
        # URLs of uploaded screenshots (first one is the "cover").
        "screenshots": [_image_url(img) for img in project.images],
    }


def _get_owned_project(db, project_id, user):
    """Fetch a project and make sure it belongs to this user (else 404)."""
    project = repository.get_project_by_id(db, project_id)
    if project is None or project.user_id != user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found.")
    return project


@router.get("")
def list_projects(db: Session = Depends(get_db), user=Depends(require_student)):
    projects = repository.get_projects_by_user_id(db, user.id)
    return [_project_to_dict(p) for p in projects]


@router.post("")
def create_project(
    payload: schemas.ProjectRequest,
    db: Session = Depends(get_db),
    user=Depends(require_student),
):
    project = repository.create_project(db, user.id, payload.model_dump(exclude_unset=True))
    return _project_to_dict(project)


@router.get("/{project_id}")
def get_project(
    project_id: int, db: Session = Depends(get_db), user=Depends(require_student)
):
    project = _get_owned_project(db, project_id, user)
    return _project_to_dict(project)


@router.put("/{project_id}")
def update_project(
    project_id: int,
    payload: schemas.ProjectRequest,
    db: Session = Depends(get_db),
    user=Depends(require_student),
):
    project = _get_owned_project(db, project_id, user)
    project = repository.update_project(db, project, payload.model_dump(exclude_unset=True))
    return _project_to_dict(project)


@router.put("/{project_id}/content")
def save_content(
    project_id: int,
    payload: schemas.ProjectContentRequest,
    db: Session = Depends(get_db),
    user=Depends(require_student),
):
    """Save the Markdown / rich-text editor body for a project."""
    project = _get_owned_project(db, project_id, user)
    project = repository.save_project_content(db, project, payload.content)
    return _project_to_dict(project)


@router.delete("/{project_id}")
def delete_project(
    project_id: int, db: Session = Depends(get_db), user=Depends(require_student)
):
    project = _get_owned_project(db, project_id, user)
    # Delete the image files on disk first, then the DB rows (cascade).
    for image in repository.get_project_images(db, project.id):
        storage.delete_file(image.file_path)
    repository.delete_project(db, project)
    return {"deleted": True}


# --------------------------- project images ---------------------------
def _image_to_dict(image):
    return {
        "id": image.id,
        "project_id": image.project_id,
        "original_name": image.original_name,
        "content_type": image.content_type,
        "size_bytes": image.size_bytes,
        "caption": image.caption,
        "url": _image_url(image),
    }


@router.get("/{project_id}/images")
def list_images(
    project_id: int, db: Session = Depends(get_db), user=Depends(require_student)
):
    project = _get_owned_project(db, project_id, user)
    return [_image_to_dict(i) for i in repository.get_project_images(db, project.id)]


@router.post("/{project_id}/images")
def upload_image(
    project_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(require_student),
):
    project = _get_owned_project(db, project_id, user)
    meta = storage.save_upload(file, storage.PROJECT_IMAGES_DIR)
    image = repository.save_project_image_metadata(db, project.id, meta)
    return _image_to_dict(image)


@router.delete("/images/{image_id}")
def delete_image(
    image_id: int, db: Session = Depends(get_db), user=Depends(require_student)
):
    image = repository.get_project_image_by_id(db, image_id)
    if image is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Image not found.")
    # Make sure the image's project belongs to this user.
    project = repository.get_project_by_id(db, image.project_id)
    if project is None or project.user_id != user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Image not found.")
    storage.delete_file(image.file_path)
    repository.delete_project_image(db, image)
    return {"deleted": True}
