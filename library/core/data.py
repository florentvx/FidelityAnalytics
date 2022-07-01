import numpy as np
import pandas as pd
import datetime as dt

from .transaction_type import get_transation_type
from .asset import asset
from .history import history

def convert_numpy_nan(x):
    if x is np.nan:
        return None
    return x

def get_fidelity_data(csv_path: str) -> history:
    
    data = pd.read_csv(csv_path)
    new_data = pd.DataFrame()
    
    # date
    new_data["date"] = data["Completion date"].apply(lambda x: dt.datetime.strptime(x, '%d %b %Y').date())
    
    # transaction_type
    new_data["transaction_type"] = data["Transaction type"].apply(lambda x: get_transation_type(x))

    # asset
    new_data["asset"] = data.apply(
        lambda row: 
            asset(
                row["Investments"], 
                row["Amount"], 
                row["Quantity"], 
                row["Price per unit"]
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
        )

    return hist_data

