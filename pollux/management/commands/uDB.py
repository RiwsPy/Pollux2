from django.core.management.base import BaseCommand
from importlib import import_module


class Command(BaseCommand):
    help = 'Update database'

    def add_arguments(self, parser):
        parser.add_argument('db_name', nargs='*', type=str)

    def handle(self, *args, **kwargs) -> None:
        self.call_api(**kwargs)
        self.stdout.write(
            self.style.SUCCESS('Mise à jour de la base de données réussie.'))

    @staticmethod
    def call_api(**kwargs) -> None:
        db_args = kwargs.get('db_name')
        for db_arg in db_args:
            arg = db_arg.replace('.py', '').replace('/', '.')
            try:
                cls = import_module(arg).Works
            except ModuleNotFoundError as e:
                print(f'Module {arg} introuvable.')
                print(e)
            except AttributeError as e:
                print(f'Classe {arg}.Works introuvable.')
                print(e)
            else:
                db_update(cls)
                if cls.filename == 'lamps':
                    """
                    from pollux.models.lamps import Lamps
                    import os
                    import json
                    from pollux.works import BASE_DIR

                    from pollux.algo.create_line_from_point_and_orientation import create_line
                    geo = create_line(Lamps, 20)
                    with open(os.path.join(BASE_DIR, 'pollux', 'db', 'lamps_line.json'), 'w+') as file:
                        json.dump(geo, file)
                    """
                    print('A effectuer :')
                    print('uCDB algo/complete_lamp_with_greenalpdata.py')
                    print('uCDB algo/set_orientation_to_lamps.py')
                    print('uCDB algo/lamp_impact_tree.py')


def db_update(cls_type):
    cls_instance = cls_type()
    print(cls_instance.filename, 'en cours.')
    try:
        data = cls_instance.request()
        cls_instance.output(data)  # filter on request result and save it
    except FileNotFoundError:
        print('Error', cls_type, ': FileNotFound')
