from enum import Enum

class plot_type(Enum):
    LINE = 0
    SCATTER = 1

class y_axis(Enum):
    RIGHT = 0
    LEFT = 1

class plot_info:

    type : plot_type
    y : y_axis
    color: str

    def __init__(
        self, 
        plt_type: plot_type = plot_type.LINE,
        y: y_axis = y_axis.RIGHT,
        color : str = "black",
        ) -> None:
        self.type = plt_type
        self.y = y
        self.color = color


