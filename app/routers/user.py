from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import SessionLocal
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.services.user_service import create_user, authenticate_user
from app.auth.auth_handler import create_access_token
from app.auth.auth_bearer import get_current_user

router = APIRouter()

# Dependency
async def get_db():
    async with SessionLocal() as session:
        yield session

@router.post("/register", response_model=UserOut)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db, user.username, user.email, user.password)

@router.post("/login")
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    found = await authenticate_user(db, user.email, user.password)
    if not found:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"sub": found.email})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
async def get_me(user=Depends(get_current_user)):
    return user