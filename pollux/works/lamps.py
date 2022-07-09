from . import Default_works
from pollux.api_ext.grenoble_alpes_metropole import Gam
from pollux.models.lamps import Lamps
from pollux.formats.csv import convert_to_geojson


lowering_night_impact = {
    "": 0,
    "GRE NOCTURNE": 0,
    "CREM NOCTURNE": 0,
    "4150h": 0,
    "GRE PERMANENT": 0,
    "CREM PERMANENT": 0,
    "GRE AUTONOME": 0,  # ??
    "GRE NOCTURNE AVEC TELEGESTION": 0,
    "CREM NOCTURNE AVEC DETECTION  10%": 0,
    "CREM NOCTURNE AVEC DETECTION  20%": 0,
    "GRE NOCTURNE PROLONGE 2H (1H Avant +1H Aprés)": 0,
    "CREM NOCTURNE AVEC COUPURE ST2": 0,  # TODO !?
    "CREM NOCTURNE AVEC REDUCTION 33% flux - 33 % NRJ en milieu de nuit (LED)": 33,
    "CREM NOCTURE AVEC REDUCTION 50% flux - 40 % NRJ en milieu de nuit": 50,
    "CREM NOCTURNE AVEC REDUCTION 50% flux - 50 % NRJ en milieu de nuit (LED)": 50,
    "GRE NOCTURNE AVEC REDUCTION Bi-Pw (Réduction de 30% de 22h40 à 5h40)": 30,
    "CREM NOCTURNE AVEC VARIATIEUR (Réduction de  50 % flux - 40 % puissance de 23h à 6h)": 50,
    "CREM NOCTURNE AVEC REDUCTION 80% flux - 80 % NRJ en milieu de nuit (LED)": 80,
    "CREM NOCTURNE AVEC REDUCTION 50% de 22h à 0h et de 70% de 0h à 5h et 50% de 5h à 6h": 50,  # TODO
    "GRE NOCTURNE AVEC REDUCTION VARIATEUR LUBIO (Réduction de 30 % de 23h à 6h)": 30,
    "CREM NOCTURNE AVEC VARIATIEUR BH (Réduction de  33 % flux - 27 % puissance de 22h à 6h)": 33,
    "CREM NOCTURE AVEC REDUCTION 33% flux - 27 % NRJ en milieu de nuit": 33,
    "GRE NOCTURNE AVEC COMPTAGE (Eclairage à la demande)": 0,
}


class Works(Default_works):
    filename = "lamps"
    file_ext = "csv"
    COPYRIGHT_ORIGIN = Gam.BASE_URL
    COPYRIGHT_LICENSE = "ODbL"
    fake_request = True
    model = Lamps

    def _can_be_output(self, feature: "Model", bound=None, **kwargs) -> bool:
        return super()._can_be_output(feature, bound=bound)

    @staticmethod
    def convert_to_geojson(directory_file: str) -> dict:
        return convert_to_geojson(directory_file)

    class Model(Default_works.Model):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            properties = kwargs["properties"]
            self.code = properties["Luminaire - Code luminaire"]
            self.height = float(properties["Luminaire - Hauteur de feu"] or 8.0)
            self.irc = int(properties["Lampe - IRC"] or 75)
            self.power = 150  # TODO: donnée à trouver (W)
            self.colour = int(properties["Lampe - Température Couleur"] or 5000)
            self.on_motion = self.is_on_motion(properties)
            self.lowering_night = lowering_night_impact.get(
                properties["Lampe - Régime"], 0
            )
            self.orientation = -1

        @staticmethod
        def is_on_motion(properties) -> bool:
            return properties["Lampe - Régime"] in (
                "CREM NOCTURNE AVEC DETECTION  10%",
                "CREM NOCTURNE AVEC DETECTION  20%",
                "GRE NOCTURNE AVEC TELEGESTION",
            )
