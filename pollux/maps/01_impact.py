from . import *


class Config(Default_Config):
    ID = 1
    LAYER_BASE = Layer('', '', '',
                       Gradient('LIGHT_COLORED'),
                       Blur(unit='%', fix=35),
                       MaxValue(method='fix', fix=50),
                       Filters(position__within=[5.704337, 45.182177, 5.722755, 45.184826])
                       )
    DATA = {
        'options': Options(
            Legend(name='Impact'),
            #bbox=[5.717633, 45.182596, 5.734348, 45.185410],
        ),
        'layers': [
            Layer(
                'Luminaires (Impact - Jour)',
                'heatmap',
                'lamps',
                Radius(field='max_range_day', unit='auto'),
                Value(field='day_impact'),
                Orientation(field='orientation'),
                HorizontalAngle(field='horizontal_angle'),
                IsActive(True),
            ),
            Layer(
                'Luminaires (Impact - Nuit)',
                'heatmap',
                'lamps',
                Radius(field='max_range_night', unit='auto'),
                Value(field='night_impact'),
                Orientation(field='orientation'),
                HorizontalAngle(field='horizontal_angle'),
            ),
            Layer(
                'Luminaires',
                'cluster',
                'lamps',
                Icon('LAMP'),
            ),
            Layer(
                'Arbres (Impact - Jour)',
                'heatmap',
                'trees',
                Value(field='day_impact'),
                MaxValue(method='part%', fix=90),
                Radius(fix=15, unit='auto'),
            ),
            Layer(
                'Arbres (Impact - Nuit)',
                'heatmap',
                'trees',
                Value(field='night_impact'),
                MaxValue(method='part%', fix=90),
                Radius(fix=15, unit='auto'),
            ),
            Layer(
                'Arbres',
                'cluster',
                'trees',
                Icon('TREE'),
            ),
        ],
        'description': {
            'title': "Carte d'impact",
            'accroche': "Une carte interactive mesurant l'impact des luminaires de l'espace public sur la biodiversité.",
            'intro': """Cette carte permet de visualiser l'impact des luminaires sur la biodiversité locale.""",
            'icon': 'buttons/impact.png',
            'video': 'mp4/tuto_map_impact.mp4',
            'href': '/map_desc/1',
            'QR': [
                {
                    'Q': "Comment est calculé l'impact des luminaires ?",
                    'R': """
                        Pollux affecte à chaque luminaire une première valeur d'impact, qui dépend de plusieurs facteurs :
                        <li>La quantité d'objets éclairés par la source lumineuse</li>
                        <li>La distance entre l'ampoule et l'objet éclairé</li>""",
                },
                {
                    'Q': "Pourquoi parler d'une distance de l'ampoule plutôt que du luminaire ?",
                    'R': """
                        Pour le calcul d'impact, la distance est un facteur clé.
                        Car <u>multiplier la distance par 2, c'est diviser l'impact par 4</u>.
                        Pour cette raison, la valeur de la distance doit être aussi précise que possible.
                        Dans ce cas, la géolocalisation des objets est nécessaire mais insuffisante.

                        Prenons un exemple :
                        Si je me place sous un luminaire, quelle distance nous sépare ?
                        En théorie, lui et moi sommes à la même position, donc <u>la distance est nulle</u>.
                        Ce raisonnement est correct sauf que ce n'est pas le luminaire qui m'éclaire mais son ampoule !

                        Ainsi en restant sous le luminaire, si je mesure 1m80 et le luminaire 8 mètres, <u>la distance devient 6m20</u>.
                        L'impact n'est plus le même.

                        De plus, cette valeur sert de base pour les calculs suivants.
                        En effet, plusieurs données permettent d'affiner ce premier résultat.""",
                },
                {
                    'Q': "Quelles sont les autres données impactantes ?",
                    'R': """
                        <b>1.</b> La puissance de l'ampoule
                        Une ampoule de 20W possède un impact 3 fois plus faible qu'une ampoule de 60W.
                        <b>2.</b> L'orientation du luminaire
                        De nombreux luminaires sont orientés vers une voie, se trouver à 1 mètre devant le luminaire ou 1 mètre derrière est complètement différent.
                        <b>3.</b> La température de couleur de l'ampoule
                        Une température de couleur basse (ou chaud) a un impact plus faible qu'une température haute (ou froide).
                        <b>4.</b> La détection de présence
                        Nous considérons également que les luminaires fonctionnant par détection possèdent un impact faible, du fait de leur faible durée d'éclairage.
                        <b>5.</b> Le type de régime
                        Il est courant que les luminaires possèdent deux plages de fonctionnement :
                        la première pour la soirée et le matin, la seconde pour la nuit.

                        Pour prendre en compte ce dernier paramètre, deux calques sont disponibles : <b>Jour</b> et <b>Nuit</b>.
                        Un luminaire dont le flux lumineux est réduit de 50% pendant la nuit, voit son impact réduit de 50% sur le calque Nuit.

                        Enfin, cette valeur d'impact est traduite sur une échelle de couleur allant du <span style="color: red;">rouge (niveau élevé)</span> au <span style="color: violet;">violet (niveau faible)</span>.""",
                },
                {
                    'Q': "A quoi sert le calque <i>Luminaires</i> ?",
                    'R': """
                        A la différence de la <a href="/map_desc/2" target="_blank" class="invisible_link">carte de Contradiction</a> qui signale des zones, celle-ci éclaire les luminaires - un comble pour eux.
                        C'est-à-dire que chaque point correspond exactement à un luminaire.
                        Avec les calques Jour et Nuit, il était possible d'identifier les positions des luminaires à fort impact.
                        Mais en rajoutant le calque <i>Luminaires</i>, Pollux va plus loin.
                        Car il permet également à l'utilisateur d'accéder aux caractéristiques du luminaire sur lequel il clique.""",
                },
                {
                    'Q': "A quoi peut servir le calque <i>Arbres</i> ?",
                    'R': """
                    Le calque Arbre est un calque d'essai.
                    Il inverse le référentiel d'étude : plutôt que de connaître l'impact généré par les luminaires, il présente l'impact reçu par les arbres.
                    Cela présente deux avantages :
                    <li>Il permet de mieux apprécier l'environnement proche des luminaires.</li>
                    <li>C'est également un moyen de vérifier la cohérence des résultats : chaque luminaire a fort impact devrait avoir un ou plusieurs arbres à proximité, et inversement !</li>"""
                },
            ]
        },
    }
