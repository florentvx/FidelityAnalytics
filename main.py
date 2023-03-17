from library import *


''' Inputs '''

main_folder = r'C:\Users\flore\GoogleDrive\Fidelity'
user= "florent_vassaux"
date_csv = dt.date(2023, 3, 17)
output_suffix = ''
print_info = False

''' Code '''

main_folder_user = f"{main_folder}\\{user}"
csv_path = get_csv_path(main_folder_user, date_csv, user)
html_path = get_html_path(main_folder_user, date_csv, user, suffix=output_suffix)
pdf_path = get_pdf_path(main_folder_user, date_csv, user, suffix=output_suffix)


fidelity_data : history = get_fidelity_data(csv_path, print_steps=False)
last_data : history_item = fidelity_data.get_last()

if print_info:
    print(f"\nLast Data: {last_data.date}\n")
    last_data.print_stats_report()
    last_data.print_total_stats_report()

template_to_html(
    {
        'user_name':    user,
        'date':         get_date_to_string(date_csv, "/"),
        'total_data':   last_data.get_dict_total_stat_report(),
        'data':         last_data.get_dict_stat_report(),
        'month_list':   MONTH_LIST,
        'div_data':     last_data.get_dividends_profile(),
        'div_data_total': last_data.get_dividends_profile(is_total = True),
        'plots':        get_plots_from_history_item(last_data, main_folder_user),
    },
    html_path,
)

convert_html_to_pdf(
    html_path, 
    pdf_path
)

print("\nEND")