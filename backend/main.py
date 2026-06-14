"""
main.py
-------
The entry point of the backend. Run it with:

    cd backend
    uvicorn main:app --reload

Then open http://127.0.0.1:8000/docs to see and try every endpoint.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import storage
from db.database import init_db
from routers import auth, profile, projects, resume, review, share_links

app = FastAPI(title="Evolio Portfolio API")

# Allow the React frontend (running on a different port) to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    # 1. Make sure the upload folders exist.
    storage.ensure_upload_dirs()
    # 2. Create the database file + all tables if they don't exist yet.
    init_db()


# Serve uploaded files (resumes, project images) at /uploads/... so the
# frontend can show images and download resumes by URL.
storage.ensure_upload_dirs()
app.mount("/uploads", StaticFiles(directory=str(storage.UPLOADS_DIR)), name="uploads")


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Evolio backend is running."}


# Plug in all the feature routers.
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(resume.router)
app.include_router(projects.router)
app.include_router(share_links.router)
app.include_router(review.router)
