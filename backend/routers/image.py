"""
Project image routes: upload screenshots, list them, delete them.

Images are stored on local disk under uploads/project_images/. Only the project
owner (a student) may manage its images.
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from auth.auth import require_student
from db.database import next_id, project_images, projects
from schemas import ImageMeta
from storage import IMAGE_DIR, delete_file, save_upload

router = APIRouter(prefix="/api/projects", tags=["project-images"])

ALLOWED_IMAGE_EXTS = {"png", "jpg", "jpeg"}


def _require_owned_project(project_id: int, user) -> dict:
    project = projects.get(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found.")
    if project["owner_id"] != user["id"]:
        raise HTTPException(
            status_code=403,
            detail="You can only manage images on your own projects.",
        )
    return project


@router.post("/{project_id}/images", response_model=ImageMeta)
def upload_image(
    project_id: int, file: UploadFile = File(...), user=Depends(require_student)
):
    _require_owned_project(project_id, user)

    meta = save_upload(file, IMAGE_DIR, ALLOWED_IMAGE_EXTS)
    image_id = next_id()
    meta["id"] = image_id
    meta["project_id"] = project_id
    project_images[image_id] = meta
    return ImageMeta(**meta)


@router.get("/{project_id}/images", response_model=list[ImageMeta])
def list_images(project_id: int, user=Depends(require_student)):
    _require_owned_project(project_id, user)
    images = [
        img for img in project_images.values() if img["project_id"] == project_id
    ]
    return [ImageMeta(**img) for img in images]


@router.delete("/{project_id}/images/{image_id}")
def delete_image(project_id: int, image_id: int, user=Depends(require_student)):
    _require_owned_project(project_id, user)
    image = project_images.get(image_id)
    if image is None or image["project_id"] != project_id:
        raise HTTPException(status_code=404, detail="Image not found.")
    delete_file(image["path"])
    project_images.pop(image_id, None)
    return {"message": "Image deleted."}
