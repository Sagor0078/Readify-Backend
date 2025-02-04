from src.db.main import get_session
from src.auth.dependencies import AccessTokenBearer, RoleChecker,RefreshTokenBearer
from src.tags.schemas import TagModel, TagCreateModel, TagAddModel
from src.reviews.schemas import ReviewModel, ReviewCreateModel
from src.books.schemas import Book, BookDetailModel
from src.db.models import Book
from src import app
from fastapi.testclient import TestClient
from datetime import datetime
from unittest.mock import Mock
from pydantic import ValidationError
import pytest
import uuid


mock_session = Mock()
mock_user_service = Mock()
mock_book_service =Mock()

def get_mock_session():
    yield mock_session


access_token_bearer = AccessTokenBearer()
refresh_token_bearer = RefreshTokenBearer()
role_checker = RoleChecker(['admin'])

app.dependency_overrides[get_session] = get_mock_session
app.dependency_overrides[role_checker] = Mock()
app.dependency_overrides[refresh_token_bearer]= Mock()


@pytest.fixture
def fake_session():
    return mock_session


@pytest.fixture
def fake_user_service():
    return mock_user_service


@pytest.fixture
def fake_book_service():
    return mock_book_service

@pytest.fixture
def test_client():
    return TestClient(app)

@pytest.fixture
def test_book():
    return Book(
        uid=uuid.uuid4(),
        user_uid=uuid.uuid4(),
        title="sample title",
        description="sample description",
        page_count=200,
        language="English",
        published_date=datetime.now(),
        update_at=datetime.now()
    )

@pytest.fixture
def test_tag_model():
    return TagModel(
        uid=uuid.uuid4(),
        name="Test Tag",
        created_at=datetime.utcnow()
    )

@pytest.fixture
def test_tag_create_model():
    return TagCreateModel(name="New Tag")

@pytest.fixture
def test_tag_add_model(test_tag_create_model):
    return TagAddModel(tags=[test_tag_create_model])

@pytest.fixture
def test_review_model():
    return ReviewModel(
        uid=uuid.uuid4(),
        ratings=4,
        review_text="Great book!",
        user_uid=uuid.uuid4(),
        book_uid=uuid.uuid4(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

@pytest.fixture
def test_review_create_model():
    return ReviewCreateModel(
        ratings=5,
        review_text="Excellent read!"
    )

@pytest.fixture
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
@pytest.fixture
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

@pytest.fixture
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

@pytest.fixture
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