from __future__ import annotations
import datetime as dt



from .transaction_type import transaction_type
from .asset import asset
from .allocation import allocation

class history_item:
    
    date:               dt.date
    alloc:              allocation
    tx_type:            transaction_type = None
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
        alloc_item.add_asset(self.tx_type, self.asset)
        
    def __str__(self):
        asset_log = ""
        if not self.asset is None:
            asset_log = f"\ntraded asset : {self.asset}"
        return f"{self.date} - {self.tx_type.name} :{asset_log} \n{self.alloc}"
    
class history:
    data : list[history_item]

    def __init__(self) -> None:
        self.data = [
            history_item(dt.date(2000,1,1), transaction_type.START)
        ]
    
    def add(
        self, 
        date:               dt.date, 
        tx_type:            transaction_type,
        source_investment:  str,
        asset:              asset,
        ) -> None:
        
        prev_item : history_item = self.data[-1]
        new_item = history_item(date, prev_item.alloc)
        new_item.add_asset(tx_type, source_investment, asset)
        print(f"\n{new_item}")
        self.data += [new_item]

        
    

