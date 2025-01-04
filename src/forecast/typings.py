from typing import TypeVar, Union
import numpy as np
import pandas as pd

T = TypeVar('T')
InputType = Union[pd.DataFrame, np.ndarray]
OutputType = Union[pd.DataFrame, pd.Series, np.ndarray]

Score = Union[float, np.floating]
