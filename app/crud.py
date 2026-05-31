from sqlalchemy.orm import Session
from . import models
from .schemas import CodeReview


def create_review(db: Session, code: str, language: str, review: CodeReview) -> models.ReviewSubmission:
    db_review = models.ReviewSubmission(
        code=code,
        language=language,
        review=review.model_dump(),
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def get_reviews(db: Session, skip: int = 0, limit: int = 50) -> list[models.ReviewSubmission]:
    return (
        db.query(models.ReviewSubmission)
        .order_by(models.ReviewSubmission.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_review_by_id(db: Session, review_id: int) -> models.ReviewSubmission | None:
    return (
        db.query(models.ReviewSubmission)
        .filter(models.ReviewSubmission.id == review_id)
        .first()
    )
