from typing import Dict, Optional, Literal, Union, TypeVar
from dataclasses import dataclass
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split

from utils.functools import chain
from .model.ModelBase import ModelBase
from .typings import InputType, OutputType


@dataclass
class Dataset:
  __store = {
    'X': InputType, 
    'y': OutputType
  }

  def __init__(self, X: InputType, y: OutputType):
    self.__store = {
      'X': X,
      'y': y,
    }

  @property
  def X(self):
    return self.__store['X']
  
  @property
  def y(self):
    return self.__store['y']

  def __getitem__(self, key: Literal['X', 'y']):
    return self.__store[key]
  
  def __setitem__(self, key, value):
    self.__store[key] = value
      

class Trainer:

  model: ModelBase
  # data: pd.DataFrame
  data: Dataset
  data_splits: Dict[Literal['train', 'valid'], Dataset]
  valid_ratio: float

  def __init__(
    self, 
    model: Optional[ModelBase] = None, 
    data: Optional[Dataset] = None,
    valid_ratio=0.2,
  ):
    self.valid_ratio = valid_ratio

    if model:
      self.load_model(model)

    if data:
      self.load_data(data)
    
  def load_model(self, model: ModelBase):
    self.model = model

  def load_data(self, data: Dataset):
    self.data = data
    self.split_train_valid_data(self.valid_ratio)

  def split_train_valid_data(self, test_size=0.2):
    X_train, X_test, y_train, y_test = train_test_split(
      np.array(self.data.X),
      np.array(self.data.y).reshape(-1),
      test_size=test_size
    )

    self.data_splits = {
      'train': Dataset(X_train, y_train),
      'valid': Dataset(X_test, y_test),
      # 'X_train': X_train,
      # 'X_test': X_test,
      # 'y_train': y_train,
      # 'y_test': y_test
    }

    # self.X_train = X_train
    # self.X_test = X_test
    # self.y_train = y_train
    # self.y_test = y_test

  def train(self):
    print('Start training')
    self.model.train(self.data_splits['train']['X'], self.data_splits['train']['y'])

  def test(self, X: InputType, y: OutputType):
    return self.model.test(X, y)

  def validate(self):
    return self.test(self.data_splits['valid']['X'], self.data_splits['valid']['y'])
