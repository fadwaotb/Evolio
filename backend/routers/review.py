"""
routers/review.py
-----------------
The portfolio review workflow. Student-only.

Statuses: Draft, Needs Revision, Ready, Published.
A student submits their portfolio (status -> Ready by default) and can read
their current status + any feedback a coach left.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import schemas
from auth_utils import require_student
from db import repository
from db.database import get_db
from db.model import ALLOWED_REVIEW_STATUSES

router = APIRouter(prefix="/api/review", tags=["review"])


@router.get("")
def get_review(db: Session = Depends(get_db), user=Depends(require_student)):
    return {
        "status": repository.get_review_status(db, user.id),
        "feedback": repository.get_review_feedback(db, user.id),
    }


@router.post("")
def submit_review(
    payload: schemas.ReviewRequest,
    db: Session = Depends(get_db),
    user=Depends(require_student),
):
    if payload.status not in ALLOWED_REVIEW_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Status must be one of: {', '.join(ALLOWED_REVIEW_STATUSES)}",
        )
    review = repository.submit_review(db, user.id, payload.status, payload.feedback)
    return {
        "status": review.status,
        "feedback": review.feedback,
        "submitted_at": review.submitted_at,
        "reviewed_at": review.reviewed_at,
    }
