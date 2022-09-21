from __future__ import annotations
from ..core import history_item, allocation_item, adjust_timeseries_by_coverage
from .plot import *

def get_plots_from_history_item(
    last_data: history_item, 
    main_folder_user: str,
    ) -> list[str]:

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
    return plots