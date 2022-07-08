
# def decorator_params(call_count=1, start_sleep_time=5, factor=2, border_sleep_time=30):
#     pass
import time

def decorator_params(call_count=2, start_sleep_time=5, factor=2, border_sleep_time=30):
    def decorator(func):
        def wrapper(*args):
            print(f"Количество запусков = call_count({call_count})")
            print("Начало работы")
            t = start_sleep_time
            for exp in range(1,call_count + 1):
                if t < border_sleep_time:
                    time.sleep(t)
                else:
                    t = border_sleep_time
                    time.sleep(t)
                print(f"Запуск номер {exp}. Ожидание {t} секунд. Результат работы декорируемой функции =", end=" ")
                value = func()
                t *= 2**factor
            print("Конец работы")
            return value
        return wrapper
    return decorator

@decorator_params(call_count=3)
def function():
    print("Функция работает")



if __name__ == "__main__":
    function()