from fastapi import FastAPI

from app import models
from app.api.analytics import router as analytics_router
from app.api.auth import router as auth_router
from app.api.categories import router as categories_router
from app.api.strategies import router as strategies_router
from app.api.transactions import router as transactions_router
from app.database import Base, engine

app = FastAPI(
    title="PFM API - Personal Finance Management",
    description="Backend per la gestione di spese e strategie di accumulo",
    version="0.2.0",
)

app.include_router(auth_router)
app.include_router(categories_router)
app.include_router(transactions_router)
app.include_router(analytics_router)
app.include_router(strategies_router)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {
        "status": "success",
        "message": "Motore API FastAPI operativo e in ascolto.",
        "environment": "development",
    }
