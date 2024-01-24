"""New Migration

Revision ID: 4ec452e4e858
Revises: 
Create Date: 2024-01-17 16:32:35.153045

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4ec452e4e858'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('coordonnees',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('longitude', sa.REAL(), nullable=True),
    sa.Column('latitude', sa.REAL(), nullable=True),
    sa.Column('ip', sa.String(), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('coordonnees')
    # ### end Alembic commands ###