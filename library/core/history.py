from __future__ import annotations
import datetime as dt

from numpy import average

from library.core.format import format_amount, format_percentage

from .transaction_type import transaction_type
from .asset import asset
from .allocation import allocation, allocation_item

MONTH_LIST = [dt.datetime(2000, i+1, 1).strftime("%B") for i in range(12)]

class history_item:
    
    # main attributes
    date:               dt.date
    alloc:              allocation

    # keeping record of the last transaction
    tx_type:            transaction_type
    source_investment:  str
    asset:              asset

    def __init__(
        self, 
        date:   dt.date, 
        alloc:  allocation = None,
        ) -> None:

        self.date = date
        self.alloc = allocation()
        if not alloc is None:
            self.alloc = alloc.copy()
        self.tx_type = transaction_type.START
        self.source_investment = None
        self.asset = None

    def allocation_keys(self):
        return self.alloc.keys()

    def get_allocation_asset(self, name: str) -> allocation_item:
        return self.alloc.get(name, trigger_error=True)

    def add_asset(
        self,
        tx_type:            transaction_type,
        source_investment:  str,
        asset:              asset,
        ) -> None:

        self.tx_type = tx_type
        self.source_investment = source_investment
        self.asset = asset.copy()
        alloc_item = self.alloc.get(self.asset.name)
        if not self.source_investment is None:
            alloc_item = self.alloc.get(self.source_investment, trigger_error = True)
            # adding the cash amount into the 'Cash' asset
            self.alloc.get("Cash", trigger_error=True).add_asset(self.date, self.tx_type, self.asset)
        alloc_item.add_asset(self.date, self.tx_type, self.asset)
        
    def __str__(self):
        asset_log = ""
        if not self.asset is None:
            asset_log = f"\ntraded asset : {self.asset}"
        return f"{self.date} - {self.tx_type.name} :{asset_log} \n{self.alloc}"

    # region statistics

    def get_total_value(self, name: str = None, include_cash : bool = True) -> float:
        items = self.allocation_keys()
        if not name is None:
            items = [name]

        return sum([
            self.get_allocation_asset(n).core.amount
            for n in items
            if not n == "Cash" or include_cash
        ])
        
    def get_dividends_total(self, name: str = None) -> float:
        items = self.allocation_keys()
        if not name is None:
            items = [name]

        return sum([
            self.get_allocation_asset(n).get_dividends_total()
            for n in items
            if not n == "Cash"
        ])

    def get_dividends_expectation(self, name: str = None) -> float:
        items = self.allocation_keys()
        if not name is None:
            items = [name]
        
        return sum([
            self.get_allocation_asset(n).get_dividends_average_rate() * self.get_allocation_asset(n).core.amount
            for n in items
            if n != "Cash"
        ])

    def get_dividends_average_rate(self, name: str = None) -> float:
        items = self.allocation_keys()
        if not name is None:
            items = [name]
        
        return average([
            self.get_dividends_expectation(n) / self.get_total_value(n, include_cash=False)
            for n in items
            if n != "Cash"
        ])
    
    def print_stats_report(self, name : str = None) -> None:
        items = self.allocation_keys()
        if not name is None:
            items = [name]
        
        print(" ")
        print(f"STATS REPORT {self.date}")
        for n in items:
            print(" - ")
            self.get_allocation_asset(n).print_stats_report()
        print(" ")

        return 

    def get_dict_total_stat_report(self) -> None:
        total_value = self.get_total_value()
        total_asset = self.get_total_value(include_cash=False)
        return {
            "total_value"           : format_amount(total_value),
            "total_cash"            : format_amount(total_value - total_asset),
            "total_assets"          : format_amount(total_asset),
            "dividends_sum"         : format_amount(self.get_dividends_total()),
            "dividends_ratio"       : format_percentage(self.get_dividends_average_rate()),
            "dividends_expectation" : format_amount(self.get_dividends_expectation()),
        }

    def get_dict_stat_report(self):
        return {
            key: self.get_allocation_asset(key).get_dict_stat_report()
            for key in self.allocation_keys()
        }

    def print_total_stats_report(self) -> None:
        tot_stat_report = self.get_dict_total_stat_report()
        print("\ntotal")
        print(f"total value      : {tot_stat_report['total_value']}")
        print(f"total (w/o cash) : {tot_stat_report['total_assets']}")
        print(f"sum div.         : {tot_stat_report['dividends_sum']}")
        print(f"div. ratio       : {tot_stat_report['dividends_ratio']}")
        print(f"div. exp.        : {tot_stat_report['dividends_expectation']}")
        return

    #endregion

    def get_dividends_profile(self, is_total: bool = False, cleaning: bool = True):
        raw_dict = {
            asset: self.get_allocation_asset(asset).get_dividends_profile() 
            for asset in self.allocation_keys()
        }
        if not (cleaning or is_total):
           return raw_dict
        if is_total:
            return {
                i: format_amount(
                    sum([
                        v.get(i+1,0) 
                        for v in raw_dict.values()
                    ])
                )
                for i in range(12)
            }
        def _clean(d : dict):
            return {
                i: format_amount(d.get(i+1,0)) 
                for i in range(12)
            }
        return {
            k: _clean(v) 
            for (k,v) in raw_dict.items()
            if len(v) > 0
        }
        
    
class history:
    _data : list[history_item]

    def __init__(self) -> None:
        self._data = [
            history_item(dt.date(2000,1,1))
        ]
    
    def get(self, date: dt.date) -> history_item:
        return self._data[self._get_closest_date(date)]

    def get_last(self) -> history_item:
        return self._data[-1]

    def get_dates(self):
        return [x.date for x in self._data]

    def _get_closest_date(self, date: dt.date) -> int:
        dates = self.get_dates()
        if date < dates[0]:
            raise ValueError(f"Your date {date} is too old : min. {dates[0]}")
        
        if date > dates[-1]:
            return len(dates) - 1
        i_res = 0
        while date > dates[i_res]:
            i_res += 1
        return i_res - 1

    def add(
        self, 
        date:               dt.date, 
        tx_type:            transaction_type,
        source_investment:  str,
        asset:              asset,
        print_step:         bool = False,
        ) -> None:
        
        if date < self.get_last().date:
            raise "adding past event"

        prev_item : history_item = self._data[-1]
        new_item = history_item(date, prev_item.alloc)
        new_item.add_asset(tx_type, source_investment, asset)
        if print_step:
            print(f"\n{new_item}")
        self._data += [new_item]

    



        
    

