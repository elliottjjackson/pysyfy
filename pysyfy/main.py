import datetime
import os
import timeit
from typing import Any, Dict, List

import matplotlib.pyplot as plt
import pandas as pd
from ArimaModel import ArimaModel
from base_classes import FormalCSVImport
from pandas_datareader import data

plt.style.use("fivethirtyeight")

start_timer = timeit.default_timer()


def absolute_path(rel_path: str) -> str:
    ui_path = os.path.dirname(os.path.abspath(__file__))
    result = os.path.join(ui_path, rel_path)
    return result


user_input_dataset_path = absolute_path("../dataset/user_input_datasheet.csv")
historic_house_price_dataset_path = absolute_path(
    "../dataset/historic_house_price.csv"
)
simulated_house_price_dataset_path = absolute_path(
    "../dataset/simulated_house_price.csv"
)
historic_CPI_dataset_path = absolute_path("../dataset/historic_CPI.csv")
simulated_interest_rate_dataset_path = absolute_path(
    "../dataset/simulated_interest_rates.csv"
)
historic_interest_rate_dataset_path = absolute_path(
    "../dataset/historic_interest_rates.csv"
)
LMI_dataset_path = absolute_path("../dataset/LMI.csv")

user_data_map = [
    "date",
    "cpi",
    "salary",
    "sti",
    "lti",
    "balance_adjustment_at",
    "salary_witheld",
    "sti_witheld",
    "lti_witheld",
    "living_expenditure",
    "home_loan_repayments",
    "home_loan_fees",
    "home_loan_interest_rate",
    "rental_income",
    "rental_costs",
    "shares_purchased",
    "share_price",
    "unfranked_dividends",
    "franked_dividends",
]
historic_house_price_map = ["date", "historic_house_price"]
simulated_house_price_map = ["date", "simulated_house_price"]
historic_CPI_map = ["date", "CPI"]
LMI_map = ["LVR", ">300K", "300K-500K", "500K-600K", "600K-750K", "750K-1M"]
# LVR - Loan to Value Ratio, lower bound does not including the value. e.g.
# $300,001 - $500,000
historic_interest_rate_map = [
    "date",
    "historic_current_home_loan_interest_rate",
    "aus_historic_variable_home_loan_interest_rate",
    "adjusted_aus_variable_home_loan_interest_rate",
    "historic_HISA_rate",
]
simulated_interest_rate_map = [
    "date",
    "simulated_current_home_loan_interest_rate",
    "simulated_HISA_rate",
]


class CSVImport(FormalCSVImport):
    def __init__(self, path: str, map: List[str]) -> None:
        # latin1 encoding required over utf-8
        self.user_input_df = pd.read_csv(path, encoding="latin1")
        # Set 'Date' as the row index and
        # extract the 'units declaration' row
        self.units_series = self.user_input_df.loc[0, :]
        self.user_input_df = self.user_input_df.drop([0])
        self.header_list = list(self.user_input_df)

        # Standardise dataframe column names
        self.user_input_df.columns = map

        self.user_input_df = self.user_input_df.set_index(map[0])

    def get(self) -> pd.DataFrame:
        return self.user_input_df

    def display_headers(self) -> None:
        print(self.header_list)

    def display_units(self) -> None:
        print(self.units_series)


class HistoricStockPrice:
    def __init__(self, ticker: List[str], start_date: str, end_date: str):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        # Data reader connects to a source and displays stock data between dates.
        # Sources: https://pandas-datareader.readthedocs.io/en/latest/remote_data.html
        self.panel_data = data.DataReader(
            ticker, "stooq", start_date, end_date
        )

    def get(self) -> pd.DataFrame:
        """Return dataframe of defined tickers. +1.8 seconds to run time"""
        return self.panel_data

    def forecast_format(self) -> pd.DataFrame:
        """For future: Rewrite code to be dynamic for different headers"""
        self.panel_data.drop(
            ["Close", "High", "Low", "Volume"], axis=1, inplace=True
        )
        # panel_data = panel_data.sort_values('Open')
        self.panel_data.columns = ["Open"]
        self.panel_data = self.panel_data.resample("MS").mean()
        return self.panel_data


