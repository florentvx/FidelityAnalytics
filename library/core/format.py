
def format_number(
    input               : float, 
    thousand_separator  : str = ",", 
    decimals_separator  : str = ".",
    prefix              : str = "",
    suffix              : str = "",
    scaling             : float = 1.0,
    decimal_precision   : int = 2,
    ) -> str:

    if thousand_separator == decimals_separator:
        raise ValueError("cannot use same separator for thousand and decimals")
    
    minus = ""
    
    x = input * scaling
    if x < 0:
        minus = "- "
        x *= -1.0
    x_int = int(x)
    x_int_str = str(x_int)
    rest = ""
    if decimal_precision > 0:
        rest = str(int(round((x - x_int) * (10**decimal_precision))))
    rest_cutting = True
    while rest_cutting:
        if len(rest) == 0:
            rest_cutting = False
        else:
            if rest[-1] == "0":
                rest  = rest[:(len(rest) - 1)]
            else:
                rest_cutting = False

    a = len(x_int_str)
    n0 = a % 3
    res = []
    if n0 > 0:
        res += [x_int_str[:n0]]
    res += [
        x_int_str[(n0+i*3):(n0+i*3+3)]
        for i in range(int((a - n0)/3))
    ]

    if len(rest) > 0:
        rest = decimals_separator + rest
    return f"{minus}{prefix}{thousand_separator.join(res)}{rest}{suffix}"


def format_amount(amount: float, decimal_precision = 2) -> str:
    return format_number(amount, prefix="£ ", decimal_precision=decimal_precision)

def format_percentage(percentage: float) -> str:
    return format_number(percentage, suffix=" %", scaling = 100.0)