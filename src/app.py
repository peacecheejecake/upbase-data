from typing import Tuple, Optional
import os
from datetime import datetime
from fastapi import FastAPI
import numpy as np

from forecast import DataLoader, Trainer, ModelBase, RandomForestModel, XGBModel, Dataset
from utils.backup import save_parquet, load_parquet
from utils.datetime import kst_time

# app = FastAPI()

class App:
  
  app: FastAPI
  model: XGBModel
  trainer: Trainer
  
  # async def __init__(self):
  #   await self.initialize()
    
  async def initialize(self):
    self.prepare_model()
    
    self.prepare_trainer()
    self.trainer.train()
    
    print(self.model.feature_importances())
    
    self.trainer.load_model(self.model_compared)
    self.trainer.train()
    
    self.app = FastAPI()
    print('Initialized')
    
  def prepare_model(self):
    # self.model = RandomForestModel()
    self.model = XGBModel()
    self.model_compared = RandomForestModel()
  
  def prepare_trainer(self):
    # X, y = await self.load_candle_data('IOTA_1s_2000000_2025-01-05T18:19:37+09:00.parquet_20250105181937.parquet')
    X, y = self.load_candle_data()
    self.trainer = Trainer(self.model, Dataset(X, y), valid_ratio=0.15)
    
  def load_candle_data(self, file_name: Optional[str] = None) -> Tuple[np.ndarray, np.ndarray]:
    data = None
    
    if file_name:
      data = load_parquet(file_name)
    
    if data is None:
      count = 2000
      data = DataLoader.load_candles(
        market='KRW-IOTA', 
        unit='second', 
        count=count,
        # to='2024-10-15T18:19:37+09:00',
      )
      data = DataLoader.preprocess(data)
      
      print(f"Data period: {data.iloc[0]['candle_date_time_kst']} - {data.iloc[-1]['candle_date_time_kst']}")
      save_parquet(data, file_name=f'IOTA_1s_{count}_{kst_time()}.parquet')
    
    X, y = DataLoader.make_input_output(
      data,
      columns_X=[
        'variance', 
        # 'best_profit_rate_before',
        'worst_profit_rate_before', 
        'opening_price', 
        'high_price', 
        'mid_price', 
        'low_price', 
        'candle_acc_trade_volume', 
        # 'diff_opening_price',
        # 'diff_high_price',
        # 'diff_mid_price',
        # 'diff_low_price', 
        # 'diff_candle_acc_trade_volume',
        'timedelta_after',
      ], 
      columns_y=['best_profit_rate'],
    )
    return X, y
  
  async def predict_now(self):
    data = DataLoader.load_candles(
      market='KRW-IOTA', 
      unit='second', 
      count=200000
    )

# async def initialize_app() -> FastAPI:
#   app = FastAPI()
#   return app
