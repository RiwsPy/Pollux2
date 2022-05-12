from pollux.works import MAX_BOUND_LNG_LAT


class Default_cross:
    filename = 'cross_default.json'

    def __init__(self):
        self.bound = MAX_BOUND_LNG_LAT

    def pre_pre_algo(self):
        print(self.__class__, 'activé.')
        print("Préparation du calcul...")

    def apply_algo(self) -> None:
        print("Calcul en cours...")

    def post_algo(self) -> None:
        print('Finitions en cours...')
