from typing import Union
from heroes import Superman, SuperHero, HumanBeing
from places import Kostroma, Tokyo
from media import TVNews

# Added Media exemplar to the function for news output.


def save_the_place(hero: SuperHero, place: Union[Kostroma, Tokyo]):
    hero.find(place)
    hero.attack()
    if hero.can_use_ultimate_attack:
        hero.ultimate()
    TVNews(hero).making_news(place)


if __name__ == '__main__':
    save_the_place(Superman(), Kostroma())
    print('-' * 20)
    save_the_place(HumanBeing('Chack Norris'), Tokyo())
