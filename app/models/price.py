from sqlalchemy import Column, Integer, Float, String, Date
from app.database import Base

class Price(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    price = Column(Float, nullable=False)