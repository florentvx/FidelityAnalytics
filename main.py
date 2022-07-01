from library import *

my_path = r'C:\Users\flore\source\repos\FidelityAnalytics\data\TransactionHistory_20220603.csv'

fidelity_data = get_fidelity_data(my_path)

last_data = fidelity_data.get_last()

print(f"\nLast Data: {last_data.date}\n")

last_data.print_stats_report()

last_data.print_total_stats_report()

plot_timeseries(last_data.get_allocation_asset("ISHARES, FTSE 250 UCITS ETF GBP DIST (MIDD)").dividends_ratio)

print("\nEND")