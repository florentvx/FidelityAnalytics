from __future__ import annotations
from matplotlib import pyplot as plt

from ..core import timeseries
from .plot_info import *

def plot_timeseries(
    my_ts_list: list[timeseries], 
    my_plt_info : list[plot_info],
    title: str = None,
    main_folder: str = None,
    show: bool = True,
    ) -> str:

    """
    returns the output path
    """

    if len(my_ts_list) != len(my_plt_info):
        raise ValueError(f"list does not match size {len(my_ts_list)} {len(my_plt_info)}")

    
    fig, ax1 = plt.subplots(figsize=(15, 5))
    ax1.set_title(title)
    ax2 = ax1.twinx()

    for i in range(len(my_ts_list)):
        my_ts = my_ts_list[i]
        my_info = my_plt_info[i]
        
        axis = None
        if my_info.y == y_axis.LEFT:
            axis = ax1
        elif my_info.y == y_axis.RIGHT:
            axis = ax2
        else:
            raise ValueError(f"axis error: {my_info.y}")

        if my_info.type == plot_type.SCATTER:
            axis.scatter(my_ts.keys(), my_ts.values(), c=my_info.color)
        elif my_info.type == plot_type.LINE:
            axis.plot(my_ts.keys(), my_ts.values(), c=my_info.color)
        else:
            raise ValueError(f"unknown plot type: {my_info.type}")

    path = None
    if not main_folder is None:
        if main_folder == "":
            path = f"images\\{title}.png"
        else:
            path = f"{main_folder}\\images\\{title}.png"
        fig.savefig(path)
    
    if show:
        plt.show()
    
    return path
