from typing import List, Union, Dict

from pandas import DataFrame

from algoralabs.data.iex.utils import __base_request, __async_base_request, transform_one_or_many
from algoralabs.data.transformations.response_transformers import no_transform
from algoralabs.decorators.data import data_request, async_data_request


def _symbols_request_info() -> dict:
    return {
        "extension": f"ref-data/symbols"
    }


@data_request
def symbols() -> DataFrame:
    """
    Symbols that IEX Cloud supports for intraday price updates.

    Reference: https://iexcloud.io/docs/api/#symbols

    :return: Dataframe of data
    """
    request_info = _symbols_request_info()
    return __base_request(**request_info)


@async_data_request
async def async_symbols() -> DataFrame:
    """
    Symbols that IEX Cloud supports for intraday price updates.

    Reference: https://iexcloud.io/docs/api/#symbols

    :return: Dataframe of data
    """
    request_info = _symbols_request_info()
    return await __async_base_request(**request_info)


def _historical_prices_request_info(*symbol: str, **kwargs) -> dict:
    request_info = {
        'range': '1m',
        'sort': 'asc'
    }
    request_info.update(kwargs)

    if len(symbol) > 1:
        request_info.update({
            'extension': "stock/market/batch",
            'symbols': ','.join(symbol),
            'types': 'chart'
        })
    else:
        request_info.update({'extension': f"time-series/HISTORICAL_PRICES/{symbol[0]}"})

    return request_info


@data_request(transformer=lambda d: transform_one_or_many(d, 'chart'))
def historical_prices(*symbol: str, **kwargs) -> Union[DataFrame, Dict[str, DataFrame]]:
    """
    Historical Prices via Time Series Endpoint
    Reference: https://iexcloud.io/docs/api/#time-series-endpoint

    :param symbol: (*str) Stock symbol(s), such as "AAPL" or "AAPL", "FB"
    :param range: (str) Optional. Returns data for a given range. Supported ranges described below.
    :param calendar: (bool) Optional. Boolean. Used in conjunction with `range` to return data in the future.
    :param limit: (int) Optional. Limits the number of results returned. Defaults to 1 when no date or range
        `{subkey}` is specified
    :param subattribute: (str) Optional. Allows you to query time series by fields in the result set.
        All time series data is stored by ID, then key, then subkey. If you want to query by any other
        field in the data, you can use `subattribute`.

        For example, news may be stored as `/news/{symbol}/{newsId}`, and the result data returns the keys
        `id`, `symbol`, `date`, `sector`, `hasPaywall`, `lang`
        By default you can only query by symbol or id. Maybe you want to query all news where the language is English.

        Your query would be: `/time-series/news?subattribute=lang|en`
        The syntax is `subattribute={keyName1}|{value1},{keyName2}|{value2}`

        Both the key name and the value are case sensitive. A pipe symbol (|) is used to represent
        “equal to”, and a tilde symbol (~) is used to represent “not equal to”.

    :param dateField: (str) Optional. All time series data is stored by a single date field, and that field
        is used for any range or date parameters. You may want to query time series data by a different date in
        the result set. To change the date field used by range queries, pass the case sensitive field name
        with this parameter. For example, corporate buy back data may be stored by announce date,
        but also contains an end date which you’d rather query by.
        To query by end date you would use `dateField=endDate&range=last-week`

    :param from: (str) Optional. Returns data on or after the given from date. Format `YYYY-MM-DD`
    :param to: (str) Optional. Returns data on or before the given to date. Format `YYYY-MM-DD`
    :param on: (str) Optional. Returns data on the given date. Format `YYYY-MM-DD`
    :param last: (int) Optional. Returns the latest n number of records in the series
    :param next: (int) Optional. Returns the next n number of records in the series
    :param first: (int) Optional. Returns the first n number of records in the series
    :param filter: (str) Optional. The standard filter parameter. Filters return data to the specified comma
        delimited list of keys (case-sensitive)
    :param format: (str) Optional. The standard format parameter. Returns data as JSON by default.
        See the data format section for supported types.
    :param sort: (str) Optional. Specify the order of results, either `ASC` or `DESC`.
        Historical queries, including queries that use `last`, will default to descending date order
        (e.g. first record returned is most recent record). Forward looking queries, including queries
        that use `first` or specify `calendar`, will default to ascending date order (e.g. first record
        returned is nearest record in the future or from the start).
    :param interval: (int) Optional. Return every `nth` record in the result

    :return: Dataframe of data
    """
    # default query params
    request_info = _historical_prices_request_info(*symbol, **kwargs)
    return __base_request(**request_info)


