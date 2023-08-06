from enum import Enum
from typing import Optional

from pydantic import BaseModel


class OptionStyle(Enum):
    AMERICAN = 'AMERICAN'
    EUROPEAN = 'EUROPEAN'


class OptionType(Enum):
    CALL = 'CALL'
    PUT = 'PUT'


class OptionModel(Enum):
    BLACK_SCHOLES = 'BLACK_SCHOLES'
    BINOMIAL = 'BINOMIAL'
    MONTE_CARLO = 'MONTE_CARLO'


class OptionModelRequest(BaseModel):
    model: OptionModel = OptionModel.BLACK_SCHOLES
    style: OptionStyle
    type: Optional[OptionType] = None
    interest_rate: Optional[float] = None
    dividend_yield: Optional[float] = None
    days_until_expiration: int
    strike_price: float
    underlying_price: float
    volatility: float
