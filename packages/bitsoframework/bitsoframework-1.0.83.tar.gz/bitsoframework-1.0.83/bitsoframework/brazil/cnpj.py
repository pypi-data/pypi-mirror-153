import re


def validate(cnpj):
    """
    Method to validate brazilian cnpjs
    Tests:

    >>> validate('61882613000194')
    True
    >>> validate('61882613000195')
    False
    >>> validate('53.612.734/0001-98')
    True
    >>> validate('69.435.154/0001-02')
    True
    >>> validate('69.435.154/0001-01')
    False
    """
    # defining some variables
    lista_validacao_um = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    lista_validacao_dois = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    # cleaning the cnpj
    cnpj = clean(cnpj)

    # finding out the digits
    verificadores = cnpj[-2:]

    # verifying the lenght of the cnpj
    if len(cnpj) != 14:
        return False

    # calculating the first digit
    soma = 0
    id = 0
    for numero in cnpj:

        # to do not raise indexerrors
        try:
            lista_validacao_um[id]
        except:
            break

        soma += int(numero) * int(lista_validacao_um[id])
        id += 1

    soma = soma % 11
    if soma < 2:
        digito_um = 0
    else:
        digito_um = 11 - soma

    digito_um = str(digito_um)  # converting to string, for later comparison

    # calculating the second digit
    # suming the two lists
    soma = 0
    id = 0

    # suming the two lists
    for numero in cnpj:

        # to do not raise indexerrors
        try:
            lista_validacao_dois[id]
        except:
            break

        soma += int(numero) * int(lista_validacao_dois[id])
        id += 1

    # defining the digit
    soma = soma % 11
    if soma < 2:
        digito_dois = 0
    else:
        digito_dois = 11 - soma

    digito_dois = str(digito_dois)

    # returnig
    return bool(verificadores == digito_um + digito_dois)


def clean(cnpj):
    """
    Method to remove all non numeric values from the given cnpj.
    Tests:

    >>> print clean('53.612.734/0001-98')
    53612734000198
    """
    if cnpj:
        return re.sub('[^0-9]', '', cnpj)
    return cnpj


def format(cnpj):
    """
    Method to format cnpj numbers.
    Tests:

    >>> print format('53612734000198')
    53.612.734/0001-98
    """
    return "%s.%s.%s/%s-%s" % (cnpj[0:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:14])
