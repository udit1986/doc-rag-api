"""init documents

Revision ID: c79b0938ea4b
Revises:
Create Date: 2025-01-08 11:45:21.361225

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "c79b0938ea4b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "documents",
        sa.Column("id", sa.Uuid(as_uuid=False), nullable=False),
        sa.Column("file_location", sa.String(length=512), nullable=False),
        sa.Column("embedding_present", sa.Boolean(), nullable=False),
        sa.Column("embeddings", sa.Float(), nullable=False),
        sa.Column("content", sa.String(length=1024), nullable=False),
        sa.Column(
            "create_time",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "update_time",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("documents")
    # ### end Alembic commands ###
