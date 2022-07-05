import numpy as np
import pandas as pd
import datetime as dt
import csv

from .transaction_type import get_transation_type
from .asset import asset
from .history import history

def get_csv_path(
    user:           str,
    date_csv:       dt.date,
    main_folder:    str = None,
    name:           str = None,
    ):
    mf = main_folder
    if main_folder is None:
        mf = r'C:\Users\flore\OneDrive\Documents\FidelityData'
    if name is None:
        name = "TransactionHistory"
    date_month = str(date_csv.month)
    if date_csv.month < 10:
        date_month = "0" + date_month
    date_day = str(date_csv.day)
    if date_csv.day < 10:
        date_day = "0" + date_day
    return mf + f"\\{user}\\{name}_{date_csv.year}{date_month}{date_day}.csv"

def convert_numpy_nan(x):
    if x is np.nan:
        return None
    if x == '':
        return None
    return x

def get_fidelity_data(
    csv_path: str,
    print_steps: bool = False,
    ) -> history:
    
    data_csv = None
    with open(csv_path, newline='') as csv_file:
        reader_csv = csv.reader(csv_file, delimiter=',')
        data_csv = [row for row in reader_csv]
    last_line_len = len(data_csv[-1])
    data_csv = [row for row in data_csv if len(row) == last_line_len]
    data = pd.DataFrame(
        data_csv[1:],
        columns=data_csv[0],
    )
    
    new_data = pd.DataFrame()
    
    # date
    new_data["date"] = data["Completion date"].apply(lambda x: dt.datetime.strptime(x, '%d %b %Y').date())
    
    # transaction_type
    new_data["transaction_type"] = data["Transaction type"].apply(lambda x: get_transation_type(x))

    # asset
    new_data["asset"] = data.apply(
        lambda row: 
            asset(
                str(row["Investments"]), 
                float(row["Amount"]), 
                float(row["Quantity"]),
                float(row["Price per unit"]),
                float(row["Price per unit"]),
            ), 
        axis = 1
    )

    # other
    new_data["product_wrapper"] = data["Product Wrapper"]
    new_data["source_investment"] = data["Source investment"].apply(convert_numpy_nan)

    # sort dates    
    new_data = new_data.sort_values(by=["date"])

    hist_data = history()

    for _, row in new_data.iterrows():
        hist_data.add(
            row['date'], 
            row['transaction_type'], 
            row["source_investment"],
            row['asset'],
            print_step = print_steps
        )

    return hist_data

