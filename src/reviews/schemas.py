import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, conint

class ReviewModel(BaseModel):
    uid: uuid.UUID
    ratings: int = Field(ge=0, le=5)  # Required field with constraints
    review_text: str
    user_uid: Optional[uuid.UUID]
    book_uid: Optional[uuid.UUID]
    created_at: datetime
    updated_at: datetime  # Ensure this field is included

class ReviewCreateModel(BaseModel):
    ratings: int = Field(ge=0, le=5) 
    review_text: str