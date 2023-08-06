from typing import Optional

from algoralabs.common.requests import __post_request
from algoralabs.data.transformations.response_transformers import no_transform
from algoralabs.decorators.data import data_request
from algoralabs.models.utils import OptionStyle, OptionType, OptionModelRequest, OptionModel


@data_request(transformer=no_transform)
def option_price(strike_price: float,
                 underlying_price: float,
                 volatility: float,
                 days_until_expiration: int,
                 style: OptionStyle = OptionStyle.EUROPEAN,
                 model: OptionModel = OptionModel.BLACK_SCHOLES,
                 type: Optional[OptionType] = None,
                 interest_rate: Optional[float] = None,
                 dividend_yield: Optional[float] = None) -> float:
    endpoint = f"data-engine/alpha/price/option"

    data = OptionModelRequest(
        model=model,
        style=style,
        type=type,
        interest_rate=interest_rate,
        dividend_yield=dividend_yield,
        days_until_expiration=days_until_expiration,
        strike_price=strike_price,
        underlying_price=underlying_price,
        volatility=volatility,
    ).json()

    return __post_request(endpoint, data=data)
