from antagonistfinder import AntagonistFinder
from weapon import Gun, Lasers, MeleeWeapon

# Added attack method for inheriting in SuperHero class.


class SuperHero:

    def __init__(self, name, can_use_ultimate_attack=True):
        self.name = name
        self.can_use_ultimate_attack = can_use_ultimate_attack
        self.finder = AntagonistFinder()

    def find(self, place):
        self.finder.get_antagonist(place)

    def attack(self, use_weapon=True):
        pass


# Created special class for very strong human beings like Chack Norris.

class HumanBeing(SuperHero, Gun, MeleeWeapon):

    def __init__(self, name):
        super(HumanBeing, self).__init__(name, False)

    def attack(self, use_weapon=True):

        if use_weapon:
            self.fire_a_gun()
        else:
            self.roundhouse_kick()


class Superman(SuperHero, Lasers, MeleeWeapon):

    def __init__(self):
        super(Superman, self).__init__(name='Clark Kent', can_use_ultimate_attack=True)

    def ultimate(self):
        self.incinerate_with_lasers()

    def attack(self, use_weapon=False):
        self.roundhouse_kick()