@async_data_request(transformer=lambda d: transform_one_or_many(d, 'chart'))
async def async_historical_prices(*symbol: str, **kwargs) -> Union[DataFrame, Dict[str, DataFrame]]:
    """
    Historical Prices via Time Series Endpoint
    Reference: https://iexcloud.io/docs/api/#time-series-endpoint

    :param symbol: (*str) Stock symbol(s), such as "AAPL" or "AAPL", "FB"
    :param range: (str) Optional. Returns data for a given range. Supported ranges described below.
    :param calendar: (bool) Optional. Boolean. Used in conjunction with `range` to return data in the future.
    :param limit: (int) Optional. Limits the number of results returned. Defaults to 1 when no date or range
        `{subkey}` is specified
    :param subattribute: (str) Optional. Allows you to query time series by fields in the result set.
        All time series data is stored by ID, then key, then subkey. If you want to query by any other
        field in the data, you can use `subattribute`.

        For example, news may be stored as `/news/{symbol}/{newsId}`, and the result data returns the keys
        `id`, `symbol`, `date`, `sector`, `hasPaywall`, `lang`
        By default you can only query by symbol or id. Maybe you want to query all news where the language is English.

        Your query would be: `/time-series/news?subattribute=lang|en`
        The syntax is `subattribute={keyName1}|{value1},{keyName2}|{value2}`

        Both the key name and the value are case sensitive. A pipe symbol (|) is used to represent
        “equal to”, and a tilde symbol (~) is used to represent “not equal to”.

    :param dateField: (str) Optional. All time series data is stored by a single date field, and that field
        is used for any range or date parameters. You may want to query time series data by a different date in
        the result set. To change the date field used by range queries, pass the case sensitive field name
        with this parameter. For example, corporate buy back data may be stored by announce date,
        but also contains an end date which you’d rather query by.
        To query by end date you would use `dateField=endDate&range=last-week`

    :param from: (str) Optional. Returns data on or after the given from date. Format `YYYY-MM-DD`
    :param to: (str) Optional. Returns data on or before the given to date. Format `YYYY-MM-DD`
    :param on: (str) Optional. Returns data on the given date. Format `YYYY-MM-DD`
    :param last: (int) Optional. Returns the latest n number of records in the series
    :param next: (int) Optional. Returns the next n number of records in the series
    :param first: (int) Optional. Returns the first n number of records in the series
    :param filter: (str) Optional. The standard filter parameter. Filters return data to the specified comma
        delimited list of keys (case-sensitive)
    :param format: (str) Optional. The standard format parameter. Returns data as JSON by default.
        See the data format section for supported types.
    :param sort: (str) Optional. Specify the order of results, either `ASC` or `DESC`.
        Historical queries, including queries that use `last`, will default to descending date order
        (e.g. first record returned is most recent record). Forward looking queries, including queries
        that use `first` or specify `calendar`, will default to ascending date order (e.g. first record
        returned is nearest record in the future or from the start).
    :param interval: (int) Optional. Return every `nth` record in the result

    :return: Dataframe of data
    """
    # default query params
    request_info = _historical_prices_request_info(*symbol, **kwargs)
    return await __async_base_request(**request_info)


def _news_request_info(symbol: str, kwargs):
    request_info = {
        "extension": f"time-series/news/{symbol}"
    }
    request_info.update(kwargs)
    return request_info


@data_request
def news(symbol: str, **kwargs) -> DataFrame:
    """
    News for given symbol
    Reference: https://iexcloud.io/docs/api/#news

    :param symbol: (str) Stock symbol, such as AAPL
    :param range: (str) Optional. Returns data for a given range. Supported ranges described below.
    :param calendar: (bool) Optional. Boolean. Used in conjunction with `range` to return data in the future.
    :param limit: (int) Optional. Limits the number of results returned. Defaults to 1 when no date or range
        `{subkey}` is specified
    :param subattribute: (str) Optional. Allows you to query time series by fields in the result set.
        All time series data is stored by ID, then key, then subkey. If you want to query by any other
        field in the data, you can use `subattribute`.

        For example, news may be stored as `/news/{symbol}/{newsId}`, and the result data returns the keys
        `id`, `symbol`, `date`, `sector`, `hasPaywall`, `lang`
        By default you can only query by symbol or id. Maybe you want to query all news where the language is English.

        Your query would be: `/time-series/news?subattribute=lang|en`
        The syntax is `subattribute={keyName1}|{value1},{keyName2}|{value2}`

        Both the key name and the value are case sensitive. A pipe symbol (|) is used to represent
        “equal to”, and a tilde symbol (~) is used to represent “not equal to”.

    :param dateField: (str) Optional. All time series data is stored by a single date field, and that field
        is used for any range or date parameters. You may want to query time series data by a different date in
        the result set. To change the date field used by range queries, pass the case sensitive field name
        with this parameter. For example, corporate buy back data may be stored by announce date,
        but also contains an end date which you’d rather query by.
        To query by end date you would use `dateField=endDate&range=last-week`

    :param from: (str) Optional. Returns data on or after the given from date. Format `YYYY-MM-DD`
    :param to: (str) Optional. Returns data on or before the given to date. Format `YYYY-MM-DD`
    :param on: (str) Optional. Returns data on the given date. Format `YYYY-MM-DD`
    :param last: (int) Optional. Returns the latest n number of records in the series
    :param next: (int) Optional. Returns the next n number of records in the series
    :param first: (int) Optional. Returns the first n number of records in the series
    :param filter: (str) Optional. The standard filter parameter. Filters return data to the specified comma
        delimited list of keys (case-sensitive)
    :param format: (str) Optional. The standard format parameter. Returns data as JSON by default.
        See the data format section for supported types.
    :param sort: (str) Optional. Specify the order of results, either `ASC` or `DESC`.
        Historical queries, including queries that use `last`, will default to descending date order
        (e.g. first record returned is most recent record). Forward looking queries, including queries
        that use `first` or specify `calendar`, will default to ascending date order (e.g. first record
        returned is nearest record in the future or from the start).
    :param interval: (int) Optional. Return every `nth` record in the result

    :return: Dataframe of data
    """
    request_info = _news_request_info(symbol, kwargs)
    return __base_request(**request_info)


