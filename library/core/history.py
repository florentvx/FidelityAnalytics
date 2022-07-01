from __future__ import annotations
import datetime as dt

from .transaction_type import transaction_type
from .asset import asset
from .allocation import allocation, allocation_item

class history_item:
    
    # main attributes
    date:               dt.date
    alloc:              allocation

    # keeping record of the last transaction
    tx_type:            transaction_type = transaction_type.START
    source_investment:  str = None
    asset:              asset = None

    def __init__(
        self, 
        date:   dt.date, 
        alloc:  allocation = None,
        ) -> None:

        self.date = date
        self.alloc = allocation()
        if not alloc is None:
            self.alloc = alloc.copy()

    def get_allocation_asset_list(self) -> list[str]:
        return list(self.alloc.keys())

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
        items = self.get_allocation_asset_list()
        if not name is None:
            items = [name]

        return sum([
            self.get_allocation_asset(n).core.amount
            for n in items
            if not n == "Cash" or include_cash
        ])
        
    def get_dividends_total(self, name: str = None) -> float:
        items = self.get_allocation_asset_list()
        if not name is None:
            items = [name]

        return sum([
            self.get_allocation_asset(n).get_dividends_total()
            for n in items
            if not n == "Cash"
        ])

    def get_dividends_expectation(self, name: str = None) -> float:
        items = self.get_allocation_asset_list()
        if not name is None:
            items = [name]
        
        return sum([
            self.get_allocation_asset(n).get_dividends_average_rate() * self.get_allocation_asset(n).core.amount
            for n in items
            if n != "Cash"
        ])

    def get_dividends_average_rate(self, name: str = None) -> float:
        items = self.get_allocation_asset_list()
        if not name is None:
            items = [name]
        
        return self.get_dividends_expectation(name) / self.get_total_value(name, include_cash=False)
    
    def print_stats_report(self, name : str = None) -> None:
        items = self.get_allocation_asset_list()
        if not name is None:
            items = [name]
        
        print(" ")
        print(f"STATS REPORT {self.date}")
        for n in items:
            print(" - ")
            self.get_allocation_asset(n).print_stats_report()
        print(" ")

        return 

    def print_total_stats_report(self) -> None:
        print("\nTOTAL")
        print(f"total value      : £ {round(self.get_total_value(), 2)}")
        print(f"total (w/o cash) : £ {round(self.get_total_value(include_cash=False), 2)}")
        print(f"sum div.         : £ {round(self.get_dividends_total(), 2)}")
        print(f"div. ratio       : {round(self.get_dividends_average_rate() * 100, 2)} %")
        print(f"div. exp.        : £ {round(self.get_dividends_expectation(), 2)}")

        return

    #endregion

    
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

    



        
    

