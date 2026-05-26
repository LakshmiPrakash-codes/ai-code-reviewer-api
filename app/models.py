from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from .database import Base


class ReviewSubmission(Base):
    __tablename__ = "review_submissions"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(Text, nullable=False)
    language = Column(String(50), nullable=False)
    review = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
