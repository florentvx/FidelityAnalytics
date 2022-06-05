from __future__ import annotations

import datetime as dt

from .transaction_type import transaction_type
from .asset import asset
from .timeseries import timeseries

class allocation_item:
    
    core:               asset
    dividends:          timeseries
    dividends_ratio:    timeseries
    prices:             timeseries
    
    def __init__(
        self, 
        name: str,
        ):

        self.core = asset(name, 0, 0, 0)
        self.dividends = timeseries(f"{name}_DIV")
        self.dividends_ratio = timeseries(f"{name}_DIV_RAT")
        self.prices = timeseries(f"{name}_PRICES")

    def average_dividend_rate(self) -> float:
        raise ValueError("not implemented")

    def add_asset(
        self,
        date:       dt.date,
        tx_type:    transaction_type,
        asset:      asset,
        ) -> None:

        if asset.name != "Cash":
            self.prices.add(date, asset.price_per_unit)
        if tx_type in [transaction_type.CASH_IN_LUMP_SUM, transaction_type.CASH_IN_REGULAR_SAVINGS_PLAN]:
            self.core.add_quantity(asset)
        elif tx_type in [transaction_type.DEALING_FEE, transaction_type.SERVICE_FEE]:
            self.core.add_fee(asset)
        elif tx_type in [transaction_type.BUY, transaction_type.BUY_FROM_REGULAR_SAVINGS_PLAN]:
            self.core.add_buy_transaction(asset)
        elif tx_type == transaction_type.CASH_OUT_FOR_BUY:
            self.core.substract_quantity(asset)
        elif tx_type == transaction_type.CASH_DIVIDEND:
            if self.core.name == "Cash":
                raise ValueError("Dividends on cash ???")
            if asset.amount < 0:
                raise ValueError("Negative dividends???")
            self.dividends.add(date, asset.amount)
            self.dividends_ratio.add(date, asset.amount / self.core.amount)
        elif tx_type in [transaction_type.CASH_IN_RING_FENCED_FOR_FEES, transaction_type.TRANSFER_TO_CASH_MANAGEMENT_ACCOUNT_FOR_FEES]:
            # fees are already registered as "service fee"
            pass
        else:
            raise ValueError(f"Unknown transaction type: {tx_type}")
        return

    def copy(self):
        res = allocation_item(self.core.name)
        res.core = self.core.copy()
        res.dividends = self.dividends.copy()
        res.dividends_ratio = self.dividends_ratio.copy()
        res.prices = self.prices.copy()
        return res

    def __str__(self):
        if self.dividends.size() == 0:
            return f"{self.core}"
        else:
            return f"{self.core} - Dividends: {round(self.dividends.sum(), 2)}"# - {self.average_dividend_rate}"


class allocation:

    _data: dict[str, allocation_item]

    def __init__(self):
        self._data = {}

    def keys(self) -> list[str]:
        return list(self._data.keys())

    def get(
        self, 
        name:           str,
        trigger_error:  bool = False,
        ) -> allocation_item:

        if not name in self._data:
            if trigger_error:
                raise ValueError(f"name not found: {name}")
            self._data[name] = allocation_item(name)
        return self._data[name]

    def copy(self) -> allocation:
        res = allocation()
        res._data = {
            k: v.copy() 
            for (k, v) in self._data.items()
        }
        return res

    def __str__(self):
        res = [
            f" -> {item}" 
            for _, item in self._data.items()
        ]
        return "\n".join(res)
