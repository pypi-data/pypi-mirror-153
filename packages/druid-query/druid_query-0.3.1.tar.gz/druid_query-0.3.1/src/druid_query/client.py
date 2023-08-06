import gzip
import json
from typing import Optional

import httpx

from .queries import NativeQuery, Sql
from .components.data_sources import Query
from .utils import druid_serealize


class DruidError(Exception):
    def __init__(self, message: str, code: int, details: Optional[str] = ''):
        self.message = message
        self.detailed_message = details
        self.code = code


class Client:
    def __init__(self, native_endpoint: Optional[str] = None, sql_endpoint: Optional[str] = None) -> None:
        if native_endpoint is None and sql_endpoint is None:
            raise AssertionError(
                'at least one of the native and sql endpoints must be provided')

        session = httpx.Client(headers={'Content-Type': 'application/json', 'Content-Encoding': 'gzip', 'Accept-Encoding': 'gzip'})
        self.native_endpoint = native_endpoint
        self.sql_endpoint = sql_endpoint
        self.inner = session
    
    
    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        self.inner.close()
    

    def execute(self, query: Query):
        if isinstance(query, NativeQuery):
            assert self.native_endpoint is not None
            resp = self.inner.post(self.native_endpoint, content=gzip.compress(
                json.dumps(query, default=druid_serealize).encode('utf-8')))
        elif isinstance(query, Sql):
            assert self.sql_endpoint is not None
            resp = self.inner.post(self.sql_endpoint, content=gzip.compress(
                json.dumps(query, default=druid_serealize).encode('utf-8')))
        else:
            raise TypeError('unknown query type')
        return process_response(resp, query)

class AsyncClient:
    def __init__(self, native_endpoint: Optional[str] = None, sql_endpoint: Optional[str] = None) -> None:
        if native_endpoint is None and sql_endpoint is None:
            raise AssertionError(
                'at least one of the native and sql endpoints must be provided')

        session = httpx.AsyncClient(headers={'Content-Type': 'application/json', 'Content-Encoding': 'gzip', 'Accept-Encoding': 'gzip'})
        self.native_endpoint = native_endpoint
        self.sql_endpoint = sql_endpoint
        self.inner = session
    
    async def __aenter__(self):
        return self


    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.inner.aclose()


    async def execute(self, query: Query):
        if isinstance(query, NativeQuery):
            assert self.native_endpoint is not None
            resp = await self.inner.post(self.native_endpoint, content=gzip.compress(
                json.dumps(query, default=druid_serealize).encode('utf-8')))
        elif isinstance(query, Sql):
            assert self.sql_endpoint is not None
            resp = await self.inner.post(self.sql_endpoint, content=gzip.compress(
                json.dumps(query, default=druid_serealize).encode('utf-8')))
        else:
            raise TypeError('unknown query type')
        return process_response(resp, query)


def process_response(resp, query: Query):
    if resp.status_code in [400, 429, 501, 504, 500]:
        errobj = resp.json()
        raise DruidError(errobj['error'], resp.status_code, errobj['errorMessage'])
    elif resp.status_code == 200:
        if isinstance(query, NativeQuery):
            return resp.json()
        assert isinstance(query, Sql)
        if query.result_format in ['object', 'array']:
            return resp.json()
        elif query.result_format in ['objectLines', 'arayLines']:
            return [json.loads(line) for line in resp.content.decode('utf-8').strip().splitlines()]
        elif query.result_format == 'csv':
            return resp.content.decode('utf-8')
        else:
            return resp.content
    else:
        return resp.content
