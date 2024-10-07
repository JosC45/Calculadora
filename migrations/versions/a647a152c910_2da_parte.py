"""2da parte

Revision ID: a647a152c910
Revises: 0d443ae89a1a
Create Date: 2024-09-25 00:24:53.569766

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a647a152c910'
down_revision = '0d443ae89a1a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('partidos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('local_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('visitante_id', sa.Integer(), nullable=False))
        batch_op.drop_constraint('partidos_ibfk_1', type_='foreignkey')
        batch_op.drop_constraint('partidos_ibfk_2', type_='foreignkey')
        batch_op.create_foreign_key(None, 'seleccion', ['local_id'], ['id'])
        batch_op.create_foreign_key(None, 'seleccion', ['visitante_id'], ['id'])
        batch_op.drop_column('visitante')
        batch_op.drop_column('local')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('partidos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('local', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.add_column(sa.Column('visitante', mysql.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('partidos_ibfk_2', 'seleccion', ['visitante'], ['id'])
        batch_op.create_foreign_key('partidos_ibfk_1', 'seleccion', ['local'], ['id'])
        batch_op.drop_column('visitante_id')
        batch_op.drop_column('local_id')

    # ### end Alembic commands ###
