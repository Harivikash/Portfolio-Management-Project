# models.py
from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    side = Column(String, index=True)
    symbol = Column(String, index=True)
    fill_qty = Column(Float)
    fill_price = Column(Float)
    fill_amount = Column(Float)
    fill_time = Column(DateTime, index=True)
    markets = Column(String)
    currency = Column(String)
    total_fees = Column(Float)

