from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from passlib.hash import bcrypt

async def create_user(db: AsyncSession, username: str, email: str, password: str):
    hashed_pw = bcrypt.hash(password)
    new_user = User(username=username, email=email, hashed_password=hashed_pw)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def authenticate_user(db: AsyncSession, email: str, password: str):
    result = await db.execute(select(User).filter(User.email == email))
    user = result.scalar_one_or_none()
    if not user or not bcrypt.verify(password, user.hashed_password):
        return None
    return user