from sqlalchemy import Column, Integer, Float, String, Date
from app.database import Base
import datetime

class Price(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, nullable=False, index=True)
    date = Column(Date, default=datetime.date.today)
    price = Column(Float, nullable=False)