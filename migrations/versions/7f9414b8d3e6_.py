"""empty message

Revision ID: 7f9414b8d3e6
Revises: 70b03670a709
Create Date: 2021-05-08 16:48:07.421402

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7f9414b8d3e6'
down_revision = '70b03670a709'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('partner_table',
    sa.Column('left_partner_id', sa.Integer(), nullable=False),
    sa.Column('right_partner_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['left_partner_id'], ['raider.id'], ),
    sa.ForeignKeyConstraint(['right_partner_id'], ['raider.id'], ),
    sa.PrimaryKeyConstraint('left_partner_id', 'right_partner_id')
    )
    op.drop_table('profession_table')
    op.drop_table('profession')
    op.add_column('raider', sa.Column('has_cooking', sa.Boolean(), nullable=True))
    op.add_column('raider', sa.Column('has_first_aid', sa.Boolean(), nullable=True))
    op.add_column('raider', sa.Column('has_fishing', sa.Boolean(), nullable=True))
    op.add_column('raider', sa.Column('is_raid_leader', sa.Boolean(), nullable=True))
    op.add_column('raider', sa.Column('profession1', sa.String(length=64), nullable=True))
    op.add_column('raider', sa.Column('profession2', sa.String(length=64), nullable=True))
    op.drop_constraint('raider_ibfk_1', 'raider', type_='foreignkey')
    op.drop_column('raider', 'partner_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('raider', sa.Column('partner_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key('raider_ibfk_1', 'raider', 'raider', ['partner_id'], ['id'])
    op.drop_column('raider', 'profession2')
    op.drop_column('raider', 'profession1')
    op.drop_column('raider', 'is_raid_leader')
    op.drop_column('raider', 'has_fishing')
    op.drop_column('raider', 'has_first_aid')
    op.drop_column('raider', 'has_cooking')
    op.create_table('profession',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('profession_table',
    sa.Column('raider_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('profession_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['profession_id'], ['profession.id'], name='profession_table_ibfk_1'),
    sa.ForeignKeyConstraint(['raider_id'], ['raider.id'], name='profession_table_ibfk_2'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.drop_table('partner_table')
    # ### end Alembic commands ###
