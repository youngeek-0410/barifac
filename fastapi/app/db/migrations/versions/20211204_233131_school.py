"""school

Revision ID: 16eef557209e
Revises: f1b4eca43331
Create Date: 2021-12-04 23:31:31.050280+09:00

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "16eef557209e"
down_revision = "f1b4eca43331"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "schools",
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
        sa.Column("name", sa.VARCHAR(length=100), nullable=False),
        sa.PrimaryKeyConstraint("uuid"),
        sa.UniqueConstraint("name"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("schools")
    # ### end Alembic commands ###
