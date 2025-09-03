from app.models.price import Price
from app.database import get_async_session
from app.services.price_service import fetch_price
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

SUPPORTED_SYMBOLS = ["BTC", "ETH", "SOL", "DOGE"]

async def save_price_snapshot(db: AsyncSession):
    for symbol in SUPPORTED_SYMBOLS:
        try:
            price = await fetch_price(symbol)
            snapshot = Price(symbol=symbol, price=price, date=date.today())
            db.add(snapshot)
        except Exception as e:
            print(f"無法取得 {symbol} 價格：{e}")
    await db.commit()