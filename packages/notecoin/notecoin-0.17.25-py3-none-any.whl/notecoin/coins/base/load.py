import json
import time

import ccxt
import pandas as pd
from ccxt.base.exchange import Exchange
from notecoin.base.database import KlineData
from tqdm import tqdm


class LoadDataKline:
    def __init__(self, exchange: Exchange, *args, **kwargs):
        self.table = KlineData()
        self.exchange = exchange
        super(LoadDataKline, self).__init__(*args, **kwargs)

    def load_all(self, *args, **kwargs):
        self.exchange.load_markets()
        for sym in tqdm(self.exchange.symbols):
            if ':' not in sym:
                self.load(sym, *args, **kwargs)

    def load(self, symbol, timeframe='1m', max_retries=3, limit=100, *args, **kwargs):
        max_time, min_time = self.table.select_symbol_maxmin(symbol)
        timeframe_duration_in_ms = self.exchange.parse_timeframe(timeframe) * 1000
        timedelta = limit * timeframe_duration_in_ms

        if max_time == 0 or min_time == 0:
            max_time = self.exchange.milliseconds()
            min_time = self.exchange.milliseconds()

        def load(fetch_since):
            result = self.exchange.fetch_ohlcv(symbol, timeframe, fetch_since, limit=limit)
            result = self.exchange.sort_by(result, 0)
            if len(result) == 0:
                return False, f'result is empty, fetch_since:{fetch_since}'
            pbar.set_postfix({'fetch_since': self.exchange.iso8601(result[0][0])})
            df = pd.DataFrame(result, columns=['timestamp', 'open', 'close', 'low', 'high', 'vol'])
            df['symbol'] = symbol
            self.table.insert(json.loads(df.to_json(orient='records')))
            time.sleep(int(self.exchange.rateLimit / 1000))
            return True, result

        earliest_timestamp = min_time
        pbar = tqdm(range(min_time, min_time-100*timedelta, -timedelta), desc=symbol)
        for _ in pbar:
            status, result = load(earliest_timestamp - timedelta)
            if status is False:
                print(result)
                break
            earliest_timestamp = result[0][0]

        #earliest_timestamp = self.exchange.milliseconds()
        lasted_timestamp = max_time
        pbar = tqdm(range(max_time, max_time+100*timedelta, timedelta), desc=symbol)
        for _ in pbar:
            status, result = load(lasted_timestamp)
            if status is False:
                print(result)
                break
            lasted_timestamp = result[-1][0]


exchan = LoadDataKline(ccxt.okex())
# exchan.load('BTC/USDT')
# exchan.load('BTC/USDT')
exchan.load_all()
