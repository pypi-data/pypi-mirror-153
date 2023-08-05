import decimal


def drop_zeros(number):
    if number is None:
        return number

    if not isinstance(number, decimal.Decimal):
        number = decimal.Decimal(number)

    result = number.normalize()
    # e.g 22000 --> Decimal('2.2E+4')
    return result.__trunc__() if not result % 1 else float(result)
