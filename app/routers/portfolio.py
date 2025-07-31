from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.models import Portfolio
from app.schemas.portfolio import PortfolioCreate, PortfolioOut
from app.auth.auth_bearer import get_current_user  # <-- JWT解出當前使用者
from app.models.user import User
from sqlalchemy.future import select

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])

@router.post("/", response_model=PortfolioOut)

async def add_portfolio(
    portfolio_data: PortfolioCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    new_portfolio = Portfolio(
        user_id=current_user.id,
        symbol=portfolio_data.symbol,
        amount=portfolio_data.amount
    )
    db.add(new_portfolio)
    await db.commit()
    await db.refresh(new_portfolio)
    return new_portfolio