"""create press_releases tables

Revision ID: 920778b16a15
Revises: 
Create Date: 2025-09-19 07:29:51.283070

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '920778b16a15'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'press_releases',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('url', sa.Text, nullable=False),
        sa.Column('url_hash', sa.String(64), nullable=False, unique=True, index=True),
        sa.Column('title', sa.Text),
        sa.Column('published_at', sa.DateTime),
        sa.Column('raw_payload', sa.JSON),
        sa.Column('last_seen_at', sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        'press_release_summary',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('press_release_id', sa.Integer, sa.ForeignKey('press_releases.id', ondelete='CASCADE')),
        sa.Column('summary', sa.Text),
        sa.Column('bullets', sa.JSON),
        sa.Column('model_name', sa.Text),
        sa.Column('status', sa.Text, server_default='pending'),
        sa.Column('summarized_at', sa.DateTime),
    )


def downgrade():
    op.drop_table('press_release_summary')
    op.drop_table('press_releases')
