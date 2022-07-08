# ссылка на задачи https://university.ylab.site/python/lecture-2-hw/


class CyclicIterator:

  def __init__(self, value):
    self.length = len(value)
    self.a = 0
    if type(value) in [set, frozenset]:
      self.value = list(value)
    else:
      self.value = value

  def __iter__(self):
    return self

  def __next__(self):
    x = self.value[self.a]
    self.a += 1
    if self.a == self.length:
      self.a = 0
    return x

list_example = CyclicIterator([1, 2, 3])
set_example = CyclicIterator(set([1, 2, 3]))
tuple_example = CyclicIterator((1, 2, 3))
range_example = CyclicIterator(range(1, 4))


if __name__ == "__main__":
    """ 
    # возьмем range такой, чтобы показать, что объект итерируется по кругу после того, 
    как в нем закончились эл-ты.
    """
    for i in range(6):
        print("Список - ", next(list_example))
        print("Множество - ", next(set_example))
        print("Кортеж - ", next(tuple_example))
        print("Диапозон - ", next(range_example))
        print("---------")