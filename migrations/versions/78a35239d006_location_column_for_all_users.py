"""location column for all users

Revision ID: 78a35239d006
Revises: 481ff51d08df
Create Date: 2023-01-25 11:24:59.709813

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78a35239d006'
down_revision = '481ff51d08df'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('location', geoalchemy2.types.Geometry(geometry_type='POINT', srid=4326, from_text='ST_GeomFromEWKT', name='geometry'), nullable=True))
        batch_op.create_index('idx_user_location', ['location'], unique=False, postgresql_using='gist')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index('idx_user_location', postgresql_using='gist')
        batch_op.drop_column('location')

    # ### end Alembic commands ###
