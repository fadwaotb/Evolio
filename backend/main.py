"""
Evolio backend - limited FastAPI app for the student portfolio workflow plus
student/employer login and account creation.

Run from inside the backend/ folder:
    pip install -r requirements.txt
    uvicorn main:app --reload

Data is kept in memory for now (see db/database.py). SQLite comes in a later
step.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from storage import UPLOAD_ROOT
from routers import (
    auth_routes,
    image,
    profile,
    project,
    resume,
    review,
    share,
)

app = FastAPI(title="Evolio Backend", version="0.1.0")

# --- CORS: allow the local React (Vite) dev server -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers ----------------------------------------------------------------
app.include_router(auth_routes.router)
app.include_router(profile.router)
app.include_router(resume.router)
app.include_router(project.router)
app.include_router(image.router)
app.include_router(share.router)
app.include_router(review.router)

# --- Serve uploaded files so returned URLs are downloadable -----------------
# e.g. http://localhost:8000/uploads/project_images/<file>
app.mount("/uploads", StaticFiles(directory=UPLOAD_ROOT), name="uploads")


# --- Health check -----------------------------------------------------------
@app.get("/api/health", tags=["health"])
def health():
    return {"status": "ok"}
