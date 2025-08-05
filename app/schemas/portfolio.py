from pydantic import BaseModel

class PortfolioBase(BaseModel):
    symbol: str
    amount: float

class PortfolioCreate(PortfolioBase):
    user_id: int
    symbol: str
    amount: int
    
class PortfolioUpdate(PortfolioBase):
    symbol: str
    amount: int

class PortfolioOut(BaseModel):
    id: int
    user_id: int
    symbol: str
    amount: int

    class Config:
        orm_mode = True