def get_external_data() -> None:
    ticker = ["SDY"]
    start_date = "2010/01/01"
    end_date = "2021/01/01"

    user_data = CSVImport(user_input_dataset_path, user_data_map)
    user_data_table = user_data.get()
    historic_house_price = CSVImport(
        historic_house_price_dataset_path, historic_house_price_map
    )
    historic_house_price_table = historic_house_price.get()
    simulated_house_price = CSVImport(
        simulated_house_price_dataset_path, simulated_house_price_map
    )
    simulated_house_price_table = simulated_house_price.get()
    historic_CPI = CSVImport(historic_CPI_dataset_path, historic_CPI_map)
    historic_CPI_table = historic_CPI.get()
    simulated_interest_rate = CSVImport(
        simulated_interest_rate_dataset_path, simulated_interest_rate_map
    )
    simulated_interest_rate_table = simulated_interest_rate.get()
    historic_interest_rate = CSVImport(
        historic_interest_rate_dataset_path, historic_interest_rate_map
    )
    historic_interest_rate_table = historic_interest_rate.get()
    LMI_object = CSVImport(LMI_dataset_path, LMI_map)
    LMI_table = LMI_object.get()

    stocks = HistoricStockPrice(ticker, start_date, end_date)
    stock_historic = stocks.forecast_format()
    match_start_date = "2019/01/01"
    stock_arima_model = ArimaModel(stock_historic, match_start_date, 150)
    stock_forecast = stock_arima_model.get_forecast()
    stock_arima_model.plot_decomposition()
    stock_arima_model.print_arima_summary_table()
    stock_arima_model.plot_arima_diagnostics()
    stock_arima_model.plot_history_match()
    stock_arima_model.plot_forecast()


class StrategyConstructor:
    """Generates dictionary with example type:
    {
    'strategy_name': ['strat_1_stocks',
    'strat_2_stocks',
    'strat_1_home',
    'strat_1_property',
    'strat_2_property]

    'strategy_type': ['stocks',
    'stocks',
    'home',
    'property',
    'property']
    }
    """

    def __init__(self, user_strategy_input: Dict[str, int]) -> None:
        # replace user_strategy_input with user input functionality
        strategy_object_dict: Dict[str, List[str]] = {
            "strategy_name": [],
            "strategy_type": [],
        }
        self.strategy_object_dict = strategy_object_dict
        self.user_strategy_input = user_strategy_input

    def _add(self, number_of_strats: int, strat_type: str) -> None:
        for num in range(number_of_strats):
            self.strategy_object_dict["strategy_name"].append(
                "strat_" + str(num + 1) + "_" + strat_type
            )
            self.strategy_object_dict["strategy_type"].append(strat_type)

    def add_stocks(self) -> None:
        self._add(self.user_strategy_input["stocks"], "Stocks")

    def add_house(self) -> None:
        self._add(self.user_strategy_input["home"], "Home")

    def add_property(self) -> None:
        self._add(self.user_strategy_input["property"], "Property")

    def print_strategies(self) -> None:
        print(pd.DataFrame(self.strategy_object_dict))


class BankAccountContructor:
    def __init__(self) -> None:
        bankaccounts_object_dict: Dict[str, List[Any]] = {
            "account_name": [],
            "account_type": [],
            "balance": [],
        }
        self.bankaccounts_object_dict = bankaccounts_object_dict

    def create_account(self, name: str, type: str, balance: float) -> None:
        self.bankaccounts_object_dict["account_name"].append(name)
        self.bankaccounts_object_dict["account_type"].append(type)
        self.bankaccounts_object_dict["balance"].append(balance)

    def print_bankaccounts(self) -> None:
        print(pd.DataFrame(self.bankaccounts_object_dict))


tax_regime_list: List[str] = []


class TaxRegimeClass:
    def __init__(self, financial_year: int) -> None:
        self.financial_year = int(financial_year)
        try:
            tax_regime_list.index(str(self.financial_year))
        except ValueError:
            tax_regime_list.append(str(self.financial_year))

    def start_date(self) -> datetime.datetime:
        return datetime.datetime(self.financial_year, 7, 1)

    def end_date(self) -> datetime.datetime:
        return datetime.datetime(self.financial_year + 1, 7, 1)


def initialise_bankaccounts() -> BankAccountContructor:
    bankaccounts = BankAccountContructor()
    bankaccounts.create_account("Home Loan", "Mortgage", -50_000)
    bankaccounts.create_account(
        "Investment Property 1 Mortgage", "Mortgage", -20_000
    )
    bankaccounts.create_account("Savings Account", "HISA", 40_000)
    return bankaccounts


def create_strategy(
    strategy_input_table: Dict[str, int]
) -> StrategyConstructor:
    strategy = StrategyConstructor(strategy_input_table)
    strategy.add_house()
    strategy.add_property()
    strategy.add_stocks()
    return strategy
    # strategy.save


def select_tax_calculations(year: int) -> TaxRegimeClass:
    tax_regime_FY20 = TaxRegimeClass(2020)  # prevent copies of the same class
    return tax_regime_FY20


def calculate_strategy() -> None:
    # timeseries = TimeSeries()
    # history_match = HistoryMatch()
    # forecast = Forecast()
    pass


if __name__ == "__main__":
    get_external_data()
    user_strategy_input = {"home": 1, "stocks": 2, "property": 2}
    strategy = create_strategy(user_strategy_input)
    strategy.print_strategies()
    bankaccounts = initialise_bankaccounts()
    bankaccounts.print_bankaccounts()
    tax_regime_FY20 = select_tax_calculations(2020)
    # calculate_strategy()
    # dashboard.update
    # dashboard.display
    # save_state()

    stop_timer = timeit.default_timer()


print("Time: ", stop_timer - start_timer)
