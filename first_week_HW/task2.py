def int32_to_ip(int32):

    dvoich = bin(int32)[2:]
    diff = 32 - len(dvoich)

    nulls = ""
    for i in range(diff):
        k = "0"
        nulls += k
    ultimate_dvoich = nulls + dvoich

    digits = []
    for i in range(0, len(ultimate_dvoich), 8):
        ip = str(int(ultimate_dvoich[i:(i + 8)], base=2))
        digits.append(ip)

    return ".".join(digits)

