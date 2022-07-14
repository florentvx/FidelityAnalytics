from library import *
import jinja2

main_folder = r'C:\Users\flore\GoogleDrive\Fidelity'

user= "florent_vassaux"
date_csv = dt.date(2022, 7, 14)

main_folder_user = f"{main_folder}\\{user}"

my_csv_path = get_csv_path(main_folder_user, date_csv, user)
fidelity_data = get_fidelity_data(my_csv_path, print_steps=False)

last_data = fidelity_data.get_last()

print(f"\nLast Data: {last_data.date}\n")

last_data.print_stats_report()

last_data.print_total_stats_report()

plots = []

for asset_name in last_data.get_allocation_asset_list():

    asset_selected = last_data.get_allocation_asset(asset_name)

    if asset_selected.prices.size > 1:
        plots += [
            plot_timeseries(
                [
                    adjust_timeseries_by_coverage(
                        asset_selected.dividends_ratio,
                        override_name="div_rat_yr",
                    ),
                    asset_selected.prices,
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

# write data into html page

jfsl = jinja2.FileSystemLoader(searchpath="./library/template/")
tmp_env = jinja2.Environment(loader=jfsl)
template = tmp_env.get_template("my_template.jinja")
output = template.render(
    {
        'user_name':    user,
        'date':         get_date_to_string(date_csv, "/"),
        'total_data':   last_data.get_dict_total_stat_report(),
        'data':         last_data.get_dict_stat_report(),
        'plots':        plots,
    }
)
with open(get_html_path(main_folder_user, date_csv, user), "w") as text_file:
    text_file.write(output)

print("\nEND")