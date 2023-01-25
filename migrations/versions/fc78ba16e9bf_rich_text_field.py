"""rich text field

Revision ID: fc78ba16e9bf
Revises: c7548fa154e7
Create Date: 2023-01-25 14:00:45.875017

"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2


# revision identifiers, used by Alembic.
revision = 'fc78ba16e9bf'
down_revision = 'c7548fa154e7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products_for_sale', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description_html', sa.String(length=300), nullable=True))
        batch_op.alter_column('description',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.String(length=300),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products_for_sale', schema=None) as batch_op:
        batch_op.alter_column('description',
               existing_type=sa.String(length=300),
               type_=sa.VARCHAR(length=64),
               existing_nullable=False)
        batch_op.drop_column('description_html')

    # ### end Alembic commands ###
