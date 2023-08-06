import asyncio
import time

from algoralabs.admin.keycloak import get_client_id, async_get_client_id
from algoralabs.data.datasets.dataset import get_datasets, async_get_datasets
from algoralabs.data.datasets.query import query_dataset, async_query_dataset
from algoralabs.data.datasets.schema import get_schemas, async_get_schemas

start_time_sequential = time.time()

s1 = get_client_id()
s2 = get_schemas()
s3 = query_dataset("2880e242-8db4-49e2-aad3-e0339931582e")
s4 = get_datasets()

print(f"--- Sequential {time.time() - start_time_sequential} seconds ---")


start_time_async = time.time()
async def async_sample_calls():
    start_time_async = time.time()

    r1 = await async_get_client_id()
    r2 = await async_get_schemas()
    r3 = await async_query_dataset("2880e242-8db4-49e2-aad3-e0339931582e")
    r4 = await async_get_datasets()

    print(f"--- Async {time.time() - start_time_async} seconds ---")

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(async_sample_calls())
