"""
schemas.py
----------
Pydantic models describe the SHAPE of the JSON that goes in and out of the API.

Beginner notes:
- "Request" schemas validate the JSON a client sends us (e.g. register form).
- "Response" schemas describe the JSON we send back.
- FastAPI uses these automatically: bad input -> a clear 422 error for free.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr


# ===========================================================================
# AUTH
# ===========================================================================
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    role: str = "Student"          # Student / Employer / Admin / Career Coach


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    role: str

    class Config:
        from_attributes = True     # let it read straight from a SQLAlchemy row


class AuthResponse(BaseModel):
    token: str
    user: UserOut


# ===========================================================================
# PROFILE
# ===========================================================================
class ProfileRequest(BaseModel):
    full_name: Optional[str] = None        # lives on the User, saved here for convenience
    headline: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    target_roles: Optional[str] = None
    contact_email: Optional[str] = None
    avatar_color: Optional[str] = None
    availability: Optional[str] = None
    skills: Optional[List[str]] = None
    github: Optional[str] = None           # stored as a social link of type "GitHub"
    linkedin: Optional[str] = None         # stored as a social link of type "LinkedIn"


class SocialLinkRequest(BaseModel):
    type: Optional[str] = None
    url: str
    label: Optional[str] = None


# ===========================================================================
# PROJECTS
# ===========================================================================
class ProjectRequest(BaseModel):
    title: str
    summary: Optional[str] = None
    description: Optional[str] = None
    role: Optional[str] = None
    duration: Optional[str] = None
    github_link: Optional[str] = None
    demo_link: Optional[str] = None
    results: Optional[str] = None
    tech_stack: Optional[List[str]] = None
    skills: Optional[List[str]] = None
    collaborators: Optional[List[str]] = None
    status: Optional[str] = None            # "Draft" or "Published"
    is_featured: Optional[bool] = None
    sort_order: Optional[int] = None


class ProjectContentRequest(BaseModel):
    content: str                   # the Markdown / rich-text body


# ===========================================================================
# SHARE LINKS
# ===========================================================================
class ShareLinkRequest(BaseModel):
    visibility: str = "private"    # "public" or "private"


class ShareSettingsRequest(BaseModel):
    visibility: Optional[str] = None
    is_active: Optional[bool] = None
    expires_at: Optional[datetime] = None


# ===========================================================================
# REVIEW
# ===========================================================================
class ReviewRequest(BaseModel):
    status: str = "Ready"          # one of the allowed review statuses
    feedback: Optional[str] = None
