from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
)
from datetime import datetime

from ...database import Base


class CompanyTickerOutboxModel(Base):
    __tablename__ = 'company_ticker_outbox'

    id = Column(Integer, primary_key=True)
    type = Column(String(10), nullable=False)
    cik_str = Column(String(128), nullable=False)
    ticker = Column(String(20), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    exchange = Column(String(50), nullable=True)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
