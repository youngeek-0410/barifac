"""teacher

Revision ID: cce83fc74b50
Revises: de3f680d08e9
Create Date: 2021-12-05 15:58:27.525504+09:00

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "cce83fc74b50"
down_revision = "de3f680d08e9"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "teachers",
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
        sa.Column("school_uuid", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["school_uuid"],
            ["schools.uuid"],
        ),
        sa.PrimaryKeyConstraint("uuid"),
        sa.UniqueConstraint("name", "school_uuid"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("teachers")
    # ### end Alembic commands ###
