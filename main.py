from library import *

main_folder = r'C:\Users\flore\GoogleDrive\Fidelity'

''' Inputs '''

user= "florent_vassaux"

date_csv = dt.date(2022, 9, 16)
output_suffix = "TEST"

''' Code '''

main_folder_user = f"{main_folder}\\{user}"
csv_path = get_csv_path(main_folder_user, date_csv, user)
html_path = get_html_path(main_folder_user, date_csv, user, suffix=output_suffix)
pdf_path = get_pdf_path(main_folder_user, date_csv, user, suffix=output_suffix)


fidelity_data = get_fidelity_data(csv_path, print_steps=False)

last_data : history_item = fidelity_data.get_last()

print(f"\nLast Data: {last_data.date}\n")

last_data.print_stats_report()

last_data.print_total_stats_report()

plots = []

for asset_name in last_data.get_allocation_asset_list():

    asset_selected : allocation_item = last_data.get_allocation_asset(asset_name)
    asset_prices : timeseries = asset_selected.get_prices_timeseries()

    if asset_prices.size > 1 and asset_name != "Cash":
        plots += [
            plot_timeseries(
                [
                    adjust_timeseries_by_coverage(
                        asset_selected.get_dividends_ratio_timeseries(),
                        override_name="div_rat_yr",
                    ),
                    asset_prices,
                ],
                [
                    plot_info(
                        plt_type = plot_type.SCATTER, 
                        y = y_axis.LEFT,
                        color = "blue",
                    ),
                    plot_info(
                        plt_type = plot_type.LINE,
                        color = "red",
                    ),
                ],
                asset_name,
                main_folder=main_folder_user,
                show=False,
            )
        ]

plt.close("all")

template_to_html(
    {
        'user_name':    user,
        'date':         get_date_to_string(date_csv, "/"),
        'total_data':   last_data.get_dict_total_stat_report(),
        'data':         last_data.get_dict_stat_report(),
        'month_list':   MONTH_LIST,
        'div_data':     last_data.get_dividends_profile(),
        'div_data_total': last_data.get_dividends_profile(is_total = True),
        'plots':        plots,
    },
    html_path,
)

convert_html_to_pdf(
    html_path, 
    pdf_path
)

print("\nEND")