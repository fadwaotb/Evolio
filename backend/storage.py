"""
Small helpers for saving uploaded files to local disk.

Used by the resume and project-image routers. Files are stored under
backend/uploads/. This will likely move to cloud storage later, but for now
local disk is fine.
"""

import os
import re
from datetime import datetime

from fastapi import HTTPException, UploadFile

# Anchor all paths to the backend/ folder (where this file lives) so uploads
# work no matter which directory uvicorn was started from.
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_ROOT = os.path.join(BACKEND_DIR, "uploads")
RESUME_DIR = os.path.join(UPLOAD_ROOT, "resumes")
IMAGE_DIR = os.path.join(UPLOAD_ROOT, "project_images")

# Web path prefix used to build URLs the frontend can open (see the /uploads
# static mount in main.py).
UPLOAD_URL_PREFIX = "/uploads"

# Max upload size (bytes). 10 MB is plenty for resumes and screenshots.
MAX_FILE_SIZE = 10 * 1024 * 1024

# Make sure the folders exist when the app starts.
os.makedirs(RESUME_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)


def _safe_filename(name: str) -> str:
    """Strip directories and unsafe characters from a user-supplied filename."""
    name = os.path.basename(name or "file")
    # Keep letters, numbers, dot, dash and underscore only.
    return re.sub(r"[^A-Za-z0-9._-]", "_", name)


def save_upload(upload: UploadFile, folder: str, allowed_exts: set) -> dict:
    """
    Validate and save an uploaded file. Returns a metadata dict.

    Raises HTTPException(400) for a bad type, HTTPException(413) for a file
    that is too large.
    """
    original = upload.filename or "file"
    ext = os.path.splitext(original)[1].lower().lstrip(".")
    if ext not in allowed_exts:
        allowed = ", ".join(sorted(allowed_exts)).upper()
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '.{ext}'. Allowed types: {allowed}.",
        )

    # Read the file and check size.
    contents = upload.file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File is too large. Maximum size is 10 MB.",
        )

    # Build a unique, safe filename so uploads never overwrite each other.
    safe = _safe_filename(original)
    stamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    stored_name = f"{stamp}_{safe}"
    path = os.path.join(folder, stored_name)
    with open(path, "wb") as f:
        f.write(contents)

    # URL the frontend can use (uploads/ is mounted statically in main.py).
    # e.g. /uploads/resumes/<stored_name>
    subfolder = os.path.basename(folder)
    url = f"{UPLOAD_URL_PREFIX}/{subfolder}/{stored_name}"

    return {
        "filename": stored_name,
        "original_filename": original,
        "url": url,
        "path": path,
        "upload_date": datetime.utcnow().isoformat(),
        "file_type": ext,
        "file_size": len(contents),
    }


def delete_file(path: str) -> None:
    """Remove a file from disk if it exists (ignore if already gone)."""
    try:
        if path and os.path.exists(path):
            os.remove(path)
    except OSError:
        # Best-effort cleanup; ignore disk errors for this phase.
        pass
