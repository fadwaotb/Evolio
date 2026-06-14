"""
routers/resume.py
-----------------
Upload / view / download / delete the student's resume. Student-only.

The PDF/Word file is saved on disk in backend/uploads/resumes/.
SQLite stores only the metadata.
"""

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

import storage
from auth_utils import require_student
from db import repository
from db.database import get_db

router = APIRouter(prefix="/api/resume", tags=["resume"])


def _resume_to_dict(resume):
    size_kb = round((resume.size_bytes or 0) / 1024, 1)
    return {
        "id": resume.id,
        "original_name": resume.original_name,
        "content_type": resume.content_type,
        "size_bytes": resume.size_bytes,
        "size_kb": size_kb,
        "uploaded_at": resume.uploaded_at,
        "url": f"/uploads/resumes/{resume.stored_name}",
    }


@router.get("")
def get_resume(db: Session = Depends(get_db), user=Depends(require_student)):
    resume = repository.get_resume_by_user_id(db, user.id)
    if resume is None:
        return None
    return _resume_to_dict(resume)


@router.post("")
def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(require_student),
):
    # If a resume already exists, delete the old FILE before replacing it.
    existing = repository.get_resume_by_user_id(db, user.id)
    if existing:
        storage.delete_file(existing.file_path)

    meta = storage.save_upload(file, storage.RESUMES_DIR)
    resume = repository.save_resume_metadata(db, user.id, meta)
    return _resume_to_dict(resume)


@router.get("/download")
def download_resume(db: Session = Depends(get_db), user=Depends(require_student)):
    resume = repository.get_resume_by_user_id(db, user.id)
    if resume is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No resume uploaded.")
    return FileResponse(
        path=resume.file_path,
        filename=resume.original_name,
        media_type=resume.content_type or "application/octet-stream",
    )


@router.delete("")
def delete_resume(db: Session = Depends(get_db), user=Depends(require_student)):
    resume = repository.get_resume_by_user_id(db, user.id)
    if resume is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No resume to delete.")
    storage.delete_file(resume.file_path)
    repository.delete_resume_metadata(db, user.id)
    return {"deleted": True}
