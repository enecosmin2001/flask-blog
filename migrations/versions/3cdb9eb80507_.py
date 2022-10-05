"""empty message

Revision ID: 3cdb9eb80507
Revises: b39b13885a9b
Create Date: 2022-10-05 14:03:40.757255

"""

# revision identifiers, used by Alembic.
revision = "3cdb9eb80507"
down_revision = "b39b13885a9b"

import sqlalchemy as sa
from alembic import op


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("post", sa.Column("body_html", sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("post", "body_html")
    # ### end Alembic commands ###