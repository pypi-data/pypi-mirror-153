"""Add SimulationController uuid to SimulationInstance

Revision ID: e8749417b866
Revises: 728eceef1424
Create Date: 2020-11-27 02:54:41.312500

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e8749417b866"
down_revision = "728eceef1424"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "simulation_instances",
        sa.Column("uuid", sa.VARCHAR(255), unique=True, index=True),
    )


def downgrade():
    op.drop_column("simulation_instances", "uuid")
