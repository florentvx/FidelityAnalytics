from __future__ import annotations
import datetime as dt
from numpy import average
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
        amount: float,
        ) -> None:
        self.div_data.add(date, dividend)
        self.div_ratio_data.add(date, dividend/amount)
        self.price_data.add(date, price)

    def copy(self) -> asset_analytics_month:
        res = asset_analytics_month(self.name, self.month)
        res.div_data = self.div_data.copy()
        res.div_ratio_data = self.div_ratio_data.copy()
        res.price_data = self.price_data.copy()
        return res

class asset_analytics:
    name:           str
    data:           dict[int, asset_analytics_month]
    price_data:     timeseries

    def __init__(self, name: str) -> None:
        self.name = name
        self.data = {}
        self.price_data = timeseries(f"{name}_PRICE")

    def get_dividends_ratio_timeseries(self) -> timeseries:
        res = timeseries(f"{self.name}_DIV_RATIO")
        for i_month in self.data.keys():
            res.copy_paste(self.data[i_month].div_ratio_data)
        return res


    def add_price(
        self, 
        date: dt.datetime, 
        price: float,
        ) -> None:
        self.price_data.add(date, price)
    
    def add_dividend(
        self, 
        date: dt.datetime, 
        dividend: float, 
        amount: float,
        ) -> None:
        price = self.price_data.get_closest(date)
        # validation
        if price is None:
            raise ValueError("Contribute price before div")
        if not date.month in self.data.keys():
            self.data[date.month] =  asset_analytics_month(self.name, date.month)
        self.data[date.month].add_data(date, dividend, price, amount)

    def _get_dim(self) -> dict[int, int]:
        return {
            i: self.data[i].div_ratio_data.size
            for i in self.data.keys()
        }

    def copy(self) -> asset_analytics:
        res = asset_analytics(self.name + "")
        res.price_data = self.price_data.copy()
        res.data = { (k+0):v.copy() for (k,v) in self.data.items() }    
        return res

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
    
    def get_dividends_total(self):
        return sum([
            self.data[i].div_data.sum()
            for i in self.data.keys()
        ])

    def get_dividends_yearly_average_rate(self):
        list_div = {
            i: self.data[i].div_ratio_data.values()
            for i in self.data.keys()
        }
        if len(list_div) == 0:
            return 0.0
        list_div_max_size = max([
            len(list_div[i])
            for i in list_div.keys()
        ])
        if list_div_max_size >= 2:
            return sum([average(list_div[i]) for i in list_div.keys()])
        else:
            # the guess is that dividends are quarterly
            return average([v for v in list_div.values()])*4.0


        

        
            
        
