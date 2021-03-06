"""fix_department

Revision ID: de3f680d08e9
Revises: 22ac8b1f5d07
Create Date: 2021-12-05 15:50:03.260484+09:00

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "de3f680d08e9"
down_revision = "22ac8b1f5d07"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("departments_name_key", "departments", type_="unique")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint("departments_name_key", "departments", ["name"])
    # ### end Alembic commands ###
