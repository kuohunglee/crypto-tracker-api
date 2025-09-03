from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.models import Portfolio
from app.schemas.portfolio import PortfolioCreate, PortfolioOut, PortfolioUpdate, PortfolioBase
from app.auth.auth_bearer import get_current_user  # <-- JWT解出當前使用者
from app.models.user import User
from sqlalchemy.future import select
from fastapi import Path
from app.services.price_service import fetch_price

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

@router.get("/me", response_model=list[PortfolioOut])
async def get_my_portfolio(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Portfolio).where(Portfolio.user_id == current_user.id)
    )
    portfolios = result.scalars().all()
    return portfolios


@router.put("/{portfolio_id}", response_model=PortfolioOut)
async def update_portfolio(
    portfolio_id: int = Path(..., description="資產記錄的 ID"),
    update_data: PortfolioUpdate = Depends(),
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Portfolio).where(Portfolio.id == portfolio_id, Portfolio.user_id == current_user.id)
    )
    portfolio = result.scalar_one_or_none()
    if not portfolio:
        raise HTTPException(status_code=404, detail="資產紀錄不存在")

    portfolio.symbol = update_data.symbol
    portfolio.amount = update_data.amount

    await db.commit()
    await db.refresh(portfolio)
    return portfolio

@router.delete("/{portfolio_id}")
async def delete_portfolio(
    portfolio_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Portfolio).where(Portfolio.id == portfolio_id, Portfolio.user_id == current_user.id)
    )
    portfolio = result.scalar_one_or_none()
    if not portfolio:
        raise HTTPException(status_code=404, detail="資產紀錄不存在")

    await db.delete(portfolio)
    await db.commit()
    return {"msg": f"資產 ID {portfolio_id} 已成功刪除"}

@router.get("/summary")
async def get_portfolio_summary(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Portfolio).where(Portfolio.user_id == current_user.id)
    )
    portfolios = result.scalars().all()

    summary = []
    total_value = 0.0

    for item in portfolios:
        try:
            price = await fetch_price(item.symbol) # 獲取庫藏貨幣當前價格
            value = price * item.amount
            summary.append({
                "symbol": item.symbol,
                "amount": item.amount,
                "price": price,
                "value": round(value, 2)
            })
            total_value += value
        except Exception as e:
            continue  # 若某幣種查不到價格則略過

    return {
        "assets": summary,
        "total_value": round(total_value, 2)
    }