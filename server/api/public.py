from http.client import HTTPException
from fastapi import APIRouter, Query
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.get("/", summary="API Homepage")
async def root():
    """
    Redirect to the API documentation.
    """
    return RedirectResponse(url="/docs")

@router.get("/klines/{symbol}", summary="Get historical candlestick data")
async def get_klines(symbol: str, interval: str = Query(...), limit: int = Query(100, ge=1, le=1000)):
    """
    Returns simulated candlestick data for a given symbol.
    """
    try:
        # Simulated candlestick data
        return [{"time": i, "open": 100 + i, "close": 100 + i * 1.5, "high": 100 + i * 2, "low": 100 + i * 0.5} for i in range(limit)]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/exchanges", summary="Get supported exchanges")
async def get_exchanges():
    """
    Returns the list of supported exchanges.
    """
    return ["Binance", "Kraken"]

@router.get("/pairs/{exchange}", summary="Get trading pairs")
async def get_pairs(exchange: str):
    """
    Returns trading pairs available on a given exchange.
    """
    if exchange.lower() == "binance":
        return ["BTC/USDT", "ETH/USDT"]
    elif exchange.lower() == "kraken":
        return ["XBT/USD", "ETH/USD"]
    else:
        raise HTTPException(status_code=404, detail=f"Exchange {exchange} not supported.")
