# ссылка на задачи https://university.ylab.site/python/lecture-2-hw/

class Range2:
    def __init__(self, stop_value: int):
        self.current = -1
        self.stop_value = stop_value - 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < self.stop_value:
            self.current += 1
            return self.current
        else:
            self.current = 0
            return self.current


class CyclicIterator:

  def __init__(self, value):
      self.value = value
      # Cоздаем итератор.
      self.iter = iter(self.value)


  def __iter__(self):
    return self

  def __next__(self):
    try:
        # Выводим элементы пока коллекция не станет пустой.
        return(next(self.iter))
    except StopIteration:
        # Как только элементы в коллекции заканчиваются, мы должны заново создать итератор.
        self.iter = iter(self.value)
        return next(self.iter)

list_example = CyclicIterator([1, 2, 3])
set_example = CyclicIterator(set([1, 2, 3]))
tuple_example = CyclicIterator((1, 2, 3))
range_example = CyclicIterator(range(1, 4))
Range2_example = CyclicIterator(Range2(3))


if __name__ == "__main__":
    """ 
    # Возьмем в цикле range такой, чтобы показать, что объект итерируется по кругу после того, 
    как в нем закончились элементы.
    """
    for i in range(6):
        print("Список - ", next(list_example))
        print("Множество - ", next(set_example))
        print("Кортеж - ", next(tuple_example))
        print("Диапозон - ", next(range_example))
        print("Range2 - ", next(Range2_example))
        print("---------")