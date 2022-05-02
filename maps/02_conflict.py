from . import Default_Config


class Config(Default_Config):
    ID = 2
    DATA = {
        'href': '/map/2',

        'options': {'draw': 0, 'legend': {
            'name': 'Contradiction'}},
        'layers': [
            {
                "layerName": "Jour",
                "layerType": 'heatmap_intensity',
                "filename": 'cross/contradiction_proximity_with_opening_hours--crossings-shops--trees--25.json',
            },
            {
                'layerName': 'Nuit',
                'layerType': 'heatmap_intensity',
                'filename': 'cross/contradiction_proximity_with_opening_hours--crossings-shops--trees--25.json',
            },
            {
                'layerName': 'Différence',
                'layerType': 'heatmap_intensity',
                'filename': 'cross/contradiction_proximity_with_opening_hours--crossings-shops--trees--25.json',
            },
        ],
        'description': {
            'title': "Carte de contradiction",
            'accroche': "Un outil mettant en lumière les zones exigeant un éclairage contradictoire en fonction de l'avancée de la nuit.",
            'intro': """L'objectif de la carte de contradiction est d'identifier les zones où sont présents des éléments dont les impacts sur la politique d'éclairage sont opposés.""",
            'icon': 'buttons/contradiction.png',
            'video': 'mp4/tuto_map_contradiction.mp4',
            'href': '/map_desc/2',
            'QR': [
                {
                    'Q': "Des éléments opposés ? C'est-à-dire ?",
                    'R': """
                    Ici, les besoins des passages piétons et les magasins sont opposés à la biodiversité.
                    En effet, les passages piétons représentent une zone d'insécurité où une forte intensité lumineuse et un excellent rendu des couleurs sont attendus.
                    Quant aux magasins, ils attirent les citoyens ce qui génère des zones à fort besoin lumineux, notamment pour le confort et l'impression de sécurité que la lumière apporte.

                    Pour ces deux raisons, l'éclairage public privilégie une luminosité <u>élevée</u> et une température de couleur <u>froide</u>.
                    En contradiction avec la biodiversité, qui préfère une luminosité <u>faible</u> et une température de couleur <u>chaude</u>."""
                },
                {
                    'Q': "Que faîtes-vous une fois ces zones de contradictions identifiées ?",
                    'R': """
                    Pour chacune d'entre elles, Pollux leur affecte une valeur en fonction de la densité des éléments identifiés comme contradictoires et de la distance les séparant.

                    Cette valeur est traduite sur une échelle de couleur allant du <span style="color: red;">rouge (niveau élevé)</span> au <span style="color: violet;">violet (niveau faible)</span>.""",
                },
                {
                    'Q': "A quelle valeur correspond la couleur rouge ou la couleur violette ?",
                    'R': """
                    La valeur des couleurs est détaillée dans la légende mais une couleur ne correspond pas à une valeur fixe.
                    Il nous faut rappeler que la carte est interactive : il est possible de zoomer et de dézoomer.
                    Dans ce cas, appliquer une échelle de valeur fixe à une carte évolutive n'est pas efficace : la carte ne serait exploitable que sur une tranche de zoom très limitée.
                    Afin de remédier à cela, nous avons opté pour une échelle aussi flexible que la carte !""",
                },
                {
                    'Q': "A quoi correspondent les calques ?",
                    'R': """
                    Sur cette carte, <b>3 calques sont disponibles</b> :
                    <ol>
                    <li><strong>Jour</strong> : indique les zones de contradiction en début de soirée.</i>
                    <li><strong>Nuit</strong> : indique les zones qui sont contradictoires à toute heure de la nuit et donc nécessitant une attention particulière.</i>
                    <li><strong>Différence</strong> : indique les zones présentant à la fois un besoin en lumière en net recul dans la nuit et une présence forte de biodiversité. Montrant ainsi les zones où l'intensité des luminaires peut être réduite dans la nuit afin de respecter au mieux la biodiversité à proximité.</i>
                    </ol>""",
                }
            ]
        },
    }
