from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import models  # noqa: F401  (registra i modelli su Base)
from app.api.analytics import router as analytics_router
from app.api.auth import router as auth_router
from app.api.categories import router as categories_router
from app.api.strategies import router as strategies_router
from app.api.transactions import router as transactions_router
from app.database import Base, engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    # All'avvio: crea le tabelle se non esistono.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="PFM API - Personal Finance Management",
    description="Backend per la gestione di spese e strategie di accumulo",
    version="0.2.0",
    lifespan=lifespan,
)

app.include_router(auth_router)
app.include_router(categories_router)
app.include_router(transactions_router)
app.include_router(analytics_router)
app.include_router(strategies_router)


@app.get("/")
async def root():
    return {
        "status": "success",
        "message": "Motore API FastAPI operativo e in ascolto.",
        "environment": "development",
    }
