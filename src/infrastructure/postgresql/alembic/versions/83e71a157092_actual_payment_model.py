"""actual payment model

Revision ID: 83e71a157092
Revises: 0d514dc5a8b7
Create Date: 2023-08-22 00:33:43.740866

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "83e71a157092"
down_revision = "0d514dc5a8b7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "payment",
        sa.Column("order_uuid", sa.UUID(), nullable=True),
        sa.Column(
            "status",
            sa.Enum("PENDING", "PAID", "REFUSED", name="paymentstatus"),
            nullable=False,
        ),
        sa.Column("uuid", sa.UUID(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["order_uuid"],
            ["order.uuid"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_payment_status"), "payment", ["status"], unique=False)
    op.create_index(op.f("ix_payment_uuid"), "payment", ["uuid"], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_payment_uuid"), table_name="payment")
    op.drop_index(op.f("ix_payment_status"), table_name="payment")
    op.drop_table("payment")
    # ### end Alembic commands ###