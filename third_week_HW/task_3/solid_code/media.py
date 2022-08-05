from abc import ABC, abstractmethod
from places import Place, Planet
from heroes import SuperHero


class Media(ABC):

    def __init__(self, hero: SuperHero):
        self.hero_name = getattr(hero, "name")

    @abstractmethod
    def making_news(self, place: Place):
        pass


class TVNews(Media):

    def __init__(self, hero: SuperHero):
        super(TVNews, self).__init__(hero)

    def making_news(self, place: Place):
        place_name = getattr(place, 'city_name')
        print(f"BREAKING news on TV:\n{self.hero_name} saved {place_name}!!!")


# Class Media is responsible for notifying news about the SuperHero`s victory.

class PlanetNotifier:

    def __init__(self, hero: SuperHero):
        self.hero_name = getattr(hero, "name")

    def planet_notifier(self, planet: Planet):
        planet_coordinates = getattr(planet, 'coordinates')
        print(f"{self.hero_name} saved the planet with the coordinates - {planet_coordinates}")

