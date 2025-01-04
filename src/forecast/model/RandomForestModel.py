from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import numpy as np

from .ModelBase import ModelBase
from ..typings import InputType, OutputType, Score

from sklearn.ensemble import RandomForestRegressor

class RandomForestModel(ModelBase):
    
    def initilize_model(self):
        self.model = RandomForestRegressor()

    def train(self, X: InputType, y: OutputType):
        self.model.fit(X, y)

    def predict(self, X: InputType) -> OutputType:
        return self.model.predict(np.array(X))

    def test(self, X: InputType, y: OutputType) -> Score:
        y_preds = self.predict(X)

        print(f'R2 Score: {r2_score(y, y_preds)}')
        print(f'MAE: {mean_absolute_error(y, y_preds)}')
        print(f'MSE: {mean_squared_error(y, y_preds)}')

        return self.model.score(
            X,
            self.predict(X)
        )
