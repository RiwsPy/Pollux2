#!/usr/bin/env python
from website import app
from dotenv import load_dotenv
from pathlib import Path
import argparse
from importlib import import_module
import json
import os
from works import BASE_DIR

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent


def db_update(cls_type):
    cls_instance = cls_type()
    print(cls_instance.filename, 'en cours.')
    try:
        data = cls_instance.request()
        cls_instance.output(data)  # filter on request result and save it
    except FileNotFoundError:
        print('Error', cls_type, ': FileNotFound')


def db_cross_update(cls_type, max_range: int = 0):
    cls_instance = cls_type()
    print(cls_instance, 'en cours.')
    try:
        cls_instance.load(max_range=max_range)
        cls_instance.apply_algo()
        cls_instance.dump()
    except FileNotFoundError:
        print('Error', cls_type, ': FileNotFound')


def show_impact_biodivisity():
    with open(os.path.join(BASE_DIR, 'db', 'cross',
                           'impact_of_lamps_with_orientation--lamps_with_orientation--trees--25.json'),
              'r') as file:
        data = json.load(file)
        cumul_jour, cumul_jour_nerf = 0, 0
        cumul_nuit, cumul_nuit_nerf = 0, 0
        lamps_with_high_impact_jour = 0
        lamps_with_high_impact_nuit = 0
        for feature in data['features']:
            impact_jour = feature['properties']['_pollux_values'].get('Jour', 0)
            impact_nuit = feature['properties']['_pollux_values'].get('Nuit', 0)

            cumul_jour += impact_jour
            cumul_jour_nerf += min(1, impact_jour)

            cumul_nuit += impact_nuit
            cumul_nuit_nerf += min(1, impact_nuit)

            if impact_jour > 1:
                lamps_with_high_impact_jour += 1
            if impact_nuit > 1:
                lamps_with_high_impact_nuit += 1
        print(f'Impact Jour:', round(cumul_jour))
        print(f'Impact Nuit:', round(cumul_nuit))
        print('Nombre de luminaires:', len(data['features']))
        print(f"Nombre de luminaires à impact (Jour) > 1: {lamps_with_high_impact_jour}" +
              f" ({round(lamps_with_high_impact_jour / len(data['features']) * 100, 2)}%)")
        print(f"Nombre de luminaires à impact (Nuit) > 1: {lamps_with_high_impact_nuit}" +
              f" ({round(lamps_with_high_impact_nuit / len(data['features']) * 100, 2)}%)")
        print(f'Jour nerf à 1: {round(cumul_jour_nerf)}' +
              f' (-{100 - round(cumul_jour_nerf / cumul_jour * 100, 2)}%)')
        print(f'Nuit nerf à 1: {round(cumul_nuit_nerf)}' +
              f' (-{100 - round(cumul_nuit_nerf / cumul_nuit * 100, 2)}%)')


def show_crossing_lake():
    with open(os.path.join(BASE_DIR, 'db', 'cross',
                           'quality_of_lamps--crossings--lamps_with_orientation--25.json'),
              'r') as file:
        data = json.load(file)
        crossing_with_low_impact_day = 0
        crossing_with_low_impact_night = 0
        for feature in data['features']:
            day_impact = feature['properties']['_pollux_values'].get('Jour', 0)
            night_impact = feature['properties']['_pollux_values'].get('Nuit', 0)
            if 0 < day_impact < 0.5:
                crossing_with_low_impact_day += 1
            if 0 < night_impact < 0.5:
                crossing_with_low_impact_night += 1

        nb_features = len(data['features'])
        print(f"Nombre de passage piétons : {nb_features}")
        print(f"Nombre de passage piétons peu éclairé (jour) : {crossing_with_low_impact_day} ({round(crossing_with_low_impact_day/nb_features*100, 2)}%)")
        print(f"Nombre de passage piétons peu éclairé (nuit) : {crossing_with_low_impact_night} ({round(crossing_with_low_impact_night/nb_features*100, 2)}%)")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pollux - Fonctionnalités.')
    parser.add_argument("-uDB", "--updateDB",
                        nargs='*',
                        help="Mettre à jour les bases de données de l'application.")
    parser.add_argument("-uCDB", "--updateCrossDB",
                        nargs='*',
                        help="Appliquer un algorithme pour mettre à jour une base de données croisée.")
    parser.add_argument("-mr", "--maxRange")
    parser.add_argument("-cImpact", "--cumulImpact")
    args = parser.parse_args()

    if args.updateDB is not None:
        db_args = args.updateDB
        for db_arg in db_args:
            arg = db_arg.replace('.py', '').replace('/', '.')
            try:
                cls = import_module(arg).Works
            except ModuleNotFoundError:
                print(f'Module {arg} introuvable.')
            except AttributeError:
                print(f'Classe {arg}.Works introuvable.')
            else:
                db_update(cls)
        print('Mise à jour terminée.')
    elif args.updateCrossDB is not None:
        arg = args.updateCrossDB[0].replace('.py', '').replace('/', '.')
        try:
            cls = import_module(arg).Cross
        except ModuleNotFoundError:
            print(f'Module {arg} introuvable.')
        except AttributeError:
            print(f'Classe {arg}.Cross introuvable.')
        else:
            db_cross_update(cls, max_range=int(args.maxRange or 0))
        print('Mise à jour terminée.')
    elif args.maxRange is not None:
        print("Utilisable qu'avec la commande --updateCrossDB.")
    elif args.cumulImpact is not None:
        show_impact_biodivisity()
        print('-----------')
        show_crossing_lake()
    else:
        app.run()
