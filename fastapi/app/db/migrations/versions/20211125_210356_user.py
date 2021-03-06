"""user

Revision ID: f1b4eca43331
Revises: 
Create Date: 2021-11-25 21:03:56.931568+09:00

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "f1b4eca43331"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
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
        sa.Column("username", sa.VARCHAR(length=256), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("uid", sa.VARCHAR(length=128), nullable=True),
        sa.Column("hashed_password", sa.String(), nullable=True),
        sa.Column("is_admin", sa.BOOLEAN(), nullable=False),
        sa.Column("is_active", sa.BOOLEAN(), nullable=False),
        sa.PrimaryKeyConstraint("uuid"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users")
    # ### end Alembic commands ###
