"""
Resume routes: upload/replace, view metadata, download, delete.

One resume per student. Stored on local disk under uploads/resumes/.
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse

from auth.auth import require_student
from db.database import resumes
from schemas import ResumeMeta
from storage import RESUME_DIR, delete_file, save_upload

router = APIRouter(prefix="/api/resume", tags=["resume"])

# PDF always; DOCX too since it is simple to allow.
ALLOWED_RESUME_EXTS = {"pdf", "docx"}


@router.post("/upload", response_model=ResumeMeta)
def upload_resume(file: UploadFile = File(...), user=Depends(require_student)):
    # Remove any previous resume file first (this also handles "replace").
    existing = resumes.get(user["id"])
    if existing:
        delete_file(existing["path"])

    meta = save_upload(file, RESUME_DIR, ALLOWED_RESUME_EXTS)
    resumes[user["id"]] = meta
    return ResumeMeta(**meta)


@router.get("", response_model=ResumeMeta)
def get_resume(user=Depends(require_student)):
    meta = resumes.get(user["id"])
    if meta is None:
        raise HTTPException(status_code=404, detail="No resume uploaded yet.")
    return ResumeMeta(**meta)


@router.get("/download")
def download_resume(user=Depends(require_student)):
    meta = resumes.get(user["id"])
    if meta is None:
        raise HTTPException(status_code=404, detail="No resume uploaded yet.")
    return FileResponse(
        meta["path"],
        filename=meta["original_filename"],
    )


@router.delete("")
def delete_resume(user=Depends(require_student)):
    meta = resumes.pop(user["id"], None)
    if meta is None:
        raise HTTPException(status_code=404, detail="No resume to delete.")
    delete_file(meta["path"])
    return {"message": "Resume deleted."}
