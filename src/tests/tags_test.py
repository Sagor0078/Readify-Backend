import uuid
from datetime import datetime
from pydantic import ValidationError
import pytest
from src.tags.schemas import TagModel, TagCreateModel, TagAddModel

def test_tag_model():
    tag = TagModel(
        uid=uuid.uuid4(),
        name="Test Tag",
        created_at=datetime.utcnow()
    )
    assert tag.name == "Test Tag"
    assert isinstance(tag.uid, uuid.UUID)
    assert isinstance(tag.created_at, datetime)

def test_tag_create_model():
    tag_create = TagCreateModel(name="New Tag")
    assert tag_create.name == "New Tag"

def test_tag_add_model():
    tag_create = TagCreateModel(name="New Tag")
    tag_add = TagAddModel(tags=[tag_create])
    assert len(tag_add.tags) == 1
    assert tag_add.tags[0].name == "New Tag"

def test_tag_model_validation_error():
    with pytest.raises(ValidationError):
        TagModel(
            uid="invalid-uuid",
            name="Test Tag",
            created_at="invalid-datetime"
        )

def test_tag_create_model_validation_error():
    with pytest.raises(ValidationError):
        TagCreateModel(name=123)

def test_tag_add_model_validation_error():
    with pytest.raises(ValidationError):
        TagAddModel(tags="invalid-tags")