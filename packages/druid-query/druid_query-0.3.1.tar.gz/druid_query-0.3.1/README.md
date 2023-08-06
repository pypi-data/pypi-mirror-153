# Apache Druid Query Library

A simple library for creating and executing queries with Apache Druid.

## Usage

### SQL Queries

```python
from druid_query.client import Client
from druid_query.queries import Sql

client = Client(sql_endpoint='localhost:8082/druid/v2/sql/')

query = Sql('SELECT * FROM wikipedia LIMIT 10')

result = client.execute(query)

print(result)
```

### Native Queries

```python
from druid_query.client import Client
from druid_query.components import *
from druid_query.queries import Timeseries

client = Client(native_endpoint='localhost:8082/druid/v2/')

query = Timeseries('wikipedia', [intervals.Interval('2015-09-11', '2015-09-13')], granularities.Period('PT2H'), aggregations=[aggregations.Count('num_records')])

result = client.execute(client, query)

print(result)
```

### Async support
```python
from druid_query.client import AsyncClient
from druid_query.queries import Sql
import asyncio

client = AsyncClient(sql_endpoint='localhost:8082/druid/v2/sql/')

query = Sql('SELECT * FROM wikipedia LIMIT 10')

result = asyncio.run(client.execute(query))

print(result)
```
