from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Generator, List, Tuple

@dataclass
class Movie:
    title: str
    dates: List[Tuple[datetime, datetime]]

    def schedule(self) -> Generator[datetime, None, None]:
        # Создаем список, куда будем класть даты в заданном диапазоне.
        days = []
        # Перебираем все диапазоны в списке.
        for i in range(len(self.dates)):
            # В каждом диапазоне ищем разницу в днях между концом и стартом.
            for day in range((self.dates[i][1] - self.dates[i][0]).days + 1):
                date = self.dates[i][0]
                # Прибавляем к начальному дню разницу.
                date += timedelta(days=day)
                days.append(date)
        return days


if __name__ == "__main__":
    m = Movie('sw', [
      (datetime(2020, 1, 1), datetime(2020, 1, 7)),
      (datetime(2020, 1, 15), datetime(2020, 2, 7))
    ])

    for d in m.schedule():
        print(d)