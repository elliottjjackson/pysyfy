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

ui_path = os.path.dirname(os.path.abspath(__file__))
user_input_dataset_path = os.path.join(ui_path, "dataset/user_input_datasheet.csv")
historic_house_price_input_dataset_path = os.path.join(ui_path, "dataset/historic_house_price.csv")

class UserData(FormalCSVImport):

    def __init__(self, path: str):
        self.user_input_df = pd.read_csv(path)
        #Set 'Date' as the row index and extract the 'units declaration' row.
        self.units_series = self.user_input_df.loc[0,:]
        self.user_input_df = self.user_input_df.drop([0])
        self.header_list = list(self.user_input_df)

        #Standardise dataframe column names
        self.user_input_df.columns = ['date', 'cpi', 'salary', 
        'sti', 'lti', 'balance_adjustment_at', 
        'salary_witheld', 'sti_witheld', 'lti_witheld', 
        'living_expenditure', 'home_loan_repayments', 'home_loan_fees', 
        'home_loan_interest_rate', 'rental_income', 'rental_costs', 
        'shares_purchased', 'share_price', 'unfranked_dividends', 
        'franked_dividends']

        self.user_input_df = self.user_input_df.set_index('date')

    def get(self):
        return self.user_input_df

    def display_headers(self):
        print(self.header_list)

    def display_units(self):
        print(self.units_series)

class HistoricHousePrice(FormalCSVImport):
    def __init__(self,path):
        self.historic_house_price = pd.read_csv(path)
        self.units_series = self.historic_house_price.loc[0,:]
        self.historic_house_price = self.historic_house_price.drop([0])
        self.header_list = list(self.historic_house_price)

        #Standardise dataframe column names
        self.historic_house_price.columns = ['date','historic_house_price']

        self.historic_house_price = self.historic_house_price.set_index('date')

    def get(self):
        return self.historic_house_price

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
    user_data = UserData(user_input_dataset_path)
    user_data_table = user_data.get()
    historic_house_price = HistoricHousePrice(historic_house_price_input_dataset_path)
    historic_house_price_table = historic_house_price.get()
    stocks = HistoricStockPrice(ticker,start_date,end_date)
    stock_historic = stocks.forecast_format()
    match_start_date = '2019/01/01'
    # stock_arima_model = ArimaModel(stock_historic,match_start_date,150)
    # stock_forecast = stock_arima_model.get_forecast()
    # house_price = HistoricHousePrice.get
    # CPI = HistoricCPI.get
    # mortgage_interest = BankLoanInterestRate.get_mortgage_rate
    # HISA_interest = BankLoanInterestRate.get_HISA_rate
    # LMI = LMIRate.get

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