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

    def call_api(self, **kwargs) -> None:
        db_args = kwargs.get('db_name')
        for db_arg in db_args:
            arg = db_arg.replace('.py', '').replace('/', '.')
            try:
                cls = import_module(arg).Cross
            except ModuleNotFoundError:
                print(f'Module {arg} introuvable.')
            except AttributeError:
                print(f'Classe {arg}.Cross introuvable.')
            else:
                db_update(cls)


def db_update(cls_type):
    cls_instance = cls_type()
    try:
        cls_instance.pre_pre_algo()
        cls_instance.pre_algo()
        cls_instance.apply_algo()
        cls_instance.post_algo()
    except FileNotFoundError:
        print('Error', cls_type, ': FileNotFound')
