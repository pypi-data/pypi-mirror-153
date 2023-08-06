"""reward to table muscle_action

Revision ID: 158c30d6a4bf
Revises: f29bac335186
Create Date: 2020-11-26 14:13:42.943147

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "158c30d6a4bf"
down_revision = "f29bac335186"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("muscle_actions", sa.Column("reward", sa.FLOAT))


def downgrade():
    op.drop_column("muscle_actions", "reward")
