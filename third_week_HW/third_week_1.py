def cashing_decorator(func) -> int:

    # создаем словарик(кэш), куда будем складывать результаты работы функции
    cash = {}
    def wrapper(*args):
        # результат выполнения функции "multiplier"
        result = func(*args)
        # проверяем, есть ли такой результат функции в кэше
        if args in cash:
            print("Если наш декоратор работает и значение есть в кэше, то это строка выведится на экран")
            return cash[args]
        else:
            print("Такого значения функции multiplier нет в кэше, поэтому записываем его туда")
            cash[args] = result
            return result
    return wrapper

@cashing_decorator
def multiplier(number: int):
    return number * 2


# создадим список, куда положим несколько значений, чтобы проверить работу нашего декоратора
checking = [5, 5, 10, 10]
for num in checking:
    print(multiplier(num))
print()
