import io
from typing import Optional, Any, Dict

import pandas as pd
from pandas import DataFrame

from algoralabs.common.requests import __post_request
from algoralabs.data.transformations.response_transformers import no_transform
from algoralabs.data_engine.models import TransformOverride
from algoralabs.decorators.data import data_request


@data_request(transformer=no_transform)
def analyze_data(data: pd.DataFrame) -> Dict[str, Any]:
    endpoint = f"data-engine/alpha/analyze"

    parquet_bytes = data.to_parquet()
    return __post_request(endpoint, files={'file': parquet_bytes})


@data_request(processor=lambda r: r.content, transformer=lambda r: pd.read_parquet(io.BytesIO(r)))
def transform_data(data: pd.DataFrame, transform_override: Optional[TransformOverride] = None) -> DataFrame:
    endpoint = f"data-engine/alpha/transform"

    if transform_override is not None:
        transform_override = {'transform_override': transform_override.json()}
    else:
        transform_override = None

    parquet_bytes = data.to_parquet()
    return __post_request(endpoint, data=transform_override, files={'file': parquet_bytes})
