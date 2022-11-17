"""create tables

Revision ID: 1c9f089c313a
Revises: c928f3232350
Create Date: 2022-11-15 11:37:21.013195

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1c9f089c313a'
down_revision = 'c928f3232350'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subscription_cost',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('subscription_type', sa.Enum('month', 'three_months', 'year', name='subscriptiontypes'), nullable=False),
    sa.Column('cost', sa.Float(precision=2), nullable=False),
    sa.Column('creation_date', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('payments',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('subscription_type', sa.Enum('month', 'three_months', 'year', name='subscriptiontypes'), nullable=False),
    sa.Column('processing_status', sa.Enum('new', 'in_processing', 'processed', 'completed', 'duplicated', name='processingstatus'), nullable=True),
    sa.Column('payment_status', sa.Enum('accepted', 'error', 'rejected', 'unknown', name='paymentstatus'), nullable=True),
    sa.Column('payment_date', sa.DateTime(), nullable=False),
    sa.Column('payment_type', sa.Enum('payment', 'refund', name='paymentstypes'), nullable=False),
    sa.Column('expiration_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payments')
    op.drop_table('subscription_cost')
    # ### end Alembic commands ###