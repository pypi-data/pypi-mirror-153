# Algora Labs Python SDK

[Algora Labs](https://algoralabs.com/) is an IDE for Quants. We provide users financial data, a research environment and
visualization tools to efficiently translate research ideas into actionable insights for trading.
The [algora-sdk](https://pypi.org/project/algora-sdk/) allows users to programmatically access datasets and resources on
our platform.

## Installation

When running locally, set the following environment variables for your username and password
for [Algora Labs](https://trade.algoralabs.com/). When running code on our platform, there is no need to set these
environment variables.

```text
ALGORA_USER=username
ALGORA_PWD=password
```

## Examples

These examples can be run on our platform.

### Rolling Performance

```python
import pandas as pd

from algoralabs.data.iex.stocks import historical_prices


def calculate_returns(df: pd.DataFrame, column: str = 'high', shift: int = 1):
    return df[column].diff() / df[column].shift(shift)


def main(symbol):
    shift = 30

    df = historical_prices(symbol, range="10y")
    df['rolling_return'] = calculate_returns(df, shift=shift) * 100

    df = df.iloc[shift:]

    return df


if __name__ == '__main__':
    print(main("AAPL"))
```

### Swap Data Repository

Note: You must have privileges to access this SDR data

```python
from algoralabs.data.sdr.query import commodity, get_by_date, get_distinct_in_field
from algoralabs.data.sdr.utils import AssetClass, Repository, DataFilter, DateRange, FieldFilter


def main():
    print("Querying Commodity dataset without filters")
    print(commodity())

    print("Querying Commodity dataset by date and repository")
    print(get_by_date(asset_class=AssetClass.COMMODITY, date="2022-01-01", repos=[Repository.CME]))

    print("Getting distinct values in `leg_1_asset` field. These values can be used in the FieldFilter")
    print(get_distinct_in_field(asset_class=AssetClass.COMMODITY, field="leg_1_asset"))

    commodity_filter = DataFilter(
        # data_range is optional, can be None
        date_range=DateRange(
            start_date="2022-01-01",
            end_date="2022-01-01",
            enabled=False  # set to True to enable
        ),
        filters=[
            FieldFilter(
                field="repository",
                # operator can be "NOT_IN" or "IN" or "NOT_EQUAL" or "EQUAL" or "GTE" or "GT" or "LTE" or "LT"
                operator="IN",
                selected_values=["CME", "DTCC"]
            ),
            FieldFilter(
                field="sector",
                operator="IN",
                selected_values=["Energy"]
            )
        ]
    )

    print("Querying Commodity dataset with filters")
    commodity_filter_df = commodity(commodity_filter)

    print(commodity_filter_df)


if __name__ == '__main__':
    main()
```

## Contact

Please [Contact Us](mailto:support@algoralabs.com) if you have any questions!
