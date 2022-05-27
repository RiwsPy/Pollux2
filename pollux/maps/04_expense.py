from . import *


class Config(Default_Config):
    ID = 4
    LAYER_BASE = Layer('', '', '',
                       MaxValue(method='part%',
                                fix=60)
                       )
    DATA = {
        'options': Options(
            Zoom(max=19, init=18),
            Legend(name='Dépense €/an'),
            bbox=[5.717633, 45.182596, 5.734348, 45.185410],
        ),
        'layers': [
            Layer(
                'Luminaires (Chaleur)',
                'heatmap',
                'lamps',
                Gradient('BLUEBELT'),
                Orientation(field='orientation'),
                HorizontalAngle(field='horizontal_angle'),
                Radius(fix=15, unit='auto'),
                MaxValue(method='fix', fix=114.4),
                IsActive(True),
                Value(field='expense'),
            ),
            Layer(
                'Luminaires',
                'cluster',
                'lamps',
                Icon('LAMP'),
            ),
        ],
        'description': {
            'title': "Carte de dépense",
            'accroche': "Une carte interactive mesurant le coût financier des luminaires de l'espace public.",
            'intro': """Cette carte permet de visualiser où l'argent part mais pas de le faire revenir.""",
            'icon': 'buttons/contradiction.png',
            'href': '/map_desc/4',
            'QR': [
                {
                    'Q': "",
                    'R': """-- Carte en construction --
                        Elle affiche simplement le coût de fonctionnement des luminaires, de nombreuses inconnues sont à déterminer, elle prend en compte :
                        <li>La puissance du luminaire</li>
                        <li>La baisse d'activité nocturne</li>
                        <li>Le prix du kWh (prix client officiel)</li>
                        <br>
                        Il manque <u>au minimum</u> :
                        <li>Le coût du kWh pour les communes</li>
                        <li>La puissance nécessaire pour alimenter la douille</li>
                        <li>Le coût de l'entretien courant</li>
                        <li>Les données complètes sur la puissance des luminaires</li>
                        <br>
                        En bonus :
                        <li>Des données sur les heures de coucher/lever de soleil en fonction des montagnes environnantes et pas uniquement qu'en fonction des positions</li>
                        <li>3 calques : Hiver/Eté/Intersaison ?""",
                }
            ]
        },
    }
