from abc import ABC, abstractmethod
from typing import List

# Created the abstract Place class so that I can make inherited from it with obligatory method "get_evil".


class Place(ABC):
    @abstractmethod
    def get_evil(self):
        ...


class Kostroma(Place):
    city_name = 'Kostroma'

    def get_orcs(self):
        print('Orcs hid in the forest')

    def get_evil(self):
        self.get_orcs()


class Tokyo(Place):
    city_name = 'Tokyo'

    def get_godzilla(self):
        print('Godzilla stands near a skyscraper')

    def get_evil(self):
        self.get_godzilla()

# Added Planet class for notifying implementation in the Media class.


class Planet:

    def __init__(self, coordinates: List[float]):
        self.coordinates = coordinates


