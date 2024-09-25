

from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
import uuid

class User(SQLModel, table = True):
    __tablename__ = 'users'

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            nullable=False,
            default=uuid.uuid4,
        )
    )
    username: str = Field(nullable=False)  # Use Field() for username
    email: str = Field(nullable=False)     # Use Field() for email
    first_name: str = Field(nullable=False) # Use Field() for first_name
    last_name: str = Field(nullable=False)  # Use Field() for last_name
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    

    def __repr__(self):
        return f"<User {self.username}>"