@async_data_request
async def async_news(symbol: str, **kwargs) -> DataFrame:
    """
    News for given symbol
    Reference: https://iexcloud.io/docs/api/#news

    :param symbol: (str) Stock symbol, such as AAPL
    :param range: (str) Optional. Returns data for a given range. Supported ranges described below.
    :param calendar: (bool) Optional. Boolean. Used in conjunction with `range` to return data in the future.
    :param limit: (int) Optional. Limits the number of results returned. Defaults to 1 when no date or range
        `{subkey}` is specified
    :param subattribute: (str) Optional. Allows you to query time series by fields in the result set.
        All time series data is stored by ID, then key, then subkey. If you want to query by any other
        field in the data, you can use `subattribute`.

        For example, news may be stored as `/news/{symbol}/{newsId}`, and the result data returns the keys
        `id`, `symbol`, `date`, `sector`, `hasPaywall`, `lang`
        By default you can only query by symbol or id. Maybe you want to query all news where the language is English.

        Your query would be: `/time-series/news?subattribute=lang|en`
        The syntax is `subattribute={keyName1}|{value1},{keyName2}|{value2}`

        Both the key name and the value are case sensitive. A pipe symbol (|) is used to represent
        “equal to”, and a tilde symbol (~) is used to represent “not equal to”.

    :param dateField: (str) Optional. All time series data is stored by a single date field, and that field
        is used for any range or date parameters. You may want to query time series data by a different date in
        the result set. To change the date field used by range queries, pass the case sensitive field name
        with this parameter. For example, corporate buy back data may be stored by announce date,
        but also contains an end date which you’d rather query by.
        To query by end date you would use `dateField=endDate&range=last-week`

    :param from: (str) Optional. Returns data on or after the given from date. Format `YYYY-MM-DD`
    :param to: (str) Optional. Returns data on or before the given to date. Format `YYYY-MM-DD`
    :param on: (str) Optional. Returns data on the given date. Format `YYYY-MM-DD`
    :param last: (int) Optional. Returns the latest n number of records in the series
    :param next: (int) Optional. Returns the next n number of records in the series
    :param first: (int) Optional. Returns the first n number of records in the series
    :param filter: (str) Optional. The standard filter parameter. Filters return data to the specified comma
        delimited list of keys (case-sensitive)
    :param format: (str) Optional. The standard format parameter. Returns data as JSON by default.
        See the data format section for supported types.
    :param sort: (str) Optional. Specify the order of results, either `ASC` or `DESC`.
        Historical queries, including queries that use `last`, will default to descending date order
        (e.g. first record returned is most recent record). Forward looking queries, including queries
        that use `first` or specify `calendar`, will default to ascending date order (e.g. first record
        returned is nearest record in the future or from the start).
    :param interval: (int) Optional. Return every `nth` record in the result

    :return: Dataframe of data
    """
    request_info = _news_request_info(symbol, kwargs)
    return await __async_base_request(**request_info)


def _peer_group_request_info(symbol: str) -> dict:
    return {
        "extension": f"stock/{symbol}/peers"
    }


@data_request(transformer=no_transform)
def peer_group(symbol: str) -> List[str]:
    """
    Stock peers
    Reference: https://iexcloud.io/docs/api/#peers

    :param symbol: (str) Stock symbol, such as AAPL
    :return list of symbols
    """
    request_info = _peer_group_request_info(symbol)
    return __base_request(**request_info)


@async_data_request(transformer=no_transform)
async def async_peer_group(symbol: str) -> List[str]:
    """
    Stock peers
    Reference: https://iexcloud.io/docs/api/#peers

    :param symbol: (str) Stock symbol, such as AAPL
    :return list of symbols
    """
    request_info = _peer_group_request_info(symbol)
    return await __async_base_request(**request_info)


