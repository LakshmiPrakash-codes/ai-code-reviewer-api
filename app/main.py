import anthropic as anthropic_sdk
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from .database import engine, get_db
from . import models, schemas, crud
from .reviewer import review_code

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Code Reviewer API",
    description="Submit Python, JavaScript, or SQL code for an AI-powered review.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SUPPORTED_LANGUAGES = {"python", "javascript", "sql"}


@app.get("/health", tags=["System"])
def health_check():
    return {"status": "healthy"}


@app.post("/review", response_model=schemas.ReviewResponse, tags=["Review"])
def submit_review(request: schemas.ReviewRequest, db: Session = Depends(get_db)):
    language = request.language.lower().strip()

    if language not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language. Supported: {', '.join(sorted(SUPPORTED_LANGUAGES))}",
        )

    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty.")

    try:
        review = review_code(request.code, language)
    except anthropic_sdk.APIStatusError as e:
        raise HTTPException(status_code=502, detail=f"AI service error: {e.message}")
    except anthropic_sdk.APIConnectionError:
        raise HTTPException(status_code=503, detail="Could not reach AI service, try again.")
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    db_submission = crud.create_review(
        db=db, code=request.code, language=language, review=review
    )

    return schemas.ReviewResponse(
        id=db_submission.id,
        language=db_submission.language,
        review=review,
        created_at=db_submission.created_at,
    )


@app.get("/history", response_model=List[schemas.HistoryItem], tags=["History"])
def get_history(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    submissions = crud.get_reviews(db, skip=skip, limit=limit)
    return [
        schemas.HistoryItem(
            id=s.id,
            language=s.language,
            quality_score=s.review["quality_score"],
            summary=s.review["summary"],
            created_at=s.created_at,
        )
        for s in submissions
    ]


@app.get("/history/{review_id}", response_model=schemas.ReviewResponse, tags=["History"])
def get_review_detail(review_id: int, db: Session = Depends(get_db)):
    submission = crud.get_review_by_id(db, review_id)
    if submission is None:
        raise HTTPException(status_code=404, detail=f"Review {review_id} not found.")

    return schemas.ReviewResponse(
        id=submission.id,
        language=submission.language,
        review=schemas.CodeReview(**submission.review),
        created_at=submission.created_at,
    )
