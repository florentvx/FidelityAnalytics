
from math import log


def format_number(
    input               : float, 
    thousand_separator  : str = ",", 
    decimals_separator  : str = ".",
    prefix              : str = "",
    suffix              : str = "",
    scaling             : float = 1.0,
    decimal_precision   : int = 2,
    do_final_check      : bool = True,
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
        rest_int = int(round((x - x_int) * (10**decimal_precision)))
        if rest_int == 0:
            rest = "0"
        elif rest_int == 10**decimal_precision:
            x_int = int(x) + 1
            x_int_str = str(x_int)
            rest = "0"
        else:
            rest_prefix = "".join(["0" for tmp in range(int(log(rest_int, 10))+1, decimal_precision)])
            rest = rest_prefix + str(rest_int)
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
    
    final_res = f"{minus}{prefix}{thousand_separator.join(res)}{rest}{suffix}"
    if do_final_check:
        err = float(final_res.replace(prefix, "").replace(suffix, "").replace(",", "").replace(" ","")) - input * scaling
        if abs(err) > 10**(-decimal_precision):
            raise ValueError(f"test failed: {final_res} {input * scaling}")
    return final_res


def format_amount(amount: float, decimal_precision = 2) -> str:
    return format_number(amount, prefix="£ ", decimal_precision=decimal_precision)

def format_percentage(percentage: float) -> str:
    return format_number(percentage, suffix=" %", scaling = 100.0)


if __name__ == "__main__":
    test = format_number(0.01997268, suffix=" %", scaling=100.0)
    print(test)
    a = format_number(-2.0712346)
    print(a)
    b = format_number(-2123456.0712346)
    print(b)
    c = format_number(-2.75678)
    print(c)
    d = format_number(-2123456.71134)
    print(d)