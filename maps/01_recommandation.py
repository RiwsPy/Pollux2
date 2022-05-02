from . import Default_Config


class Config(Default_Config):
    ID = 1
    DATA = {
        'href': '/map/1',
        'template_name_or_list': 'maps/map_recommandation.html',
        'mapJSMethod': 'create_map_recommandation',

        'options': {'legend': 0},
        'legendName': 'Impact',
        'layers': [
            {'filename': 'trees_output.json',
             'layerName': 'Arbres',
             'layerType': 'cluster',
             'entityType': 'Tree',
             'icon': 'markers/tree.png'},

            {'filename': 'crossings_output.json',
             'layerName': 'Passages piétons',
             'layerType': 'cluster',
             'entityType': 'Crossing',
             'icon': 'markers/pedestrian.png'},

            {'filename': 'accidents_output.json',
             'layerName': 'Accidents de voiture de nuit',
             'layerType': 'node',
             'entityType': 'Accident',
             'icon': 'markers/accident.png'},

            {'filename': 'tc_ways_output.json',
             'layerName': 'Lignes de bus',
             'layerType': 'node',
             'entityType': 'BusLine'},

            {'filename': 'tc_stops_output.json',
             'layerName': 'Arrêts de transports en commun',
             'layerType': 'node',
             'entityType': 'PublicTransportStop',
             'icon': 'markers/busstop.png'},

            {'filename': 'parks_output.json',
             'layerName': 'Parcs',
             'layerType': 'node',
             'entityType': 'Park'},

            {'filename': 'birds_output.json',
             'layerName': 'Observations oiseau',
             'layerType': 'node',
             'entityType': 'Animal',
             'icon': 'markers/bird.png'},

            {'filename': 'shops_output.json',
             'layerName': 'Bâtiments accueillant du public',
             'layerType': 'cluster',
             'entityType': 'Shop',
             'icon': 'markers/shop.png'},

            {'filename': 'lamps_output.json',
             'layerName': 'Luminaires',
             'layerType': 'cluster',
             'entityType': 'Lamp',
             'icon': 'markers/lamp.png'},

            {'filename': 'highways_output.json',
             'layerName': 'Artères principales',
             'layerType': 'node',
             'entityType': 'Highway'},
        ],
        'description': {
            'title': "Carte des recommandations",
            'accroche': "Un outil permettant d'identifier dans une zone précise, les éléments impactant l'éclairage public et d'indiquer leurs recommandations.",
            'intro': """Sur cette carte vous êtes invités à créer votre propre zone géographique d'analyse.
                Celle-ci peut couvrir un quartier, une rue ou même le devant de votre porte.
                Une fois fait, Pollux identifie les différents éléments présents dans cette zone ayant un impact sur la politique d'éclairage public.
                Cela peut être un parc, un passage piétonnier, un arrêt de bus...
                Pollux va ensuite traduire ces éléments en recommandations d'éclairage.""",
            'icon': 'buttons/recommandation.png',
            'video': 'mp4/tuto_map_recommandations.mp4',
            'href': '/map_desc/1',
            'QR': [
                {
                    'Q': 'A quoi sert la zone de droite ?',
                    'R': """
                        Dans le panneau latéral droit, s'affichera les recommandations d'éclairage en fonction des éléments présents dans la zone que vous avez créé.
                        Ces recommandations sont issues des normes en vigueur ou bien d'associations engagées dans le domaine de l'éclairage public.

                        Certains termes peuvent être techniques alors n'hésitez pas à consulter notre <a href="/encyclopedia" target="_blank" class="invisible_link">encyclopédie<img src="../static/img/buttons/encyclopedie.png" width="40"></a>"""
                },
                {
                    'Q': 'Comment je crée une zone ?',
                    'R': """
                        La façon la plus élémentaire : c'est de cliquer sur la carte.
                        Un simple clic crée un cercle rouge d'un rayon de 10 mètres.

                        <img src="../static/img/button_dessin.png"> Il est possible de créer d'autres formes grâce à la barre de dessin. Essayez-les !"""
                },
                {
                    'Q': 'Comment je modifie une zone ?',
                    'R': """
                        Il est possible de déplacer, de modifier et de supprimer les formes créées.
                        <img src="../static/img/button_trash.png"> Il suffit de cliquer sur le bouton adéquat puis de cliquer sur la zone que vous souhaitez modifier.
                        Une fois terminé, n'oubliez pas de cliquer sur le bouton <img src="../static/img/button_save.png"> !"""
                },
                {
                    'Q': "Comment j'affiche les éléments dans une zone ?",
                    'R': """
                        Tout d'abord, en passant votre souris sur la forme créée, s'affichera le nombre des différents éléments trouvés.

                        Pour plus de détails, vous trouverez en haut à droite le bouton Calque. <img src="../static/img/button_calque.png">
                        En cliquant sur le ou les calques qui vous intéresse(nt) vous afficherez les éléments que vous désirez.

                        Deux calques particuliers sont présents :
                        <li><b>Zone Test</b> : affiche ou cache les limites de la zone couverte par Pollux, au-delà, c'est le vide !
                        <li><b>Mon Calque</b> : affiche ou cache les différentes formes que vous avez créé."""
                },
                {
                    'Q': "Et si je veux encore plus d'information sur les éléments affichés ?",
                    'R': """
                        Après avoir coché le calque correspondant aux éléments recherchés, il est possible de cliquer individuellement sur ces éléments.
                        Diverses informations sont renseignées comme par exemple l'espèce de l'arbre ou les horaires d'ouvertures du magasin."""
                },
                {
                    'Q': 'Et si je veux en savoir encore plus ?',
                    'R': """
                        Nous vous invitons à regarder la vidéo explicative en début de page. Bon visionnage !"""
                }
            ]
        },
    }
