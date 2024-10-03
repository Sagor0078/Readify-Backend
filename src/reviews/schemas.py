from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid


class ReviewModel(BaseModel):
    uid: uuid.UUID
    ratings: int
    review_text: str
    user_uid: Optional[uuid.UUID]
    book_uid: Optional[uuid.UUID]
    created_at: datetime
    updated_at: datetime


class ReviewCreateModel:
    ratings: int = Field(lt=5)
    review_text: str
