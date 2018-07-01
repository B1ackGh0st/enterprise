"""empty message

Revision ID: 4a0ad0417c24
Revises: f4c20716c888
Create Date: 2018-06-20 16:15:00.199517

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a0ad0417c24'
down_revision = 'f4c20716c888'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('defect', 'eliminated',
               existing_type=sa.INTEGER(),
               nullable=False,
               existing_server_default=sa.text('0'))
    op.alter_column('defect', 'taken_user_id',
               existing_type=sa.INTEGER(),
               nullable=False,
               existing_server_default=sa.text('1'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('defect', 'taken_user_id',
               existing_type=sa.INTEGER(),
               nullable=True,
               existing_server_default=sa.text('1'))
    op.alter_column('defect', 'eliminated',
               existing_type=sa.INTEGER(),
               nullable=True,
               existing_server_default=sa.text('0'))
    # ### end Alembic commands ###