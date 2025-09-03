from fastapi import APIRouter, HTTPException
from app.services.price_service import fetch_price
from app.services.snapshot_service import save_price_snapshot
from app.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.models.price import Price
from sqlalchemy.future import select

router = APIRouter(prefix="/price", tags=["Price"])

@router.get("/{symbol}")
async def get_current_price(symbol: str):
    try:
        price = await fetch_price(symbol)
        return {"symbol": symbol, "price": price}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e: 
        raise HTTPException(status_code=500, detail="取得幣價失敗") from e
    
@router.get("/snapshot")
async def snapshot_price(db: AsyncSession = Depends(get_async_session)):
    await save_price_snapshot(db)
    return {"msg": "快照成功"}

@router.get("/history/{symbol}")
async def get_price_history(
    symbol: str,
    db: AsyncSession = Depends(get_async_session)
):
    result = await db.execute(
        select(Price).where(Price.symbol == symbol.upper()).order_by(Price.date.desc())
    )
    prices = result.scalars().all()
    return [
        {"symbol": p.symbol, "date": p.date, "price": p.price}
        for p in prices
    ]