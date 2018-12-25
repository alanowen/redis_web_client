"""empty message

Revision ID: 73c754bbc5ac
Revises: 
Create Date: 2018-12-24 16:47:13.808567

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73c754bbc5ac'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('redis_server_connections',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('connection_name', sa.String(length=50), nullable=False),
    sa.Column('host', sa.String(length=128), nullable=False),
    sa.Column('port', sa.Integer(), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('redis_server_connections')
    op.drop_table('users')
    # ### end Alembic commands ###