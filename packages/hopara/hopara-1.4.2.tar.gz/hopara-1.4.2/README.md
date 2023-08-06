# Pyhopara

Pyhopara is the Hopara Python SDK. It's main purpose is to ingest data from Python/Pandas.

### Install
```shell
pip install hopara
```

---
Before using Pyhopara you should setup your environment. This is achieved by installing the Hopara CLI and sign-in or sign-up:
```shell
npm install -g hopara
hopara signup
```

---

Basic usage:

```python
import hopara as hp

hopara = hp.Hopara()

table = hp.Table('table_name')
table.add_column('column1', hp.ColumnType.INTEGER)
table.add_column('column2', hp.ColumnType.STRING)

hopara.create_table(table)

rows = [{'column1': 1, 'column2': 'a'},
        {'column1': 2, 'column2': 'b'},
        {'column1': 3, 'column2': 'c'}]
hopara.insert_rows(table, rows)
```

With pandas DataFrame:

```python
import hopara as hp
import hopara.from_pandas as hpd
import pandas as pd

hopara = hp.Hopara()

df = pd.DataFrame({
    'column1': [1, 2, 3],
    'column2': ['a', 'b', 'c']
})
table = hpd.get_table('table_name', df)

hopara.create_table(table)
hopara.insert_rows(table, hpd.get_rows(df))
```

Please check the ``Hopara`` and ``Table`` sections for additional options.