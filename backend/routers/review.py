"""
Review workflow routes.

A student submits their portfolio for review, checks the status, and reads
(mocked) reviewer feedback. Statuses: Draft / Needs Revision / Ready / Published.
"""

from datetime import datetime

from fastapi import APIRouter, Depends

from auth.auth import require_student
from db.database import reviews
from schemas import ReviewFeedbackOut, ReviewStatusOut, ReviewSubmit

router = APIRouter(prefix="/api/review", tags=["review"])


def _get_or_create_review(user_id: int) -> dict:
    review = reviews.get(user_id)
    if review is None:
        review = {"status": "Draft", "feedback": []}
        reviews[user_id] = review
    return review


@router.post("/submit", response_model=ReviewStatusOut)
def submit_review(data: ReviewSubmit, user=Depends(require_student)):
    review = _get_or_create_review(user["id"])
    # Submitting moves the portfolio into the review queue.
    review["status"] = "Ready"

    # Add a mocked reviewer reply so the frontend timeline has something to show.
    review["feedback"].append(
        {
            "reviewer": "Career Coach (mock)",
            "status": "Ready",
            "comment": "Thanks for submitting! Your portfolio is queued for review.",
            "date": datetime.utcnow().isoformat(),
        }
    )
    return ReviewStatusOut(status=review["status"])


@router.get("/status", response_model=ReviewStatusOut)
def get_review_status(user=Depends(require_student)):
    review = _get_or_create_review(user["id"])
    return ReviewStatusOut(status=review["status"])


@router.get("/feedback", response_model=ReviewFeedbackOut)
def get_review_feedback(user=Depends(require_student)):
    review = _get_or_create_review(user["id"])
    return ReviewFeedbackOut(status=review["status"], feedback=review["feedback"])
