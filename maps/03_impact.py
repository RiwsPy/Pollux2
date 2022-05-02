from . import Default_Config


class Config(Default_Config):
    ID = 3
    DATA = {
        'href': '/map/3',

        'options': {'draw': 0, 'legend': {
            'name': 'Impact'}},
        'layers': [
            {
                'layerName': 'Jour',
                'layerType': 'heatmap_intensity',
                'filename': 'cross/impact_of_lamps--lamps--trees--25.json',
            },
            {
                'layerName': 'Nuit',
                'layerType': 'heatmap_intensity',
                'filename': 'cross/impact_of_lamps--lamps--trees--25.json',
            },
            {
                'layerName': 'Différence',
                'layerType': 'heatmap_intensity',
                'filename': 'cross/impact_of_lamps--lamps--trees--25.json',
            },
            {
                'layerName': 'Luminaires',
                'layerType': 'cluster',
                'filename': 'cross/impact_of_lamps--lamps--trees--25.json',
                'icon': 'markers/lamp.png',
                'entityType': 'Lamp',
            },
            {
                'layerName': 'Jour (arbre)',
                'valueName': 'Jour',
                'layerType': 'heatmap_intensity',
                'filename': 'cross/impact_from_lamps--trees--lamps--25.json',
            },
            {
                'layerName': 'Nuit (arbre)',
                'valueName': 'Nuit',
                'layerType': 'heatmap_intensity',
                'filename': 'cross/impact_from_lamps--trees--lamps--25.json',
            },
            {
                'layerName': 'Arbres',
                'layerType': 'cluster',
                'filename': 'cross/impact_from_lamps--trees--lamps--25.json',
                'icon': 'markers/tree.png',
                'entityType': 'Tree',
            },
        ],
        'description': {
            'title': "Carte d'impact",
            'accroche': "Une carte interactive mesurant l'impact des luminaires de l'espace public sur la biodiversité.",
            'intro': """Cette carte permet de visualiser l'impact des luminaires sur la biodiversité locale.""",
            'icon': 'buttons/impact.png',
            'video': 'mp4/tuto_map_impact.mp4',
            'href': '/map_desc/3',
            'QR': [
                {
                    'Q': "Comment est calculé l'impact des luminaires ?",
                    'R': """
                        Pollux affecte à chaque luminaire une première valeur d'impact, qui dépend de deux facteurs :
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
                        <b>1.</b> La température de couleur de l'ampoule
                        Nous considérons qu'une température inférieure à 2500 Kelvins possède un impact faible sur la biodiversité.
                        <b>2.</b> La détection de présence
                        Nous considérons également que les luminaires fonctionnant par détection possèdent un impact faible, du fait de leur faible durée d'éclairage.
                        <b>3.</b> Le type de régime
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
