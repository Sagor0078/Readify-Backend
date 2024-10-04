"""add_tags_and_Tag

Revision ID: 55f3b33f14d3
Revises: ebd9b8a2e883
Create Date: 2024-10-04 16:01:06.769444

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '55f3b33f14d3'
down_revision: Union[str, None] = 'ebd9b8a2e883'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tags',
    sa.Column('uid', sa.UUID(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_table('booktag',
    sa.Column('book_id', sa.Uuid(), nullable=False),
    sa.Column('tag_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['books.uid'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.uid'], ),
    sa.PrimaryKeyConstraint('book_id', 'tag_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('booktag')
    op.drop_table('tags')
    # ### end Alembic commands ###
