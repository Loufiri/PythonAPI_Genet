# Pydantic models
from pydantic import BaseModel


class TWAPOrder(BaseModel):
    symbol: str
    quantity: float
    duration: int  # In seconds
    limit_price: float
    side: str  # "buy" or "sell"