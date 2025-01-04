from abc import ABCMeta, abstractmethod
from ..typings import InputType, OutputType, Score

class ModelBase(metaclass=ABCMeta):
    
    def __init__(self):
        self.initilize_model()

    @abstractmethod
    def initilize_model(self):
        pass

    @abstractmethod
    def train(self, X: InputType, y: OutputType):
        pass

    @abstractmethod
    def predict(self, X: InputType) -> OutputType:
        pass

    @abstractmethod
    def test(self, X: InputType, y: OutputType) -> Score:
        pass






    # def pick_data(self, data: pd.DataFrame, columns: list):
    #     return data.loc[:, columns]

    # def make_data(self, X, y, test_size=0.2):
    #     X_train, X_test, y_train, y_test = train_test_split(
    #       np.array(X),
    #       np.array(y).reshape(-1),
    #       test_size=test_size
    #     )

    #     self.X_train = X_train
    #     self.X_test = X_test
    #     self.y_train = y_train
    #     self.y_test = y_test

        # return (X_train, X_test, y_train, y_test)

    # def train(self):
    #     self.model.fit(self.X_train, self.y_train)

    # def predict(self, X=None):
    #     if X is None:
    #         X = self.X_test

    #     return self.model.predict(X)

    # def score(self):
    #     y_preds = self.predict(self.X_test)
    #     print(f'R2 Score: {r2_score(self.y_test, y_preds)}')
    #     print(f'MAE: {mean_absolute_error(self.y_test, y_preds)}')
    #     print(f'MSE: {mean_squared_error(self.y_test, y_preds)}')
    #     return self.model.score(
    #         self.X_test,
    #         self.predict(self.X_test)
    #     )