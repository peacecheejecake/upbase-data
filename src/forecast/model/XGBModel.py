import xgboost as xgb
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import numpy as np
import pandas as pd

from .ModelBase import ModelBase
from ..typings import InputType, OutputType, Score

class XGBModel(ModelBase):
  
  model: xgb.XGBRegressor
  
  def initilize_model(self):
    self.model = xgb.XGBRegressor(
      base_score=0.5,
      booster='gbtree',
      n_estimators=1000,
      early_stopping_rounds=50,
      objective='reg:squarederror',
      max_depth=3,
      learning_rate=0.01
    )

  def train(self, X: InputType, y: OutputType, X_test: InputType, y_test: OutputType):
    self.model.fit(
      X, 
      y,
      eval_set=[(X, y), (X_test, y_test)],
      verbose=False
    )

  def predict(self, X: InputType) -> OutputType:
    return self.model.predict(np.array(X))

  def test(self, X: InputType, y: OutputType) -> Score:
    y_preds = self.predict(X)

    print(f'R2 Score: {r2_score(y, y_preds)}')
    print(f'MAE: {mean_absolute_error(y, y_preds)}')
    print(f'MSE: {mean_squared_error(y, y_preds)}')
    
    # print(pd.DataFrame(data=[y, y_preds], index=['y', 'y_pred']).T)

    return self.model.score(
      X,
      y
    )
    
  def feature_importances(self):
    fi = pd.DataFrame(
      data=self.model.feature_importances_,
      # index=self.model.feature_names_in_,
      columns=['importance'])
    # fi.sort_values('importance')
    return fi
  


# https://www.kaggle.com/code/robikscube/time-series-forecasting-with-machine-learning-yt#Using-Machine-Learning-to-Forecast-Energy-Consumption
# reg = xgb.XGBRegressor(base_score=0.5, booster='gbtree',    
#                        n_estimators=1000,
#                        early_stopping_rounds=50,
#                        objective='reg:linear',
#                        max_depth=3,
#                        learning_rate=0.01)
# reg.fit(X_train, y_train,
#         eval_set=[(X_train, y_train), (X_test, y_test)],
#         verbose=100)