import pandas as pd
import statsmodels.api as sm


class OLS:

    @staticmethod
    def my_ols_model(y_input, x_input):
        return sm.OLS(y_input, sm.add_constant(x_input)).fit()
