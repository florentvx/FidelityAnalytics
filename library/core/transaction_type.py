from enum import Enum

class transaction_type(Enum):
    START                                           = 0     # initial state
    BUY                                             = 1     # asset you aquire        
    BUY_FROM_REGULAR_SAVINGS_PLAN                   = 2     # same as buy (but from RSP)
    CASH_OUT_FOR_BUY                                = 3     # money paid to aquire asset
    DEALING_FEE                                     = 4     # fee paid for purchase
    CASH_IN_REGULAR_SAVINGS_PLAN                    = 5     # cash deposit from RSP
    SERVICE_FEE                                     = 6     # generic fee
    CASH_DIVIDEND                                   = 7     # dividend
    TRANSFER_TO_CASH_MANAGEMENT_ACCOUNT_FOR_FEES    = 8     # transfer to pay "cash in ring-fenced for fees"
    CASH_IN_RING_FENCED_FOR_FEES                    = 9     # payment in special accout to pay for service fees
    CASH_IN_LUMP_SUM                                = 10    # simple cash deposit
    SELL                                            = 11    # sell a given asset
    CASH_IN_FROM_SELL                               = 12    # cash received from sale
    WITHDRAWAL                                      = 13    # withdraw money from fidelity
    AUTO_SELL_FOR_FEES                              = 14    # sold share to pay some fees
    CASH_IN_FEES_FROM_AUTO_SELL                     = 15    # cash received from the auto-sell (14)
    CASH_INTEREST                                   = 19    # cash interest from cash account


def get_transation_type(x : str):
    for tt in transaction_type:
        if x.upper().replace(" ", "_").replace("-", "_") == tt.name:
            return tt
    raise ValueError(f"No matching tx type {x}")