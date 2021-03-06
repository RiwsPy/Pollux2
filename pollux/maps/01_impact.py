from . import *


class Config(Default_Config):
    ID = 1
    LAYER_BASE = Layer('', '', '',
                       Gradient('LIGHT_COLORED'),
                       Blur(unit='%', fix=35),
                       MaxValue(method='fix', fix=100),
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
                Radius(unit='pixel'),
                # Radius(field='max_range_day', unit='auto'),
                MaxValue(method='part%', fix=80),
                Value(field='day_impact'),
                # Orientation(field='orientation'),
                # HorizontalAngle(field='horizontal_angle'),
                IsActive(True),
            ),
            Layer(
                'Luminaires (Impact - Nuit)',
                'heatmap',
                'lamps',
                Radius(unit='pixel'),
                MaxValue(method='part%', fix=80),
                # Radius(field='max_range_night', unit='auto'),
                Value(field='night_impact'),
                # Orientation(field='orientation'),
                # HorizontalAngle(field='horizontal_angle'),
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
            'accroche': "Une carte interactive mesurant l'impact des luminaires de l'espace public sur la biodiversit??.",
            'intro': """Cette carte permet de visualiser l'impact des luminaires sur la biodiversit?? locale.""",
            'icon': 'buttons/impact.png',
            'video': 'mp4/tuto_map_impact.mp4',
            'href': '/map_desc/1',
            'QR': [
                {
                    'Q': "Comment est calcul?? l'impact des luminaires ?",
                    'R': """
                        Pollux affecte ?? chaque luminaire une premi??re valeur d'impact, qui d??pend de plusieurs facteurs :
                        <li>La quantit?? d'objets ??clair??s par la source lumineuse</li>
                        <li>La distance entre l'ampoule et l'objet ??clair??</li>""",
                },
                {
                    'Q': "Pourquoi parler d'une distance de l'ampoule plut??t que du luminaire ?",
                    'R': """
                        Pour le calcul d'impact, la distance est un facteur cl??.
                        Car <u>multiplier la distance par 2, c'est diviser l'impact par 4</u>.
                        Pour cette raison, la valeur de la distance doit ??tre aussi pr??cise que possible.
                        Dans ce cas, la g??olocalisation des objets est n??cessaire mais insuffisante.

                        Prenons un exemple :
                        Si je me place sous un luminaire, quelle distance nous s??pare ?
                        En th??orie, lui et moi sommes ?? la m??me position, donc <u>la distance est nulle</u>.
                        Ce raisonnement est correct sauf que ce n'est pas le luminaire qui m'??claire mais son ampoule !

                        Ainsi en restant sous le luminaire, si je mesure 1m80 et le luminaire 8 m??tres, <u>la distance devient 6m20</u>.
                        L'impact n'est plus le m??me.

                        De plus, cette valeur sert de base pour les calculs suivants.
                        En effet, plusieurs donn??es permettent d'affiner ce premier r??sultat.""",
                },
                {
                    'Q': "Quelles sont les autres donn??es impactantes ?",
                    'R': """
                        <b>1.</b> La puissance de l'ampoule
                        Une ampoule de 20W poss??de un impact 3 fois plus faible qu'une ampoule de 60W.
                        <b>2.</b> L'orientation du luminaire
                        De nombreux luminaires sont orient??s vers une voie, se trouver ?? 1 m??tre devant le luminaire ou 1 m??tre derri??re est compl??tement diff??rent.
                        <b>3.</b> La temp??rature de couleur de l'ampoule
                        Une temp??rature de couleur basse (ou chaud) a un impact plus faible qu'une temp??rature haute (ou froide).
                        <b>4.</b> La d??tection de pr??sence
                        Nous consid??rons ??galement que les luminaires fonctionnant par d??tection poss??dent un impact faible, du fait de leur faible dur??e d'??clairage.
                        <b>5.</b> Le type de r??gime
                        Il est courant que les luminaires poss??dent deux plages de fonctionnement :
                        la premi??re pour la soir??e et le matin, la seconde pour la nuit.

                        Pour prendre en compte ce dernier param??tre, deux calques sont disponibles : <b>Jour</b> et <b>Nuit</b>.
                        Un luminaire dont le flux lumineux est r??duit de 50% pendant la nuit, voit son impact r??duit de 50% sur le calque Nuit.

                        Enfin, cette valeur d'impact est traduite sur une ??chelle de couleur allant du <span style="color: red;">rouge (niveau ??lev??)</span> au <span style="color: violet;">violet (niveau faible)</span>.""",
                },
                {
                    'Q': "A quoi sert le calque <i>Luminaires</i> ?",
                    'R': """
                        A la diff??rence de la <a href="/map_desc/2" target="_blank" class="invisible_link">carte de Contradiction</a> qui signale des zones, celle-ci ??claire les luminaires - un comble pour eux.
                        C'est-??-dire que chaque point correspond exactement ?? un luminaire.
                        Avec les calques Jour et Nuit, il ??tait possible d'identifier les positions des luminaires ?? fort impact.
                        Mais en rajoutant le calque <i>Luminaires</i>, Pollux va plus loin.
                        Car il permet ??galement ?? l'utilisateur d'acc??der aux caract??ristiques du luminaire sur lequel il clique.""",
                },
                {
                    'Q': "A quoi peut servir le calque <i>Arbres</i> ?",
                    'R': """
                    Le calque Arbre est un calque d'essai.
                    Il inverse le r??f??rentiel d'??tude : plut??t que de conna??tre l'impact g??n??r?? par les luminaires, il pr??sente l'impact re??u par les arbres.
                    Cela pr??sente deux avantages :
                    <li>Il permet de mieux appr??cier l'environnement proche des luminaires.</li>
                    <li>C'est ??galement un moyen de v??rifier la coh??rence des r??sultats : chaque luminaire a fort impact devrait avoir un ou plusieurs arbres ?? proximit??, et inversement !</li>"""
                },
            ]
        },
    }
