import pandas as pd
import numpy
import datetime

from core import transaction_type, asset, get_transation_type, history
from core.data import get_fidelity_data

my_path = r'C:\Users\flore\source\repos\FidelityAnalytics\data\TransactionHistory_20220603.csv'

fidelity_data = get_fidelity_data(my_path)

print("END")