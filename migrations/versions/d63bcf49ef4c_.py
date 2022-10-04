"""empty message

Revision ID: d63bcf49ef4c
Revises: 2bac30da651f
Create Date: 2022-10-04 12:25:01.756307

"""

# revision identifiers, used by Alembic.
revision = "d63bcf49ef4c"
down_revision = "2bac30da651f"

import sqlalchemy as sa
from alembic import op


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("roles", sa.Column("default", sa.Boolean(), nullable=True))
    op.add_column("roles", sa.Column("permissions", sa.Integer(), nullable=True))
    op.create_index(op.f("ix_roles_default"), "roles", ["default"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_roles_default"), table_name="roles")
    op.drop_column("roles", "permissions")
    op.drop_column("roles", "default")
    # ### end Alembic commands ###
