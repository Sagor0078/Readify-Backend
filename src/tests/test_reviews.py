import uuid
from datetime import datetime
from pydantic import ValidationError
import pytest
from src.reviews.schemas import ReviewModel, ReviewCreateModel

def test_review_model():
    review = ReviewModel(
        uid=uuid.uuid4(),
        ratings=4,
        review_text="Great book!",
        user_uid=uuid.uuid4(),
        book_uid=uuid.uuid4(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    assert review.ratings == 4
    assert review.review_text == "Great book!"
    assert isinstance(review.uid, uuid.UUID)
    assert isinstance(review.user_uid, uuid.UUID)
    assert isinstance(review.book_uid, uuid.UUID)
    assert isinstance(review.created_at, datetime)
    assert isinstance(review.updated_at, datetime)

def test_review_create_model():
    review_create = ReviewCreateModel(
        ratings=5,
        review_text="Excellent read!"
    )
    assert review_create.ratings == 5
    assert review_create.review_text == "Excellent read!"

def test_review_model_validation_error():
    with pytest.raises(ValidationError):
        ReviewModel(
            uid="invalid-uuid",
            ratings=6,  # Invalid rating
            review_text="Great book!",
            user_uid="invalid-uuid",
            book_uid="invalid-uuid",
            created_at="invalid-datetime",
            updated_at="invalid-datetime"
        )

def test_review_create_model_validation_error():
    with pytest.raises(ValidationError):
        ReviewCreateModel(
            ratings=-1,  # Invalid rating
            review_text=123  # Invalid review_text
        )