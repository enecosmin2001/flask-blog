"""empty message

Revision ID: a0793151cc86
Revises: d2c4020eff16
Create Date: 2022-10-13 18:03:43.378189

"""

# revision identifiers, used by Alembic.
revision = "a0793151cc86"
down_revision = "d2c4020eff16"

import sqlalchemy as sa
from alembic import op


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "posts", sa.Column("image_path", sa.String(length=100), nullable=True)
    )
    op.add_column(
        "posts", sa.Column("text_to_image", sa.String(length=100), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("posts", "text_to_image")
    op.drop_column("posts", "image_path")
    # ### end Alembic commands ###
