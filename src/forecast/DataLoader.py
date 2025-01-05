from typing import Tuple, Optional
from datetime import datetime, timedelta
from time import sleep
import math
import numpy as np
import pandas as pd

from upbit.candles import TimeUnit, UpbitCandles
from utils.datetime import kst_time
from utils.functools import chain
from utils.backup import save_parquet
from .preprocess import (
  remove_duplicated, 
  sort_by_time, 
  add_mid_price,
  add_best_profit_rate, 
  # add_worst_profit_rate, 
  # add_profit_rate_bound_gap, 
  add_worst_profit_rate_before, 
  add_variance, 
  add_timedelta_after,
  add_price_changes,
  add_trade_volume_changes,
)

class DataLoader:

  @staticmethod
  async def load_candles(market: str, unit: TimeUnit, count: int, file_name: Optional[str] = None) -> pd.DataFrame:
    print(f"market={market}, candle_unit={unit}, count={count}")

    to = kst_time(datetime.now())
    # delta_to = timedelta_for_unit(unit)

    num_batches = math.ceil(count / 200)
    data = []

    for i in range(num_batches):
        print(f'\r{i + 1}/{num_batches}', end="")

        # url = f"{base_url(market, candle_unit)}?market={market}&count={count}&to={str(to).split('.')[:-1][0]}"
        # response = requests.get(url, headers=headers)
        # data += json.loads(response.text)
        _count = min(count - len(data), 200)
        data += await UpbitCandles.get_candles(market, unit, to, _count)
        # to -= delta_to * count
        last_datetime = datetime.strptime(data[-1]['candle_date_time_kst'], '%Y-%m-%dT%H:%M:%S')
        to = kst_time(last_datetime - timedelta(seconds=1))

        sleep(0.1)

    print()

    df = pd.DataFrame(data=data)
    
    if file_name:
      save_parquet(df, file_name)

    return df
  
  @staticmethod
  def preprocess(data: pd.DataFrame):
    return chain(
      remove_duplicated,
      sort_by_time,
      add_mid_price,
      add_best_profit_rate,
      # add_worst_profit_rate,
      # add_profit_rate_bound_gap,
      add_worst_profit_rate_before,
      add_variance,
      add_timedelta_after,
      add_price_changes,
      add_trade_volume_changes,
    )(data)

  @staticmethod
  def make_input_output(data: pd.DataFrame, columns_X: list, columns_y: list) -> Tuple[np.ndarray, np.ndarray]:
    _data = data.dropna(subset=columns_X + columns_y)
    return np.array(_data[columns_X]), np.array(_data[columns_y]).reshape(-1)
  