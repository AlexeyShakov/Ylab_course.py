from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Generator, List, Tuple

@dataclass
class Movie:
    title: str
    dates: List[Tuple[datetime, datetime]]

    def schedule(self) -> Generator[datetime, None, None]:
        # Перебираем все диапазоны в списке.
        for i in range(len(self.dates)):
            # Сохраняем начало и конец диапазона в переменные
            start = self.dates[i][0]
            end = self.dates[i][1]
            while start <= end:
                yield start
                start += timedelta(days=1)


if __name__ == "__main__":
    m = Movie('sw', [
      (datetime(2020, 1, 1), datetime(2020, 1, 7)),
      (datetime(2020, 1, 15), datetime(2020, 2, 7))
    ])
    print("Проверка, что данное выражение действительно генератор:\n", m.schedule())
    print("-------------------")
    for d in m.schedule():
        print(d)
