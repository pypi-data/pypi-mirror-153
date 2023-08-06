from numpy import ndarray
from pandas import Series
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from vteklib.regressions.regression import Regression
from abc import ABC
import numpy as np


class Poly(Regression, ABC):
    def __init__(self):
        self.reg = make_pipeline(PolynomialFeatures(), Ridge(alpha=1e-3))
        self.equation = 'polynomial y(x)'

    def fit(self, x_data: Series, y_data: Series):
        self.reg.fit(np.matrix(x_data).T.A, y_data)

    def predict(self, x_data) -> ndarray:
        return self.reg.predict(np.matrix(x_data).T.A)

    @classmethod
    def __repr__(cls):
        return 'polynomial'

