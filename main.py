from re import A
import pandas as pd
import numpy
import datetime

from core import transaction_type, asset, get_transation_type, history
from core.allocation import allocation_item
from core.data import get_fidelity_data
from core.timeseries import timeseries

my_path = r'C:\Users\flore\source\repos\FidelityAnalytics\data\TransactionHistory_20220603.csv'

fidelity_data = get_fidelity_data(my_path)

last_data = fidelity_data.get_last()

for asset_name in last_data.get_allocation_asset_list():
    asset_item : allocation_item = last_data.get_allocation_asset(asset_name)
    ts_div: timeseries = asset_item.dividends
    print(ts_div)

print("END")