from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
)
from datetime import datetime

from ...database import Base


class NewswireFinancingOutboxModel(Base):
    __tablename__ = 'newswire_financing_outbox'

    id = Column(Integer, primary_key=True)
    news_id = Column(
        Integer,
        nullable=False,
        index=True,
    )
    source = Column(
        String(20),
        nullable=False,
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
