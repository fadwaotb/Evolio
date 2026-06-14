"""
storage.py
----------
Helpers for saving uploaded files to disk.

Reminder: the database only stores METADATA (file name, size, where it is).
The real files live under backend/uploads/. We never put files inside SQLite.
"""

import secrets
import shutil
from pathlib import Path

# backend/  (the folder this file is in)
BACKEND_DIR = Path(__file__).resolve().parent

UPLOADS_DIR = BACKEND_DIR / "uploads"
RESUMES_DIR = UPLOADS_DIR / "resumes"
PROJECT_IMAGES_DIR = UPLOADS_DIR / "project_images"


def ensure_upload_dirs():
    """Create the upload folders if they don't exist yet."""
    RESUMES_DIR.mkdir(parents=True, exist_ok=True)
    PROJECT_IMAGES_DIR.mkdir(parents=True, exist_ok=True)


def _unique_name(original_name: str) -> str:
    """Add a random prefix so two files with the same name don't clash."""
    suffix = Path(original_name).suffix          # keeps ".pdf", ".png", etc.
    return f"{secrets.token_hex(8)}{suffix}"


def save_upload(upload_file, target_dir: Path) -> dict:
    """
    Save a FastAPI UploadFile to `target_dir` and return its metadata dict.
    """
    target_dir.mkdir(parents=True, exist_ok=True)
    stored_name = _unique_name(upload_file.filename or "file")
    file_path = target_dir / stored_name

    with open(file_path, "wb") as out:
        shutil.copyfileobj(upload_file.file, out)

    size_bytes = file_path.stat().st_size
    return {
        "original_name": upload_file.filename,
        "stored_name": stored_name,
        "file_path": str(file_path),
        "content_type": upload_file.content_type,
        "size_bytes": size_bytes,
    }


def delete_file(file_path: str):
    """Delete a file from disk if it exists. Never crashes if it's already gone."""
    try:
        Path(file_path).unlink(missing_ok=True)
    except OSError:
        pass
