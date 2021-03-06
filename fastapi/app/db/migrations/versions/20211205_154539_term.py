"""term

Revision ID: 22ac8b1f5d07
Revises: c94ea39e3603
Create Date: 2021-12-05 15:45:39.201974+09:00

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "22ac8b1f5d07"
down_revision = "c94ea39e3603"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "terms",
        sa.Column("uuid", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
            comment="登録日時",
        ),
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(timezone=True),
            nullable=True,
            comment="最終更新日時",
        ),
        sa.Column("academic_year", sa.Integer(), nullable=False),
        sa.Column("semester", sa.VARCHAR(length=10), nullable=False),
        sa.PrimaryKeyConstraint("uuid"),
        sa.UniqueConstraint("academic_year", "semester"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("terms")
    # ### end Alembic commands ###
