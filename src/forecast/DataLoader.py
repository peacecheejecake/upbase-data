from datetime import datetime, timedelta
from time import sleep
import math
import pandas as pd

from upbit.candles import TimeUnit, UpbitCandles
from utils.datetime import kst_time

class DataLoader:

  @staticmethod
  async def load_candles(market: str, unit: TimeUnit, count: int):
    print("LOAD CANDLE DATA")
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

        sleep(0.5)

    print()

    df = pd.DataFrame(data=data)

    # if file_name:
    #     save_parquet(df, file_name)

    return df
  