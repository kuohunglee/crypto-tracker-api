from fastapi import FastAPI
from app.routers import user, portfolio, price

app = FastAPI(title="Crypto Tracker API")

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(portfolio.router, prefix="/portfolio", tags=["portfolio"])
app.include_router(price.router, prefix="/price", tags=["price"])


@app.get("/")
def root():
    return {"message": "Welcome to Crypto Tracker API"}