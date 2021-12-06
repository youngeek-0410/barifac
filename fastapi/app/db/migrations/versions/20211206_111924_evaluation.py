"""evaluation

Revision ID: aec7a6411b64
Revises: e3d4dbe0fe8c
Create Date: 2021-12-06 11:19:24.665321+09:00

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "aec7a6411b64"
down_revision = "e3d4dbe0fe8c"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "evaluations",
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
        sa.Column("subject_uuid", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("rate", sa.Integer(), nullable=False),
        sa.Column("type", sa.VARCHAR(length=20), nullable=False),
        sa.ForeignKeyConstraint(
            ["subject_uuid"],
            ["subjects.uuid"],
        ),
        sa.PrimaryKeyConstraint("uuid"),
        sa.UniqueConstraint("name", "subject_uuid"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("evaluations")
    # ### end Alembic commands ###