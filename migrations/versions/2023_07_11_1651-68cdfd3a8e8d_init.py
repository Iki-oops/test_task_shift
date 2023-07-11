"""init

Revision ID: 68cdfd3a8e8d
Revises: cc4c9fb96066
Create Date: 2023-07-11 16:51:06.633824

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '68cdfd3a8e8d'
down_revision = 'cc4c9fb96066'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_employee_progression_id', table_name='employee_progression')
    op.drop_table('employee_progression')
    op.drop_index('ix_employee_position_level_id', table_name='employee_position_level')
    op.drop_table('employee_position_level')
    op.drop_index('ix_employee_email', table_name='employee')
    op.drop_index('ix_employee_id', table_name='employee')
    op.drop_table('employee')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('employee',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(length=320), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=320), autoincrement=False, nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=320), autoincrement=False, nullable=False),
    sa.Column('last_name', sa.VARCHAR(length=320), autoincrement=False, nullable=False),
    sa.Column('hashed_password', sa.VARCHAR(length=1024), autoincrement=False, nullable=False),
    sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('is_superuser', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('is_verified', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('progression_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['progression_id'], ['employee_progression.id'], name='employee_progression_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='employee_pkey'),
    sa.UniqueConstraint('username', name='employee_username_key')
    )
    op.create_index('ix_employee_id', 'employee', ['id'], unique=False)
    op.create_index('ix_employee_email', 'employee', ['email'], unique=False)
    op.create_table('employee_position_level',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('employee_position_level_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('position_level', sa.VARCHAR(length=320), autoincrement=False, nullable=False),
    sa.Column('min_salary', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('max_salary', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='employee_position_level_pkey'),
    sa.UniqueConstraint('position_level', name='employee_position_level_position_level_key'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_employee_position_level_id', 'employee_position_level', ['id'], unique=False)
    op.create_table('employee_progression',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('current_position_level_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('current_position_date', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=False),
    sa.Column('salary', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('promotion_position_level_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('promotion_position_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['current_position_level_id'], ['employee_position_level.id'], name='employee_progression_current_position_level_id_fkey'),
    sa.ForeignKeyConstraint(['promotion_position_level_id'], ['employee_position_level.id'], name='employee_progression_promotion_position_level_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='employee_progression_pkey')
    )
    op.create_index('ix_employee_progression_id', 'employee_progression', ['id'], unique=False)
    # ### end Alembic commands ###