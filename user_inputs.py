import pandas as pd
import numpy as np
import os

ui_path = os.path.dirname(os.path.abspath(__file__))
test_dataset_location = os.path.join(ui_path, "test_dataset/test_user_input_datasheet.csv")

user_input_df = pd.read_csv(test_dataset_location)

#Set 'Date' as the row index and extract the 'units declaration' row.
user_input_df.set_index('Date')
units_series = user_input_df.loc[0,:]
df = user_input_df.drop([0])
header_list = list(user_input_df)

#Standardise dataframe column names
df.columns = ['date', 'cpi', 'salary', 
'sti', 'lti', 'balance_adjustment_at', 
'salary_witheld', 'sti_witheld', 'lti_witheld', 
'living_expenditure', 'home_loan_repayments', 'home_loan_fees', 
'home_loan_interest_rate', 'rental_income', 'rental_costs', 
'shares_purchased', 'share_price', 'unfranked_dividends', 
'franked_dividends']

print(units_series)
print(user_input_df)
print(header_list)