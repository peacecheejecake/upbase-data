from typing import Literal, Optional, Union
from datetime import datetime, timedelta

from .request import request

TimeUnit = Literal['minute', 'hour', 'day', 'week', 'second']


class UpbitCandles:

  @classmethod
  def upbit_api_path(cls, unit: TimeUnit) -> str:
    if unit == 'hour':
        return "/candles/minutes/60"

    if unit == 'minute':
        return "/candles/minutes/1"

    if unit in ['day', 'week', 'month', 'second']:
        return f"/candles/{unit}s"

    raise Exception("Unit must be one of 'minute', 'hour', 'day', 'week', 'month', 'second'")
  
  @classmethod
  def timedelta_for_unit(cls, unit: TimeUnit):
    if unit == 'second':
        return timedelta(seconds=1)

    if unit == 'minute':
        return timedelta(minutes=1)

    if unit == 'hour':
        return timedelta(hours=1)

    if unit == 'day':
        return timedelta(days=1)

    if unit == 'week':
        return timedelta(days=7)

  @classmethod
  def get_candles(cls, market: str, unit: TimeUnit, to: Union[str, datetime], count: Optional[int] = 200):
    url = cls.upbit_api_path(unit)

    # delta_to = cls.timedelta_for_unit(unit)
    return request.get(url, params={
      "market": market, 
      "count": count,
      "to": str(to),
    })


