import pandas as pd
import numpy as np
import os
from pandas_datareader import data
import timeit
import itertools
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import statsmodels.api as sm
import matplotlib
from ArimaModel import ArimaModel
from base_classes import FormalCSVImport


start_timer = timeit.default_timer()

def absolute_path(rel_path: str):
    ui_path = os.path.dirname(os.path.abspath(__file__))
    result = os.path.join(ui_path, rel_path)
    return result

user_input_dataset_path = absolute_path("dataset/user_input_datasheet.csv")
historic_house_price_dataset_path = absolute_path("dataset/historic_house_price.csv")
simulated_house_price_dataset_path = absolute_path("dataset/simulated_house_price.csv")
historic_CPI_dataset_path = absolute_path("dataset/historic_CPI.csv")
simulated_interest_rate_dataset_path = absolute_path("dataset/simulated_interest_rates.csv")
historic_interest_rate_dataset_path = absolute_path("dataset/historic_interest_rates.csv")
LMI_dataset_path = absolute_path("dataset/LMI.csv")

user_data_map = ['date', 'cpi', 'salary', 
        'sti', 'lti', 'balance_adjustment_at', 
        'salary_witheld', 'sti_witheld', 'lti_witheld', 
        'living_expenditure', 'home_loan_repayments', 'home_loan_fees', 
        'home_loan_interest_rate', 'rental_income', 'rental_costs', 
        'shares_purchased', 'share_price', 'unfranked_dividends', 
        'franked_dividends']
historic_house_price_map = ['date','historic_house_price']
simulated_house_price_map = ['date','simulated_house_price']
historic_CPI_map = ['date','CPI']
LMI_map = ['LVR','>300K','300K-500K','500K-600K','600K-750K','750K-1M']
#LVR - Loan to Value Ratio, lower bound does not including the value. e.g. $300,001 - $500,000
historic_interest_rate_map = ['date','historic_current_home_loan_interest_rate',
'aus_historic_variable_home_loan_interest_rate','adjusted_aus_variable_home_loan_interest_rate',
'historic_HISA_rate']
simulated_interest_rate_map = ['date','simulated_current_home_loan_interest_rate','simulated_HISA_rate']


class CSVImport(FormalCSVImport):

    def __init__(self, path: str, map: list):
        self.user_input_df = pd.read_csv(path)
        #Set 'Date' as the row index and extract the 'units declaration' row.
        self.units_series = self.user_input_df.loc[0,:]
        self.user_input_df = self.user_input_df.drop([0])
        self.header_list = list(self.user_input_df)

        #Standardise dataframe column names
        self.user_input_df.columns = map

        self.user_input_df = self.user_input_df.set_index(map[0])

    def get(self):
        return self.user_input_df

    def display_headers(self):
        print(self.header_list)

    def display_units(self):
        print(self.units_series)

class HistoricStockPrice:
    def __init__(self,ticker: list,start_date,end_date):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        # Data reader connects to a source and displays stock data between dates.
        #Sources: https://pandas-datareader.readthedocs.io/en/latest/remote_data.html
        self.panel_data = data.DataReader(ticker,'stooq',start_date,end_date)

    def get(self):
        """ Return dataframe of defined tickers. +1.8 seconds to run time """
        return self.panel_data

    def forecast_format(self):
        """For future: Rewrite code to be dynamic for different headers"""
        self.panel_data.drop(['Close','High','Low','Volume'],axis=1,inplace=True)
        # panel_data = panel_data.sort_values('Open')
        self.panel_data.columns = ['Open']
        self.panel_data = self.panel_data.resample('MS').mean()
        return self.panel_data

def get_external_data():
    ticker = ['SDY']
    start_date = '2010/01/01'
    end_date = '2021/01/01'

    user_data = CSVImport(user_input_dataset_path,user_data_map)
    user_data_table = user_data.get()
    historic_house_price = CSVImport(historic_house_price_dataset_path,historic_house_price_map)
    historic_house_price_table = historic_house_price.get()
    simulated_house_price = CSVImport(simulated_house_price_dataset_path,simulated_house_price_map)
    simulated_house_price_table = simulated_house_price.get()
    historic_CPI = CSVImport(historic_CPI_dataset_path,historic_CPI_map)
    historic_CPI_table = historic_CPI.get()
    simulated_interest_rate = CSVImport(simulated_interest_rate_dataset_path,simulated_interest_rate_map)
    simulated_interest_rate_table = simulated_interest_rate.get()
    historic_interest_rate = CSVImport(historic_interest_rate_dataset_path,historic_interest_rate_map)
    historic_interest_rate_table = historic_interest_rate.get()
    LMI_object = CSVImport(LMI_dataset_path,LMI_map)
    LMI_table = LMI_object.get()

    stocks = HistoricStockPrice(ticker,start_date,end_date)
    stock_historic = stocks.forecast_format()
    match_start_date = '2019/01/01'
    # stock_arima_model = ArimaModel(stock_historic,match_start_date,150)
    # stock_forecast = stock_arima_model.get_forecast()
    # stock_arima_model.plot_decomposition()
    # stock_arima_model.print_arima_summary_table()
    # stock_arima_model.plot_arima_diagnostics()
    # stock_arima_model.plot_history_match()
    # stock_arima_model.plot_forecast()

def create_strategy():
    strategy = Strategy()
    strategy.save

def initialise_bank_accounts():
    pass

def select_tax_calculations():
    tax_calculation_set = TaxCalculations()

def calculate_strategy():
    timeseries = TimeSeries()
    history_match = HistoryMatch()
    forecast = Forecast()

get_external_data()
# create_strategy()
# calculate_strategy()
# dashboard.update
# dashboard.display

# save_state()

stop_timer = timeit.default_timer()


print('Time: ',stop_timer - start_timer)