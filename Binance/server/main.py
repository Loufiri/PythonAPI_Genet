import asyncio
from fastapi import FastAPI
from server.api import public, authenticated
from server.core.market_data import collect_market_data

# FastAPI app instance
app = FastAPI(
    title="Cryptocurrency TWAP API",
    description="API for TWAP order execution and market data access.",
    version="1.0.0"
)

# Include API routers
app.include_router(public.router, prefix="/api/public")
app.include_router(authenticated.router, prefix="/api/auth")
