import pandas as pd
import numpy as np
import os

ui_path = os.path.dirname(os.path.abspath(__file__))
test_dataset_location = os.path.join(ui_path, "test_dataset/test_user_input_datasheet.csv")

# def import_csv(loc):
#     df = pd.read_csv(loc)
#     df = pd.DataFrame(df)
#     df = df.set_index('Date')
    
#     user_input_header = df[:0]
#     print(user_input_header)

def import_csv(loc):
    df = pd.read_csv(loc)
    csv_header_list = list(df)
    csv_index = csv_header_list.pop(0)
    df = pd.DataFrame(df)
    for headers in csv_header_list:
        csv_series = df.loc[:,[csv_index,headers]]
        csv_series = csv_series.set_index(csv_index)
        print(csv_series)
    
    print(csv_header_list)
    print(csv_index)

import_csv(test_dataset_location)