# alpha-data-py
## A client to fetch data from the alphaticks data base

### Installation

You can install alpha-data-py using the following command:
```shell
pip install alpha-data-py
```

### Usage

In order to use the library, you need an API key from alphaticks. Go to [alphaticks.io](https://alphaticks.io),
Account -> Licenses -> AlphaData and click on **Add credentials**.

Now that you have your credentials ready, you can create a client, fetch a security, and fetch the data you need for 
that security.

```py
import datetime
from adata import Client, FREQ_1M

c = Client(API_KEY, API_SECRET)
secs = c.get_securities()
for s in secs:
    if s.symbol == "BTCUSDT" and s.exchange == "fbinance":
        sec = s

start = datetime.datetime(2022, 1, 1)
end = datetime.datetime(2022, 1, 5)
it = c.get_historical_ohlcv(sec, FREQ_1M, start, end)
while it.next():
    print(it.o, it.h, it.l, it.c, it.v)
```
