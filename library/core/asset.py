from __future__ import annotations

class asset:
    
    name:               str
    quantity:           float
    market_price:       float
    price_per_unit:     float
    fees:               float

    def __init__(
        self, 
        name:               str, 
        amount:             float, 
        quantity:           float, 
        price_per_unit:     float, 
        fees:               float= 0.0
        ):

        self.name = name
        self.price_per_unit = price_per_unit
        if price_per_unit == 0:
            self.price_per_unit = 1.0
        self.market_price = self.price_per_unit
        if quantity == 0:
            self.quantity = amount
        else:
            self.quantity = quantity
        self.fees = fees
        if name == "Cash" and abs(amount + quantity * self.price_per_unit) < 0.01:
            self.quantity *= -1
    
    @property
    def amount(self):
        return self.quantity * self.market_price

    def _update_market_price(self, new_price: float):
        self.market_price = new_price

    def add_quantity(
        self, 
        asset: asset
        ) -> None:
        if asset.quantity <= 0:
            raise ValueError(f"quantity must be positive: {asset.quantity}")
        self.quantity += asset.quantity
        self._update_market_price(asset.market_price)

    def substract_quantity(
        self,
        asset: asset
        ) -> None:
        if asset.quantity >= 0:
            raise ValueError(f"quantity must be positive: {asset.quantity}")
        self.quantity += asset.quantity
        self._update_market_price(asset.market_price)

    def add_fee(
        self,
        asset : asset
        ) -> None:
        
        if asset.quantity > 0:
            raise ValueError(f"fee must be negative: {asset.quantity}")
        self.quantity += asset.quantity
        self.fees -= asset.amount
        self._update_market_price(asset.market_price)

    def add_buy_transaction(
        self,
        asset: asset,
        ) -> None:
        self.price_per_unit = (self.amount + asset.amount) / (self.quantity + asset.quantity)
        self.quantity += asset.quantity
        self.fees += asset.fees
        self._update_market_price(asset.market_price)

    def copy(self) -> asset:
        return asset(
            self.name,
            self.amount,
            self.quantity,
            self.price_per_unit,
            self.fees
        )

    def __str__(self):
        res = f"{self.name}: Amount: {round(self.amount, 2)} " \
            + f"# Quantity: {round(self.quantity, 2)} " \
            + f"# Market Price: {round(self.market_price, 2)} " \
            + f"# Unit Price: {round(self.price_per_unit, 2)} "
        if self.fees != 0:
            res += f"# Fees: {round(self.fees, 2)}"
        return res
    