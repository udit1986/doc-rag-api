# SQL Alchemy models declaration.
# https://docs.sqlalchemy.org/en/20/orm/quickstart.html#declare-models
# mapped_column syntax from SQLAlchemy 2.0.

# https://alembic.sqlalchemy.org/en/latest/tutorial.html
# Note, it is used by alembic migrations logic, see `alembic/env.py`

# Alembic shortcuts:
# # create migration
# alembic revision --autogenerate -m "migration_name"

# # apply all migrations
# alembic upgrade head


import uuid
from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, String, Uuid, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    create_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    update_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Document(Base):
    __tablename__ = 'documents'

    id = Mapped[int] = mapped_column(BigInteger, primary_key=True)
    file_location: Mapped[str] = mapped_column(
        String(512), nullable=True
    )
    content = Column(String, nullable=False)
    embedding_present: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    embeddings: Mapped[Float] = mapped_column(Float, nullable=False)
    
    def __repr__(self):
        return f"<Document(id={self.id}, content={self.content[:20]}, embeddings={self.embeddings})>"
