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

print(f"Last Data: {last_data.date}")
last_data.print_stats_report()

print("\nTOTAL")
print(f"total value      : £ {round(last_data.get_total_value(), 2)}")
print(f"total (w/o cash) : £ {round(last_data.get_total_value(include_cash=False), 2)}")
print(f"sum div.         : £ {round(last_data.get_dividends_total(), 2)}")
print(f"div. ratio       : {round(last_data.get_dividends_average_rate() * 100, 2)} %")
print(f"div. exp.        : £ {round(last_data.get_dividends_expectation(), 2)}")



print("END")