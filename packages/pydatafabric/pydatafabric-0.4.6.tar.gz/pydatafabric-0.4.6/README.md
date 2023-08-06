# SHINSEGAE DataFabric Python Package

[![Linter && Formatting](https://github.com/emartdt/datafabric-python-dist/actions/workflows/Flake8.yml/badge.svg)](https://github.com/emartdt/datafabric-python-dist/actions/workflows/Flake8.yml)
[![Publish to TestPyPI](https://github.com/emartdt/datafabric-python-dist/actions/workflows/TestPyPI.yml/badge.svg)](https://github.com/emartdt/datafabric-python-dist/actions/workflows/TestPyPI.yml)
[![Publish to PyPI](https://github.com/emartdt/datafabric-python-dist/actions/workflows/PyPI.yml/badge.svg)](https://github.com/emartdt/datafabric-python-dist/actions/workflows/PyPI.yml)

This is highly site dependent package. Resources are abstracted into package structure.

## Usage

Get pandas dataframe from parquet file in hdfs
```python
from pydatafabric.ye import parquet_to_pandas

pandas_df = parquet_to_pandas(hdfs_path)
```

Save pandas dataframe as parquet in hdfs
```python
from pydatafabric.ye import get_spark
from pydatafabric.ye import pandas_to_parquet

spark = get_spark()
pandas_to_parquet(pandas_df, hdfs_path, spark)  # we need spark for this operation
spark.stop()
```

Work with spark
```python
from pydatafabric.ye import get_spark

spark = get_spark()
# do with spark session
spark.stop()
```

Work with spark-bigquery-connector
```python
# SELECT
from pydatafabric.gcp import bq_table_to_pandas

pandas_df = bq_table_to_pandas("dataset", "table_name", ["col_1", "col_2"], "2020-01-01", "cust_id is not null")
# INSERT 
from pydatafabric.gcp import pandas_to_bq_table

pandas_to_bq_table(pandas_df, "dataset", "table_name", "2022-02-22")
```

Send slack message
```python
from pydatafabric.ye import slack_send

text = 'Hello'
username = 'airflow'
channel = '#leavemealone'
slack_send(text=text, username=username, channel=channel)
# Send dataframe as text
df = pd.DataFrame(data={'col1': [1, 2], 'col2': [3, 4]})
slack_send(text=df, username=username, channel=channel, dataframe=True)
```

Get bigquery client
```python
from pydatafabric.gcp import get_bigquery_client

bq = get_bigquery_client(project="emart-datafabric")
bq.query(query)
```

IPython BigQuery Magic
```python
from pydatafabric.gcp import import_bigquery_ipython_magic

import_bigquery_ipython_magic()

query_params = {
    "p_1": "v_1",
    "dataset": "common_dev",
}
```
```python
%% bq --params $query_params

SELECT c_1 
FROM {dataset}.user_logs
WHERE c_1 = @p_1
```

Use NES CLI
```bas
nes input_notebook_url -p k1 v1 -p k2 v2 -p k3 v3
```

Use github util
```python
from pydatafabric.ye import get_github_util

g = get_github_util
# query graphql
res = g.query_gql(graph_ql)
# get file in github repository
byte_object = g.download_from_git(github_url_path)
```

## Installation

```sh
$ pip install pydatafabric --upgrade
```

If you would like to install submodules for Emart Inc.

```sh
$ pip install pydatafabric[emart] --upgrade
```
