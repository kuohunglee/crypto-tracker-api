from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from .auth_handler import decode_access_token
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.database import get_async_session  # 你自己的 async db session dependency

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")
# oauth2_scheme = OAuth2PasswordBearer(
#     tokenUrl="users/login",
#     bearerFormat="JWT",
#     description="Paste your access token here. Format: Bearer <token>"
# )

async def get_current_user(token: str=Depends(oauth2_scheme),
                     db: AsyncSession = Depends(get_async_session )
                    ) -> User:
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    email: str = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    # 查資料庫拿 User ORM 物件
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user  # ✅ 現在回傳的是 SQLAlchemy 的 User 實體