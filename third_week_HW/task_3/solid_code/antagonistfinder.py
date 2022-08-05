from places import Place

# Now the class doesn't take the specific place class, it takes the abstract class.


class AntagonistFinder:

    @staticmethod
    def get_antagonist(evil_finder: Place):
        evil_finder.get_evil()


