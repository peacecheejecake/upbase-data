from typing import Dict, Optional, Literal
from dataclasses import dataclass
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split

from .model.ModelBase import ModelBase
from .typings import InputType, OutputType


@dataclass
class Dataset:
  X: InputType
  y: OutputType

  def __getitem__(self, key: Literal['X', 'y']):
    return self[key]
  
  def __setitem__(self, name, value):
    self[name] = value
  

class Trainer:

  model: ModelBase
  # data: pd.DataFrame
  data: Dataset
  data_splits: Dict[Literal['train', 'valid'], Dataset]

  def __init__(self, model: Optional[ModelBase] = None, data: Optional[Dataset] = None):
    if model:
      self.load_model(model)

    if data:
      self.load_data(data)
    
  def load_model(self, model: ModelBase):
    self.model = model

  def load_data(self, data: Dataset):
    self.data = data
    self.split_train_valid_data()

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
    self.model.train(self.data_splits['train']['X'], self.data_splits['train']['y'])

  def test(self, X: InputType, y: OutputType):
    return self.model.test(X, y)

  def validate(self):
    return self.test(self.data_splits['valid']['X'], self.data_splits['valid']['y'])
