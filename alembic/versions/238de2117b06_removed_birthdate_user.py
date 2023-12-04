"""removed birthdate (User)

Revision ID: 238de2117b06
Revises: aaff8baecb27
Create Date: 2023-12-04 21:10:56.236571

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '238de2117b06'
down_revision: Union[str, None] = 'aaff8baecb27'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'birth_date')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('birth_date', sa.DATETIME(), nullable=False))
    # ### end Alembic commands ###
