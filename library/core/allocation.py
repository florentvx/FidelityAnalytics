from __future__ import annotations

import datetime as dt

from .transaction_type import transaction_type
from .asset import asset
from .time_series import timeseries
from .format import *

class allocation_item:
    
    core:               asset
    dividends:          timeseries
    dividends_ratio:    timeseries
    prices:             timeseries
    
    def __init__(
        self, 
        name: str,
        ):

        self.core = asset(name, 0, 0, 0, 0)
        self.dividends = timeseries(f"{name}_DIV")
        self.dividends_ratio = timeseries(f"{name}_DIV_RAT")
        self.prices = timeseries(f"{name}_PRICES")

    def add_asset(
        self,
        date:       dt.date,
        tx_type:    transaction_type,
        asset:      asset,
        ) -> None:

        # update price timeseries (to move else where?)
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
            if asset.amount < 0:
                raise ValueError("Negative dividends???")
            if self.core.name == "Cash":
                self.core.add_quantity(asset)
            else:
                self.dividends.add(date, asset.amount)
                self.dividends_ratio.add(date, asset.amount / self.core.amount)
                #self.core.add_quantity(asset)
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
        if self.dividends.size == 0:
            return f"{self.core}"
        else:
            return f"{self.core} - Dividends: {round(self.dividends.sum(), 2)}"# - {self.average_dividend_rate}"

    # region statistics
    
    def get_dividends_total(self) -> float:
        return self.dividends.sum()

    def get_dividends_average_rate(self) -> float:
        return self.dividends_ratio.average() * 4
    
    def get_dividends_expectation(self) -> float:
        # the div average ratio is assumed to be quarterly
        return self.get_dividends_average_rate() * self.core.amount
    
    def get_dict_stat_report(self):
        dp = 0
        if self.core.name == "Cash":
            dp = 2
        return {
            "name":                     self.core.name,
            "market_price":             format_amount(self.core.market_price, decimal_precision=4),
            "quantity":                 format_number(self.core.quantity, decimal_precision=dp),
            "amount":                   format_amount(self.core.amount),
            "purchased_price":          format_amount(self.core.price_per_unit, decimal_precision=4),
            "return":                   format_percentage((self.core.market_price / self.core.price_per_unit - 1)),
            "pnl":                      format_amount(self.core.quantity * (self.core.market_price - self.core.price_per_unit)),
            "dividends_sum":            format_amount(self.get_dividends_total()),
            "dividends_ratio":          format_percentage(self.get_dividends_average_rate()),
            "dividends_expectation":    format_amount(self.get_dividends_expectation()),
        }

    def print_stats_report(self) -> None:
        stat_report = self.get_dict_stat_report()
        print(f"asset: {stat_report['name']}")
        print(
            f"last price / quantity / amount: " +\
            f"{stat_report['market_price']} / {stat_report['quantity']} / {stat_report['amount']}"
        )
        print(
            f"purchased price: {stat_report['purchased_price']} " + \
            f"({stat_report['return']}) " + \
            f" -> PnL: {stat_report['pnl']}"
        )

        print(f"sum dividends: {stat_report['dividends_sum']}")
        print(f"dividends ratio: {stat_report['dividends_ratio']}")
        print(f"dividends expected: {stat_report['dividends_expectation']}")

        return

    

    #endregion


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
