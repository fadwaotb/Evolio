"""
Pydantic schemas (request and response shapes only).

These describe the JSON the API accepts and returns. They are NOT database
models -- there is no SQLAlchemy here yet. Keeping them in one file makes the
limited backend easy to read.
"""

from typing import List, Optional
from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    # Only "student" or "employer" are allowed (validated in the router).
    role: str


class LoginRequest(BaseModel):
    email: str
    password: str
    # Sent by the frontend so we can double-check the chosen role.
    role: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str


# ---------------------------------------------------------------------------
# Profile
# ---------------------------------------------------------------------------

class ProfileIn(BaseModel):
    name: str = ""
    headline: str = ""
    bio: str = ""
    skills: List[str] = []
    location: str = ""
    github: str = ""
    linkedin: str = ""
    contact_email: str = ""
    availability: str = "Open to work"


class ProfileOut(ProfileIn):
    user_id: int


# ---------------------------------------------------------------------------
# Resume
# ---------------------------------------------------------------------------

class ResumeMeta(BaseModel):
    filename: str            # stored (safe) filename on disk
    original_filename: str   # name the user uploaded
    url: str                 # path/URL the frontend can use
    upload_date: str
    file_type: str
    file_size: int           # bytes


# ---------------------------------------------------------------------------
# Projects
# ---------------------------------------------------------------------------

class ProjectIn(BaseModel):
    title: str
    summary: str = ""
    description: str = ""
    content: str = ""             # rich text / Markdown content
    tech_stack: List[str] = []
    github_link: str = ""
    demo_link: str = ""
    status: str = "Draft"         # Draft / Published
    featured: bool = False
    collaborators: List[str] = []  # placeholder list for now


class ProjectOut(ProjectIn):
    id: int
    owner_id: int


class ProjectContentIn(BaseModel):
    # Rich text / Markdown saved as a plain string. Structure is ready for
    # validation/sanitization later, but we do not sanitize yet.
    content: str = ""


# ---------------------------------------------------------------------------
# Project images
# ---------------------------------------------------------------------------

class ImageMeta(BaseModel):
    id: int
    project_id: int
    filename: str
    original_filename: str
    url: str
    upload_date: str
    file_type: str
    file_size: int


# ---------------------------------------------------------------------------
# Share links
# ---------------------------------------------------------------------------

class ShareLinkIn(BaseModel):
    # Placeholders for now -- not enforced yet.
    visibility: str = "public"
    expires_at: Optional[str] = None


class ShareLinkOut(BaseModel):
    token: str
    url: str
    visibility: str
    expires_at: Optional[str] = None


class ShareSettingsIn(BaseModel):
    visibility: Optional[str] = None
    expires_at: Optional[str] = None


# ---------------------------------------------------------------------------
# Review workflow
# ---------------------------------------------------------------------------

# Allowed review statuses: Draft / Needs Revision / Ready / Published

class ReviewSubmit(BaseModel):
    # Optional message a student can send along with the submission.
    message: str = ""


class ReviewFeedbackItem(BaseModel):
    reviewer: str
    status: str
    comment: str
    date: str


class ReviewStatusOut(BaseModel):
    status: str


class ReviewFeedbackOut(BaseModel):
    status: str
    feedback: List[ReviewFeedbackItem] = []
