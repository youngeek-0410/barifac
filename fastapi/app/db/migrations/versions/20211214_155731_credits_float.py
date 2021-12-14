"""credits_float

Revision ID: 4ebdcb256f71
Revises: 8c0541cd14bc
Create Date: 2021-12-14 15:57:31.412154+09:00

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "4ebdcb256f71"
down_revision = "8c0541cd14bc"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "subjects",
        "credits",
        existing_type=sa.INTEGER(),
        type_=sa.Float(),
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "subjects",
        "credits",
        existing_type=sa.Float(),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    # ### end Alembic commands ###
