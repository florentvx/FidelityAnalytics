from __future__ import annotations
import datetime as dt

from .time_series import timeseries

class asset_analytics_month:
    name:           str
    month:          int
    div_data:       timeseries
    div_ratio_data: timeseries
    price_data:     timeseries
    
    def __init__(self, name: str, month: int) -> None:
        self.name = name
        self.month = month
        self.div_data = timeseries(f"{name}_{month}_DIV")
        self.div_ratio_data = timeseries(f"{name}_{month}_DIV_RATIO")
        self.price_data = timeseries(f"{name}_{month}_PRICE")
        
    def add_data(
        self, 
        date: dt.datetime, 
        dividend: float, 
        price: float,
        ) -> None:
        self.div_data.add(date, dividend)
        self.div_ratio_data.add(date, dividend/price)
        self.price_data.add(date, price)

class asset_analytics:
    name:   str
    data:   dict[int, asset_analytics_month]

    def __init__(self, name: str) -> None:
        self.name = name
        self.data = {}

    def add_data(
        self, 
        date: dt.datetime, 
        dividend: float, 
        price: float,
        ) -> None:
        if not date.month in self.data.keys():
            self.data[date.month] =  asset_analytics_month(self.name, date.month)
        self.data[date.month].add_data(date, dividend, price)

    def _get_dim(self) -> dict[int, int]:
        return {
            i: self.data[i].div_ratio_data.size
            for i in self.data.keys()
        }

    def is_at_least_one_year(self) -> bool:
        return max([v for (k,v) in self._get_dim().items()]) > 1
    
    def get_last_yearly_dividend_rate(self) -> float:
        tmp = {
            i: self.data[i].div_ratio_data.get_last_value()
            for i in self.data.keys()
        }

        res = sum([v for (k,v) in tmp.items()])
        if self.is_at_least_one_year():
            return res
        else:
            if len(tmp) <= 4:
                # assumed to be quarterly dividends
                return res / len(tmp) * 4
            else:
                raise ValueError(f"not implemented logic for {tmp}")
        

        
            
        
