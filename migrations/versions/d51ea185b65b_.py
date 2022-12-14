"""empty message

Revision ID: d51ea185b65b
Revises: 29e7dfdaee8e
Create Date: 2022-10-03 14:37:26.139779

"""

# revision identifiers, used by Alembic.
revision = "d51ea185b65b"
down_revision = "29e7dfdaee8e"

import sqlalchemy as sa
from alembic import op


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("email", sa.String(length=64), nullable=True))
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_column("users", "email")
    # ### end Alembic commands ###
