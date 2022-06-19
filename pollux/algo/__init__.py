from pollux.works import MAX_BOUND_LNG_LAT


class Default_cross:
    filename = 'cross_default.json'
    bound = MAX_BOUND_LNG_LAT

    def pre_pre_algo(self) -> None:
        print(self.__class__, 'activé.')
        print("Préparation du calcul...")

    def pre_algo(self, *args) -> None:
        pass

    def apply_algo(self) -> None:
        print("Calcul en cours...")

    def post_algo(self) -> None:
        print('Finitions en cours...')

    def run(self, *args) -> None:
        self.pre_pre_algo()
        self.pre_algo(*args)
        self.apply_algo()
        self.post_algo()
