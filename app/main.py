from fastapi import FastAPI
from app.routers import user, portfolio, price, price

app = FastAPI(title="Crypto Tracker API")

app.include_router(user.router)
app.include_router(portfolio.router)
app.include_router(price.router)


@app.get("/")
def root():
    return {"message": "Welcome to Crypto Tracker API"}