"""insert data

Revision ID: 1359d34f0928
Revises: 6e9940a7e1c9
Create Date: 2023-10-09 17:50:01.022313

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import json


# revision identifiers, used by Alembic.
revision: str = '1359d34f0928'
down_revision: Union[str, None] = '6e9940a7e1c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

users_table = sa.table(
    "users",
    sa.column("id", sa.Integer),
    sa.column("username", sa.String),
    sa.column("hashed_password", sa.String),
)

authors_table = sa.table(
    "authors",
    sa.column("id", sa.Integer),
    sa.column("name", sa.String),
)

books_table = sa.table(
    "books",
    sa.column("id", sa.Integer),
    sa.column("name", sa.String),
    sa.column("number_page", sa.String),
    sa.column("author_id", sa.Integer),
)

def upgrade() -> None:
    f = open('data.json')
    data = json.load(f)
    op.bulk_insert(
        users_table,
        data["users"]
    )
    op.bulk_insert(
        authors_table,
        data["authors"]
    )
    op.bulk_insert(
        books_table,
        data["books"]
    )


def downgrade() -> None:
    pass
