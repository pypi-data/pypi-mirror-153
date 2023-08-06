from numi.utils import base

def _get_from_base(n, f):
    """
    Returns all possible variations for the written numbers in the base as a list of strings
    for numbers between 1-19 as well as all numbers that are divisable by 10,100,1000 etc.
    """
    # try:
    num = base[n, f]
    if "/" in num:
        return num.split("/")
    else:
        return [num]
    # except Exception as e:
    # DEM I don't like that Python buries part of the excepetion when I use Try/except.  
    #     if n not in set([x[0] for x in base.keys()]):
    #         print(f'Invalid input for n: {n}')
    #     if (n,f) not in base.keys():
    #         print(f'Invalid input for the combination of n and f: ({n}, {f})')

def _nums_20_99(n, f):
    """
    Returns all possible variations for the written numbers from 20 to 99 as a list of strings.
    """
    n1 = int(str(n)[0] + "0")
    n2 = int(str(n)[1])
    last_number = _get_from_base(n2, f)
    if len(last_number) == 2:
        return [f"{base[n1,'at_af']} og {n2}" for n2 in last_number]
    else:
        return [f"{base[n1,'at_af']} og {base[n2,f]}"]

def _nums_100_999(n, f):
    """
    Returns all possible variations for the written numbers from 100 to 999 as a list of strings.
    """

    def _hundreds(n):
        n_1 = int(str(n)[0])
        if n_1 == 1:
            num = f"{base[n_1, 'et_hk_nf']} hundrað"
        elif n_1 in [2, 3, 4]:
            num = f"{base[n_1,'ft_hk_nf']} hundruð"
        else:
            num = f"{base[n_1,'at_af']} hundruð"
        
        return num

    n1 = int(str(n)[0] + "00")
    num1 = _hundreds(n1)
    n2 = n - n1
    num2 = []

    if n in [100, 200, 300, 400, 500, 600, 700, 800, 900]:
        num = [_hundreds(n)]

    elif n2 in [x for x in range(1, 20)] or n2 in [x for x in range(20, 101, 10)]:
        for line in _get_from_base(n2, f):
            num2.append(f"og {line}")
        num2 = num2
    else:
        num2 = _nums_20_99(n2, f)
    
    if num2:
        num = [f"{num1} {n2}" for n2 in num2]
    
    for line in num:
        if "eitt hundrað" in line:
            num.append(line.replace("eitt hundrað", "hundrað"))

    return num

def spell_out(n, f):
    """
    Handles user input and returns a list of string with all possible variations of 
    if input number
    """
    if (
        n in [x for x in range(1, 20)]
        or n in [x for x in range(20, 91, 10)]
        or n in [1000, 1000000]
    ):
        return _get_from_base(n, f)
    elif n in [x for x in range(20, 100)]:
        return _nums_20_99(n, f)
    elif n in [x for x in range(100, 1000)]:
        return _nums_100_999(n, f)


