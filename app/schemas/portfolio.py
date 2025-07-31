from pydantic import BaseModel

class PortfolioCreate(BaseModel):
    symbol: str
    amount: int

class PortfolioOut(BaseModel):
    id: int
    user_id: int
    symbol: str
    amount: int

    class Config:
        orm_mode = True