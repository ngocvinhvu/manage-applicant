"""empty message

Revision ID: 36cbbd09b9ef
Revises: 
Create Date: 2022-08-10 11:03:21.826738

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '36cbbd09b9ef'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('applicants',
    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('created_dttm', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('dob', sa.DateTime(), nullable=True),
    sa.Column('country', postgresql.ENUM('VIETNAM', 'SINGAPORE', 'LAOS', 'INDONESIA', 'THAILAND', 'CAMPUCHIA', 'MALAYSIA', name='countries'), nullable=True),
    sa.Column('status', postgresql.ENUM('processed', 'pending', 'failed', name='status'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('applicants')
    # ### end Alembic commands ###