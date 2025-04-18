"""tables groups and links

Revision ID: 2ebda6156680
Revises: 5a491502deb7
Create Date: 2025-03-02 20:14:43.534146

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2ebda6156680'
down_revision: Union[str, None] = '5a491502deb7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1
    op.create_table('links',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String, nullable=False, unique=True),
                    sa.Column('link', sa.String, nullable=False),
                    sa.Column('users', sa.String(), nullable=False),
                    sa.Column('priority', sa.Integer(), nullable=True),
                    sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now(),
                              nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.func.now(),
                              nullable=False, onupdate=sa.func.now()),
                    sa.PrimaryKeyConstraint('id')
                    )
    # 2
    op.create_table('groups',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String, nullable=False, unique=True),
                    sa.Column('users', sa.String(), nullable=False),
                    sa.Column('level', sa.String, nullable=True),
                    sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now(),
                              nullable=False),
                    sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.func.now(),
                              nullable=False, onupdate=sa.func.now()),
                    sa.PrimaryKeyConstraint('id')
                    )
    # 3
    with op.batch_alter_table('users') as batch_op:
        batch_op.alter_column('last_message_id', existing_type=sa.Text(), type_=sa.Integer(), nullable=True)


def downgrade() -> None:
    # 1
    op.drop_table('links')
    # 2
    op.drop_table('groups')
    # 3
    with op.batch_alter_table('users') as batch_op:
        batch_op.alter_column('last_message_id', existing_type=sa.Integer(), type_=sa.Text(), nullable=True)

