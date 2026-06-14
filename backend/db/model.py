"""
model.py
--------
These Python classes describe the TABLES in our database.

Beginner notes:
- Each class = one table.
- Each Column = one column in that table.
- ForeignKey = "this column points at a row in another table".
- relationship() = a convenient Python link so you can write
  `user.projects` instead of writing a SQL JOIN by hand.

Cascade delete (cascade="all, delete-orphan"):
  When you delete a parent row, its children are deleted too.
  Example: delete a User -> their profile, resume, projects, share links,
  and reviews are all deleted automatically.

JSON string fields:
  SQLite has no real "list" column, so for now we store lists (like skills)
  as a JSON TEXT string, e.g. '["React", "Python"]'. The router code converts
  between a Python list and this string.
"""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from db.database import Base


# The four roles allowed in the platform.
ALLOWED_ROLES = ["Student", "Employer", "Admin", "Career Coach"]

# The four review statuses allowed by the project spec.
ALLOWED_REVIEW_STATUSES = ["Draft", "Needs Revision", "Ready", "Published"]


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(String, nullable=False, default="Student")

    # Simple login token. When a user logs in we store a random token here and
    # the frontend sends it back on every request (Authorization: Bearer <token>).
    auth_token = Column(String, index=True, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # --- Relationships (one User has these children) ---
    profile = relationship(
        "StudentProfile",
        back_populates="user",
        uselist=False,                       # one profile per user
        cascade="all, delete-orphan",
    )
    resume = relationship(
        "Resume",
        back_populates="user",
        uselist=False,                       # one resume per user
        cascade="all, delete-orphan",
    )
    projects = relationship(
        "Project",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    share_links = relationship(
        "ShareLink",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    reviews = relationship(
        "PortfolioReview",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,                         # one profile per user
        nullable=False,
        index=True,
    )

    headline = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    location = Column(String, nullable=True)
    target_roles = Column(String, nullable=True)
    contact_email = Column(String, nullable=True)
    avatar_color = Column(String, nullable=True)
    availability = Column(String, nullable=True)   # e.g. "Open to work"

    # List-like field stored as a JSON string, e.g. '["React","Python"]'
    skills_json = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="profile")
    social_links = relationship(
        "SocialLink",
        back_populates="profile",
        cascade="all, delete-orphan",
    )


class SocialLink(Base):
    __tablename__ = "social_links"

    id = Column(Integer, primary_key=True, index=True)
    student_profile_id = Column(
        Integer,
        ForeignKey("student_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    type = Column(String, nullable=True)     # e.g. "LinkedIn", "GitHub"
    url = Column(String, nullable=False)
    label = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    profile = relationship("StudentProfile", back_populates="social_links")


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,                         # one resume per user
        nullable=False,
        index=True,
    )

    # We store only METADATA here. The actual PDF/Word file lives on disk in
    # backend/uploads/resumes/. file_path points to it.
    original_name = Column(String, nullable=False)   # what the user named it
    stored_name = Column(String, nullable=False)     # unique name on disk
    file_path = Column(String, nullable=False)       # full path on disk
    content_type = Column(String, nullable=True)     # e.g. application/pdf
    size_bytes = Column(Integer, nullable=True)

    uploaded_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="resume")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title = Column(String, nullable=False)
    summary = Column(String, nullable=True)
    description = Column(Text, nullable=True)        # the Markdown / rich text body
    role = Column(String, nullable=True)
    duration = Column(String, nullable=True)
    github_link = Column(String, nullable=True)
    demo_link = Column(String, nullable=True)
    results = Column(Text, nullable=True)
    status = Column(String, nullable=False, default="Draft")   # "Draft" or "Published"

    # List-like fields stored as JSON strings.
    tech_stack_json = Column(Text, nullable=True)
    skills_json = Column(Text, nullable=True)
    collaborators_json = Column(Text, nullable=True)

    is_featured = Column(Boolean, default=False)
    sort_order = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="projects")
    images = relationship(
        "ProjectImage",
        back_populates="project",
        cascade="all, delete-orphan",
    )


class ProjectImage(Base):
    __tablename__ = "project_images"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    original_name = Column(String, nullable=False)
    stored_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    content_type = Column(String, nullable=True)
    size_bytes = Column(Integer, nullable=True)
    caption = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="images")


class ShareLink(Base):
    __tablename__ = "share_links"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    token = Column(String, unique=True, index=True, nullable=False)
    visibility = Column(String, default="private")   # "public" or "private"
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="share_links")


class PortfolioReview(Base):
    __tablename__ = "portfolio_reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # One of ALLOWED_REVIEW_STATUSES. Defaults to "Draft".
    status = Column(String, nullable=False, default="Draft")
    feedback = Column(Text, nullable=True)

    submitted_at = Column(DateTime, nullable=True)   # set when student submits
    reviewed_at = Column(DateTime, nullable=True)    # set when a coach reviews

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="reviews")
