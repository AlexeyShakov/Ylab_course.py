def cashing_decorator(func) -> int:

    # Создаем словарик(кэш), куда будем складывать результаты работы функции.
    cash = {}
    def wrapper(*args):
        # Результат выполнения функции "multiplier".
        result = func(*args)
        # Проверяем, есть ли такой результат функции в кэше.
        if args in cash:
            print(f"Если наш декоратор работает и значение параметра({args[0]}) есть в кэше,"
                  f"то эта строка выведится на экран")
            return cash[args]
        else:
            print(f"Такого параметра({args[0]}) функции multiplier нет в кэше, поэтому записываем его туда")
            cash[args] = result
            return result
    return wrapper

@cashing_decorator
def multiplier(number: int):
    return number * 2


if __name__ == "__main__":
    # Создадим список, куда положим несколько значений, чтобы проверить работу нашего декоратора.
    checking = [5, 5, 10, 10]
    for num in checking:
        print(multiplier(num))

