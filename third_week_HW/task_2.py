import time

def decorator_params(call_count=2, start_sleep_time=5, factor=2, border_sleep_time=30):
    def decorator(func):
        def wrapper(*args):
            print(f"Количество запусков = call_count({call_count}).")
            print("Начало работы.")
            print("Вызов функции без задержки:")
            func()
            print("Повторные вызовы функции:")
            for exp in range(0,call_count):
                # Время ожидания запуска функции
                t = start_sleep_time * factor ** exp
                if t < border_sleep_time:
                    time.sleep(t)
                else:
                    t = border_sleep_time
                    time.sleep(t)
                print(f"Запуск номер {exp+1}. Ожидание {t} секунд. Результат работы декорируемой функции =", end=" ")
                value = func()
            print("Конец работы.")
            return value
        return wrapper
    return decorator

@decorator_params(call_count=5, start_sleep_time=1, factor=2, border_sleep_time=20)
def function():
    print("Функция работает.")


if __name__ == "__main__":
    function()