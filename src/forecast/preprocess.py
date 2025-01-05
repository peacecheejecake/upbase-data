from datetime import datetime
import pandas as pd

# from utils.functools import chain
# from utils.file_io import load_candle_data, load_parquet

DATE_TIME_KEY = 'candle_date_time_kst'

def clone(data: pd.DataFrame) -> pd.DataFrame:
    return data.copy().iloc[::-1].reset_index(drop=True)

def sort_by_time(data: pd.DataFrame, reverse: bool = False) -> pd.DataFrame:
    print('sort_by_time')
    _data = clone(data)
    return _data.sort_values(by=[DATE_TIME_KEY], ascending=reverse)

def remove_duplicated(data: pd.DataFrame) -> pd.DataFrame:
    print('remove_duplicated')
    return clone(data).loc[data.duplicated().apply(lambda x: not x)]

def add_mid_price(data: pd.DataFrame, sort: bool = False) -> pd.DataFrame:
    print('add_mid_prices')
    _data = (sort_by_time if sort else clone)(data)
    mid_prices = (_data.high_price + _data.low_price).div(2)
    _data.insert(_data.columns.size, 'mid_price', mid_prices)
    return _data

def add_price_changes(data: pd.DataFrame, sort: bool = False) -> pd.DataFrame:
    if 'mid_price' not in data.columns:
        data = add_mid_price(data, sort)
        
    print('add_price_changes')
    
    _data = (sort_by_time if sort else clone)(data)
    
    diff_mid_prices = _data.mid_price.diff().div(_data.mid_price)
    diff_opening_prices = _data.opening_price.diff().div(_data.opening_price)
    diff_high_prices = _data.high_price.diff().div(_data.high_price)
    diff_low_prices = _data.low_price.diff().div(_data.low_price)
    
    _data.insert(_data.columns.size, 'diff_mid_price', diff_mid_prices)
    _data.insert(_data.columns.size, 'diff_opening_price', diff_opening_prices)
    _data.insert(_data.columns.size, 'diff_high_price', diff_high_prices)
    _data.insert(_data.columns.size, 'diff_low_price', diff_low_prices)
    
    return _data

def add_trade_volume_changes(data: pd.DataFrame, sort: bool = False) -> pd.DataFrame:
    print('add_trade_volume_changes')
    _data = (sort_by_time if sort else clone)(data)
    
    diff_trade_volumes = _data.candle_acc_trade_volume.diff()
    _data.insert(_data.columns.size, 'diff_candle_acc_trade_volume', diff_trade_volumes)
    
    return _data

def add_variance(data: pd.DataFrame, stride: int = 60, sort: bool = False) -> pd.DataFrame:
    print('add_variance')
    _data = (sort_by_time if sort else clone)(data)
    variances = pd.Series(_data.mid_price.iloc[index - stride + 1:index + 1].std() for index, _ in enumerate(_data.mid_price.iloc[stride:]))
    _data.insert(_data.columns.size, 'variance', variances)
    return _data

def add_best_profit_rate(data: pd.DataFrame, stride: int = 60, sort: bool = False) -> pd.DataFrame:
    print('add_best_profit_rate')
    _data = (sort_by_time if sort else clone)(data)
    best_profit_rates = []

    for i in range(len(_data)):
        current_price = _data.mid_price.iloc[i]
        high_price = _data.mid_price.iloc[i + 1:i + stride + 1].max()
        best_profit_rate = (high_price - current_price) / current_price
        best_profit_rates.append(best_profit_rate)

    _data.insert(data.columns.size, 'best_profit_rate', best_profit_rates)
    return _data

def add_worst_profit_rate(data: pd.DataFrame, stride: int = 60, sort: bool = False) -> pd.DataFrame:
    print('add_worst_profit_rate')
    _data = (sort_by_time if sort else clone)(data)
    worst_profit_rates = []

    for i in range(len(_data)):
        current_price = _data.mid_price.iloc[i]
        low_price = _data.mid_price.iloc[i + 1:i + stride + 1].min()
        worst_profit_rate = (low_price - current_price) / current_price
        worst_profit_rates.append(worst_profit_rate)

    _data.insert(data.columns.size, 'worst_profit_rate', worst_profit_rates)
    return _data

def add_worst_profit_rate_before(data: pd.DataFrame, stride: int = 60, sort: bool = False) -> pd.DataFrame:
    print('add_worst_profit_rate_before')
    _data = (sort_by_time if sort else clone)(data)
    worst_profit_rates = []

    for i in range(len(_data)):
        current_price = _data.mid_price.iloc[i]
        low_price = _data.mid_price.iloc[max(0, i - stride):i].min()
        worst_profit_rate = (low_price - current_price) / current_price
        worst_profit_rates.append(worst_profit_rate)

    _data.insert(data.columns.size, 'worst_profit_rate_before', worst_profit_rates)
    return _data

def add_profit_rate_bound_gap(data: pd.DataFrame, stride: int = 60, sort: bool = False) -> pd.DataFrame:
    print('add_profit_rate_bound_gap')
    _data = (sort_by_time if sort else clone)(data)
    columns = _data.columns

    if 'best_profit_rate' not in columns:
        _data = add_best_profit_rate(_data, stride)

    if 'worst_profit_rate' not in columns:
        _data = add_worst_profit_rate(_data, stride)

    _data.insert(data.columns.size, 'profit_rate_bound_gap', _data.best_profit_rate - _data.worst_profit_rate)
    return _data

def add_timedelta_after(data: pd.DataFrame, stride: int = 60, sort: bool = False) -> pd.DataFrame:
    print('add_timedelta_after')
    _data = (sort_by_time if sort else clone)(data)
    datetimes = _data[DATE_TIME_KEY]

    def _to_datetime(t):
        return datetime.strptime(t, '%Y-%m-%dT%H:%M:%S')

    time_after = [
        (_to_datetime(datetimes.iloc[i + stride]) - _to_datetime(datetimes.iloc[i])).seconds
            if i + stride < len(datetimes)
            else None
        for i in range(len(datetimes))
    ]
    _data.insert(data.columns.size, f'timedelta_after', time_after)
    return _data

# def prepare_data(market=None, candle_unit=None, num_candles=None, time_bound=None, from_file=None):
#     if from_file:
#         data = load_parquet(from_file)
#     else:
#         file_name=f"{market}-{candle_unit}-{num_candles}-{candle_unit}{'s' if num_candles > 1 else ''}"
#         data = load_candle_data(
#             market,
#             candle_unit=candle_unit,
#             num_candles=num_candles,
#             file_name=file_name
#         )

#     return chain(
#         set_mid_prices,
#         # lambda d: search_peaks_in_bounds(d, until=-time_bound, target='lowest'),
#         # lambda d: search_peaks_in_bounds(d, until=time_bound, target='lowest'),
#         # lambda d: search_peaks_in_bounds(d, until=-time_bound, target='highest'),
#         # lambda d: search_peaks_in_bounds(d, until=time_bound, target='highest'),
#     )(data)
