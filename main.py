import pandas as pd
import numpy as np


years = ['2018A','2019B','2020P','2021P','2022P','2023P']
sales = pd.Series(index=years)
sales['2018A'] = 31.0
print(sales)