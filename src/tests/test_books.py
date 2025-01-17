import uuid
from datetime import date, datetime
from pydantic import ValidationError
import pytest
from src.books.schemas import Book, BookDetailModel
from src.reviews.schemas import ReviewModel
from src.tags.schemas import TagModel

def test_book_model():
    book = Book(
        uid=uuid.uuid4(),
        title="Sample Book",
        author="Author Name",
        publisher="Publisher Name",
        published_date=date.today(),
        page_count=300,
        language="English",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    assert book.title == "Sample Book"
    assert book.author == "Author Name"
    assert isinstance(book.uid, uuid.UUID)
    assert isinstance(book.published_date, date)
    assert isinstance(book.created_at, datetime)
    assert isinstance(book.updated_at, datetime)

def test_book_detail_model():
    review = ReviewModel(
        uid=uuid.uuid4(),
        ratings=4,
        review_text="Great book!",
        user_uid=uuid.uuid4(),
        book_uid=uuid.uuid4(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    tag = TagModel(
        uid=uuid.uuid4(),
        name="Fiction",
        created_at=datetime.utcnow()
    )
    book_detail = BookDetailModel(
        uid=uuid.uuid4(),
        title="Sample Book",
        author="Author Name",
        publisher="Publisher Name",
        published_date=date.today(),
        page_count=300,
        language="English",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        reviews=[review],
        tags=[tag]
    )
    assert book_detail.title == "Sample Book"
    assert book_detail.reviews[0].review_text == "Great book!"
    assert book_detail.tags[0].name == "Fiction"

def test_book_model_validation_error():
    with pytest.raises(ValidationError):
        Book(
            uid="invalid-uuid",
            title="Sample Book",
            author="Author Name",
            publisher="Publisher Name",
            published_date="invalid-date",
            page_count="invalid-page-count",
            language="English",
            created_at="invalid-datetime",
            updated_at="invalid-datetime"
        )

def test_book_detail_model_validation_error():
    with pytest.raises(ValidationError):
        BookDetailModel(
            uid="invalid-uuid",
            title="Sample Book",
            author="Author Name",
            publisher="Publisher Name",
            published_date="invalid-date",
            page_count="invalid-page-count",
            language="English",
            created_at="invalid-datetime",
            updated_at="invalid-datetime",
            reviews="invalid-reviews",
            tags="invalid-tags"
        )