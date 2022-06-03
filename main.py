import pandas as pd
import numpy
import datetime

from core import transaction_type, asset, get_transation_type, history

data = pd.read_csv(r'C:\Users\flore\source\repos\FidelityAnalytics\data\TransactionHistory_20220603.csv')

new_data = pd.DataFrame()
new_data["date"] = data["Completion date"].apply(lambda x: datetime.datetime.strptime(x, '%d %b %Y').date())
new_data["transaction_type"] = data["Transaction type"].apply(lambda x: get_transation_type(x))
new_data["asset"] = data.apply(
    lambda row:
        asset(
            row["Investments"], 
            row["Amount"], 
            row["Quantity"], 
            row["Price per unit"]
        ), 
    axis = 1)
new_data["product_wrapper"] = data["Product Wrapper"]
new_data["source_investment"] = data["Source investment"]
tx_type_list = data["Transaction type"].to_list()
tx_type_unique_list = []
for x in tx_type_list:
    if not x in tx_type_unique_list:
        tx_type_unique_list += [x]

print(tx_type_unique_list)

print(new_data.head())

new_data = new_data.sort_values(by=["date"])

hist_data = history()

for index, row in new_data.iterrows():

    date            :datetime.datetime  = row["date"]
    tx_type         :transaction_type   = row["transaction_type"]
    r_asset         :asset              = row["asset"]
    source_inv      :str                = row["source_investment"]
    if source_inv is numpy.nan:
        source_inv = None

    hist_data.add(date, tx_type, source_inv, r_asset)

print("END")