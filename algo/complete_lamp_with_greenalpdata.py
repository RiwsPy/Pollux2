from . import Default_cross
from pollux.models.lamps import Lamps
from pollux.works import BASE_DIR
import os
import json
from pollux.formats.position import Position


class Cross(Default_cross):
    def pre_algo(self):
        print('Préparation des luminaires...')
        self.lamps_queryset = Lamps.objects.all()

        print('Préparation des données de GreenAlp')
        with open(os.path.join(BASE_DIR, 'db', 'data patrimoines EP_output.json'), 'r') as file:
            green_data = json.load(file)

        self.lum_id_to_green_data = dict()
        for feature in green_data['features']:
            self.lum_id_to_green_data[feature['properties']['code']] = feature

    def apply_algo(self):
        super().apply_algo()
        nb_power_change = 0
        for lamp in self.lamps_queryset:
            green_data = self.lum_id_to_green_data.get(lamp.code)
            if green_data:
                distance_between = Position(lamp.position).distance(green_data["geometry"]["coordinates"])
                if distance_between <= 5:
                    green_properties = green_data['properties']
                    if lamp.irc == 75 and green_properties['irc'] != -1:
                        lamp.irc = green_properties['irc']
                    if green_properties['power'] != 0:
                        lamp.power = green_properties['power']
                        nb_power_change += 1
                    lamp.save()
        change_percent = round(nb_power_change/Lamps.objects.all().count()*100, 2)
        print(f'{nb_power_change} modifications de puissance effectuées ({change_percent}%).')
