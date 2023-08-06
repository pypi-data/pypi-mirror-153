"""Add experiment name

Revision ID: 728eceef1424
Revises: 158c30d6a4bf
Create Date: 2020-11-26 20:31:17.452703

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "728eceef1424"
down_revision = "158c30d6a4bf"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "experiments",
        sa.Column("name", sa.VARCHAR(255), unique=True, index=True),
    )


def downgrade():
    op.drop_column("experiments", "name")
