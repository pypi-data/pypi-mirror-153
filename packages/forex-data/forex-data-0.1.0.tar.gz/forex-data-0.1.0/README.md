# Forex Data Get and Process
A small demo library for getting forex data and process it

### Installation
```
pip install forex-data
```

### Get started
How to pass currency pairs to process it:

```Python
from forex_data import portfolio
from forex_data import get_process
currency_pairs = [["AUD","USD",[],portfolio("AUD","USD")],
                  ["GBP","EUR",[],portfolio("GBP","EUR")],
                  ["USD","CAD",[],portfolio("USD","CAD")]]

get_process(currency_pairs, "sqlite_hw1/test.db", 86400, 360)   # 86400=24h, 360=6min

# get_process(currency_pairs, db_path, total_run_time, aggregate_time)
# time should be seconds
```