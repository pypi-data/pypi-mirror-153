from dataclasses import asdict
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Union, Any, Dict


class AssetClass(Enum):
    COMMODITY = "commodity"
    CREDIT = "credit"
    EQUITY = "equity"
    FOREX = "forex"
    RATES = "rates"


class Repository(Enum):
    CME = "CME"
    DTCC = "DTCC"
    ICE = "ICE"


@dataclass
class LogicalDisplayName:
    display_name: str
    logical_name: str


@dataclass
class DateRange:
    start_date: str
    end_date: str
    enabled: bool


@dataclass
class APIFieldFilter:
    logical_display: LogicalDisplayName
    operator: str  # operator can be "NOT_IN" or "IN" or "NOT_EQUAL" or "EQUAL" or "GTE" or "GT" or "LTE" or "LT"
    selected_values: List[str]


@dataclass
class FieldFilter:
    field: str
    operator: str  # operator can be "NOT_IN" or "IN" or "NOT_EQUAL" or "EQUAL" or "GTE" or "GT" or "LTE" or "LT"
    selected_values: List[str]


@dataclass
class DataFilter:
    date_range: Optional[DateRange]
    filters: List[Union[FieldFilter, APIFieldFilter]]


def __transform_filter(filter: Union[FieldFilter, APIFieldFilter]) -> APIFieldFilter:
    if isinstance(filter, APIFieldFilter):
        return filter

    return APIFieldFilter(
        logical_display=LogicalDisplayName(
            logical_name=filter.field,
            display_name=filter.field
        ),
        operator=filter.operator,
        selected_values=filter.selected_values
    )


def transform_data_filter(data_filter: Optional[DataFilter]) -> Optional[Dict[str, Any]]:
    if data_filter is not None:
        transformed_filter = DataFilter(
            date_range=data_filter.date_range,
            filters=list(map(__transform_filter, data_filter.filters))
        )

        return asdict(transformed_filter)

    return None
