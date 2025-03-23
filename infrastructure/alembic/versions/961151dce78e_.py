"""empty message

Revision ID: 961151dce78e
Revises: f5e6a0ca8aa5
Create Date: 2024-10-28 18:59:32.920748

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "961151dce78e"
down_revision = "f5e6a0ca8aa5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "order",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("customer_id", sa.Integer(), nullable=True),
        sa.Column("created", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["customer_id"],
            ["customer.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_order_id"), "order", ["id"], unique=False)
    op.create_table(
        "order_items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=True),
        sa.Column("product_id", sa.Integer(), nullable=True),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["order_id"],
            ["order.id"],
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["product.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_order_items_id"), "order_items", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_order_items_id"), table_name="order_items")
    op.drop_table("order_items")
    op.drop_index(op.f("ix_order_id"), table_name="order")
    op.drop_table("order")
    # ### end Alembic commands ###
