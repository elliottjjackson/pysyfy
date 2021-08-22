import itertools
import numpy as np
import matplotlib.pyplot as plt

plt.style.use("fivethirtyeight")
import pandas as pd
import statsmodels.api as sm
import matplotlib
import warnings

warnings.filterwarnings("ignore")


class ArimaModel:
    """Monthly model. Takes pandas dataframes with monthly timesteps
    Returns the forecast as a time series dataframe"""

    def __init__(self, df, match_start_date, forecast_steps):
        self.df = df
        self.match_start_date = match_start_date
        self.forecast_steps = forecast_steps
        # Resample to monthly
        self.df = self.df.resample("MS").mean()
        # Generate trend data
        self.decomposition = sm.tsa.seasonal_decompose(self.df, model="additive")
        # Generate history match
        p = d = q = range(0, 2)
        pdq = list(itertools.product(p, d, q))
        seasonal_pdq = [(x[0], x[1], x[2], 12) for x in pdq]
        self.param_dict = {"param": None, "param_seasonal": None, "result.aic": None}
        for param in pdq:
            for param_seasonal in seasonal_pdq:
                try:
                    # Mimimum error match using Autoregressive integrated moving average (ARIMA)
                    mod = sm.tsa.statespace.SARIMAX(
                        self.df,
                        order=param,
                        seasonal_order=param_seasonal,
                        enforce_invertibility=False,
                    )
                    result = mod.fit(disp=0)
                    print(f"ARIMA{param}x{param_seasonal} - AIC: {result.aic}")
                    if (
                        self.param_dict["result.aic"] == None
                        or result.aic < self.param_dict["result.aic"]
                    ):
                        self.param_dict.update([("param", param)])
                        self.param_dict.update([("param_seasonal", param_seasonal)])
                        self.param_dict.update([("result.aic", result.aic)])
                except:
                    continue
        model = sm.tsa.statespace.SARIMAX(
            self.df,
            order=self.param_dict["param"],
            seasonal_order=self.param_dict["param_seasonal"],
            enforce_invertibility=False,
        )
        self.arima_model = model.fit()
        self.history_match = self.arima_model.get_prediction(
            start=pd.to_datetime(self.match_start_date), dynamic=False
        )
        self.forecast = self.arima_model.get_forecast(steps=self.forecast_steps)

    def get_forecast(self):
        return self.forecast.predicted_mean

    def plot_decomposition(self):
        fig = self.decomposition.plot()
        plt.show()

    def print_arima_summary_table(self):
        print(self.arima_model.summary().tables[1])

    def plot_arima_diagnostics(self):
        self.arima_model.plot_diagnostics(figsize=(15, 8))
        plt.show()

    def plot_history_match(self):
        pred_ci = self.history_match.conf_int()
        ax = self.df.plot(label="Observed", figsize=(14, 7))
        self.history_match.predicted_mean.plot(
            ax=ax, label="One-step ahead Forecast", alpha=0.7, figsize=(14, 7)
        )
        ax.fill_between(
            pred_ci.index, pred_ci.iloc[:, 0], pred_ci.iloc[:, 1], color="k", alpha=0.2
        )

        ax.set_xlabel = "Date"
        ax.set_ylabel = "Open Price"
        plt.legend()
        plt.show()

    def plot_forecast(self):
        pred_ci = self.forecast.conf_int()
        ax = self.df.plot(label="Observed", figsize=(14, 7))
        self.forecast.predicted_mean.plot(ax=ax, label="Forecast")
        ax.fill_between(
            pred_ci.index, pred_ci.iloc[:, 0], pred_ci.iloc[:, 1], color="k", alpha=0.25
        )
        ax.set_xlabel = "Date"
        ax.set_ylabel = "Open Price"
        # plt.yscale('log')
        plt.legend()
        plt.show()
