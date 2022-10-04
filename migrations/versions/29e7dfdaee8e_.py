"""empty message

Revision ID: 29e7dfdaee8e
Revises: 38c4e85512a9
Create Date: 2022-10-03 13:57:05.409931

"""

# revision identifiers, used by Alembic.
revision = "29e7dfdaee8e"
down_revision = "38c4e85512a9"

import sqlalchemy as sa
from alembic import op


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users", sa.Column("password_hash", sa.String(length=128), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "password_hash")
    # ### end Alembic commands ###