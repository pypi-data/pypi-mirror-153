import math


def suffix_number(number: float) -> str:
    if number < 0:
        raise ValueError("Cannot suffix a negative number.")
    if number == 0:
        string_number = str(number)
    elif math.log10(number) >= 9:
        string_number = str(number / 1000000000) + "B"
    elif math.log10(number) >= 6:
        string_number = str(number / 1000000) + "M"
    elif math.log10(number) >= 3:
        string_number = str(number / 1000) + "k"
    else:
        string_number = str(number)
    return string_number
