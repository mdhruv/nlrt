"""empty message

Revision ID: 0d608908a6f9
Revises: 
Create Date: 2021-06-25 11:57:05.283022

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d608908a6f9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('raider',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('game_class', sa.String(length=64), nullable=True),
    sa.Column('role', sa.String(length=64), nullable=True),
    sa.Column('realm', sa.String(length=64), nullable=True),
    sa.Column('guild', sa.String(length=64), nullable=True),
    sa.Column('is_raid_leader', sa.Boolean(), nullable=True),
    sa.Column('profession1', sa.String(length=64), nullable=True),
    sa.Column('profession2', sa.String(length=64), nullable=True),
    sa.Column('has_cooking', sa.Boolean(), nullable=True),
    sa.Column('has_first_aid', sa.Boolean(), nullable=True),
    sa.Column('has_fishing', sa.Boolean(), nullable=True),
    sa.Column('alt_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['alt_id'], ['raider.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('realm', sa.String(length=64), nullable=True),
    sa.Column('guild', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('friend_table',
    sa.Column('left_friend_id', sa.Integer(), nullable=False),
    sa.Column('right_friend_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['left_friend_id'], ['raider.id'], ),
    sa.ForeignKeyConstraint(['right_friend_id'], ['raider.id'], ),
    sa.PrimaryKeyConstraint('left_friend_id', 'right_friend_id')
    )
    op.create_table('partner_table',
    sa.Column('left_partner_id', sa.Integer(), nullable=False),
    sa.Column('right_partner_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['left_partner_id'], ['raider.id'], ),
    sa.ForeignKeyConstraint(['right_partner_id'], ['raider.id'], ),
    sa.PrimaryKeyConstraint('left_partner_id', 'right_partner_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('partner_table')
    op.drop_table('friend_table')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('raider')
    # ### end Alembic commands ###
