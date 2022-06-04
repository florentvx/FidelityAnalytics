from __future__ import annotations

from .transaction_type import transaction_type
from .asset import asset

class allocation_item:
    
    core:                   asset
    dividends_rate_hist:    list
    dividends:              float
    
    def __init__(
        self, 
        name: str,
        ):

        self.core = asset(name, 0, 0, 0)
        self._dividends_rate_hist = []
        self.dividends = 0.0

    @property
    def average_dividend_rate(self) -> float:
        if len(self._dividends_rate_hist) == 0:
            return 0.0
        return sum(self._dividends_rate_hist)/len(self._dividends_rate_hist)

    def add_asset(
        self,
        tx_type:    transaction_type,
        asset:      asset,
        ) -> None:

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
            self.dividends += asset.amount
            self._dividends_rate_hist += [asset.amount / self.core.amount * 4] ## supposition 1 dividend per quarter
        elif tx_type in [transaction_type.CASH_IN_RING_FENCED_FOR_FEES, transaction_type.TRANSFER_TO_CASH_MANAGEMENT_ACCOUNT_FOR_FEES]:
            # fees are already registered as "service fee"
            pass
        else:
            raise ValueError(f"Unknown transaction type: {tx_type}")
        return

    def copy(self):
        res = allocation_item(self.core.name)
        res.core = self.core.copy()
        res._dividends_rate_hist = self._dividends_rate_hist.copy()
        res.dividends = self.dividends
        return res

    def __str__(self):
        if self.dividends == 0:
            return f"{self.core}"
        else:
            return f"{self.core} - Dividends: {self.dividends}"# - {self.average_dividend_rate}"


class allocation:

    _data: dict[str, allocation_item]

    def __init__(self):
        self._data = {}

    def keys(self) -> list[str]:
        return self._data.keys()

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
