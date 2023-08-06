"""
Python ID validator and check digit generator package based on Luhn's formula.
Luhn's Formula was designed to protect against accidental input errors.
"""

# Precomputed even value to improve performance and energy impact
# sum(divmod(2 *  0 , 10)) :  0
# sum(divmod(2 *  1 , 10)) :  2
# sum(divmod(2 *  2 , 10)) :  4
# sum(divmod(2 *  3 , 10)) :  6
# sum(divmod(2 *  4 , 10)) :  8
# sum(divmod(2 *  5 , 10)) :  1
# sum(divmod(2 *  6 , 10)) :  3
# sum(divmod(2 *  7 , 10)) :  5
# sum(divmod(2 *  8 , 10)) :  7
# sum(divmod(2 *  9 , 10)) :  9
__PrecomputedEvenValue = [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]


def checksum(number: str) -> int:
    """Checksum vith the luhn formula
    Args:
        number : Numbeer to calculate
    return:
        Result of luhn formula
    """
    digits = list(map(int, number))
    odd_sum = sum(digits[-1::-2])
    even_sum = sum([__PrecomputedEvenValue[d] for d in digits[-2::-2]])
    return (odd_sum + even_sum) % 10


def isvalid(number: str) -> bool:
    """Validate number with the Luhn formula.
    Args:
        number: Number to validate.
    Return:
        ``True`` when the number is valid, otherwise ``False``.
    """
    if not (number.isdecimal() and len(number) > 1):
        return False
    return (checksum(number) == 0)


def getcheckdigit(number: str) -> str:
    """Generate check digit with the Luhn formula for a number.
    Args:
        number: Number used to generate the check digit.
    Return:
        the check digit for a number.
    Raise error:
        ValueError : Invalid number.
    """
    if not number.isdecimal():
        raise ValueError("Invalid number")
    return str((10 - checksum(number + '0')) % 10)


def addcheckdigit(number: str) -> str:
    """Generate and add check digit with the luhn formula for a number
    Args:
        number: Number used to generate the check digit.
    Return:
        the number with the check digit.
    Raise error:
        ValueError : Invalid number.
    """
    return "".join((number, getcheckdigit(number)))
