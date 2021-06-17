import pandas as pd
import numpy as np


timeseries = ['2018A','2019B','2020P','2021P','2022P','2023P']

def get_external_data():
    user_data = UserData.get
    stock_price = HistoricStockPrice.get
    house_price = HistoricHousePrice.get
    CPI = HistoricCPI.get
    mortgage_interest = BankLoanInterestRate.get_mortgage_rate
    HISA_interest = BankLoanInterestRate.get_HISA_rate
    LMI = LMIRate.get

def create_strategy():
    strategy = Strategy()
    strategy.save

def initialise_bank_accounts():

def select_tax_calculations():
    tax_calculation_set = TaxCalculations()

def calculate_strategy():
    timeseries = TimeSeries()
    history_match = HistoryMatch()
    forecast = Forecast()

get_external_data()
create_strategy()
calculate_strategy()
dashboard.update
dashboard.display

save_state()

