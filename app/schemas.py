from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class ReviewRequest(BaseModel):
    code: str = Field(..., min_length=1)
    language: str

    class Config:
        json_schema_extra = {
            "example": {
                "code": "def add(a, b):\n    return a + b",
                "language": "python"
            }
        }


class Bug(BaseModel):
    line_number: int
    description: str
    severity: str  # low / medium / high


class SecurityIssue(BaseModel):
    description: str
    severity: str
    recommendation: str


class Complexity(BaseModel):
    time_complexity: str
    space_complexity: str
    explanation: str


class CodeReview(BaseModel):
    quality_score: int = Field(ge=1, le=10)
    summary: str
    bugs: List[Bug]
    security_issues: List[SecurityIssue]
    suggestions: List[str]
    complexity: Complexity
    rewritten_code: str


class ReviewResponse(BaseModel):
    id: int
    language: str
    review: CodeReview
    created_at: datetime

    class Config:
        from_attributes = True


class HistoryItem(BaseModel):
    id: int
    language: str
    quality_score: int
    summary: str
    created_at: datetime
