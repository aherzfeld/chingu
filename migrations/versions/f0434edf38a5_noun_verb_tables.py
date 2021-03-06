"""Noun & Verb tables

Revision ID: f0434edf38a5
Revises: 9ed5b81fb12b
Create Date: 2019-02-06 18:04:46.183764

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0434edf38a5'
down_revision = '9ed5b81fb12b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('nouns',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('category', sa.String(), nullable=True),
    sa.Column('word', sa.String(), nullable=False),
    sa.Column('definition', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('word')
    )
    op.create_table('verbs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('category', sa.String(), nullable=True),
    sa.Column('word', sa.String(), nullable=False),
    sa.Column('definition', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('word')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('verbs')
    op.drop_table('nouns')
    # ### end Alembic commands ###
