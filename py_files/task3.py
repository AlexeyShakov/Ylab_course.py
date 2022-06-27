def zeros(n):

    null_counter = 0
    # the number of trailing null has correlation with the amount of 5s in the factorial of a digit
    i = 5
    while n / i >= 1:
        null_counter += n // i
        i *= 5
    return null_counter


