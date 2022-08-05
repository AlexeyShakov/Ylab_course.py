import itertools as it
import math

def calculating_number(bases, values):

    number = 1
    for base in range(len(bases)):
        number *= bases[base]**int(values[base])
    return number

def count_find_num(primesL, limit):

    # we will put the max extent of a prime factor. The prime factor with the max extent must be less than limit
    base_dict = {}
    for base in primesL:
        base_dict[base] = math.floor(math.log(limit, base))

    """we put all possible extents for prime factors into a string
    for example: "3" appears in a number 4 times {3: "1234"}
    """
    string_dict = {}
    for i in base_dict.keys():
        string_dict[i] = [i for i in range(1, base_dict[i] + 1)]

    print(string_dict)

    # create all possible combinations between the prime factors
    combinations = list(it.product(*string_dict.values()))

    spisok = []
    for i in combinations:
        # print(i)
        num = calculating_number(primesL, i)
        spisok.append(num)

    # leave numbers less than limit
    final_spisok = set([num for num in spisok if num <= limit])
    print(final_spisok)

    if len(final_spisok) != 0:
        return [len(final_spisok), max(final_spisok)]
    else:
        return []

