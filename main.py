from library import *
import jinja2

user= "florent_vassaux"
date_csv = dt.date(2022, 6, 3)

my_path = get_csv_path(user, date_csv)
fidelity_data = get_fidelity_data(my_path, print_steps = False)

last_data = fidelity_data.get_last()

print(f"\nLast Data: {last_data.date}\n")

last_data.print_stats_report()

last_data.print_total_stats_report()

for asset_name in last_data.get_allocation_asset_list():

    asset_selected = last_data.get_allocation_asset(asset_name)

    if asset_selected.prices.size > 1:
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
        )

plt.close("all")

# write data into html page

jfsl = jinja2.FileSystemLoader(searchpath="./library/template/")
tmp_env = jinja2.Environment(loader=jfsl)
template = tmp_env.get_template("my_template.jinja")
output = template.render(
    {
        'user_name': user,
        'date': get_date_to_string(date_csv, "/"),
        'data': last_data.get_dict_stat_report()
    }
)
with open("./output.html", "w") as text_file:
    text_file.write(output)

print("\nEND")