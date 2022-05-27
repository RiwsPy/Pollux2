from . import *


class Config(Default_Config):
    ID = 2
    LAYER_BASE = Layer('', '', '',
                       Radius(unit='meter'),
                       Blur(fix=0),
                       MaxValue(method='fix', fix=6000),
                       Value(field='colour'),
                       gradient={
                            0.3333: '#FF880E',
                            0.4166: '#FF9F46',
                            0.5: '#FFB16D',
                            0.6666: '#FFCDA6',
                            0.8333: '#FFE4CD',
                            1.0: '#FFF6EC'}
                       )

    DATA = {
        'href': '/map/2',
        'options': Options(
            TileLayer('NIGHT'),
            Zoom(min=14, max=15, init=15),
            Legend(name='Température de couleur'),
            bbox=[5.703192, 45.179133, 5.735250, 45.189599],
        ),
        'layers': [
            Layer(
                'Vue réaliste',
                'heatmap',
                'lamps',
                IsActive(True),
                Orientation(field='orientation'),
                HorizontalAngle(field='horizontal_angle'),
                Radius(field='max_range_day')
            ),
        ],
        'description': {
            'title': 'Vue "satellitaire"',
            'icon': 'buttons/recommandation.png',
            'accroche': "Une carte interactive représentant l'éclairage au sol sur l'espace public.",
            'intro': """Cette carte permet de visualiser une simulation de vue satellitaire de l'éclairage public.""",
            'href': '/map_desc/2',
            'QR': [
                {
                    'Q': "Qu'entendez-vous par simulation de vue satellitaire ?",
                    'R': """
                        De nos jours, il est courant de pouvoir observer la Terre grâce aux images satellitaires, ces images sont d'ailleurs parfois utilisées pour estimer la pollution lumineuse.
                        Mais aucune donnée de ce type n'a servi à générer cette carte, cependant les données sont affichées de telle sorte afin de s'approcher de ce résultat.""",
                },
                {
                    'Q': "Pourquoi ne pas tout simplement montrer une vraie photo satellite ?",
                    'R': """
                        Les photos sont réalistes mais ont leurs propres limites. En effet un satellite ne peut montrer que ce qu'il reçoit.
                        Il est incapable de connaître la luminosité dans un métro souterrain pas plus que sous le dense feuillage d'une forêt.
                        Sans compter une caractéristique du sol appelé Albédo.
                        Selon le type de surface, le sol va réfléchir une quantité variable de lumière, altérant ainsi la perception du satellite.
                        C'est pourquoi il est très utile pour connaître la pollution lumineuse mais moins pour connaître l'éclairage réel au sol."""
                },
                {
                    'Q': "Comment en êtes-vous arrivé à ce résultat ?",
                    'R': """
                        Plusieurs informations sur les luminaires ont été nécessaires à sa réalisation :
                        <li>L'emplacement des luminaires ainsi que leur orientation permet de générer un demi-cercle orienté</li>
                        <li>Le rayon de ce demi-cercle est issu de leur hauteur et de l'angle d'incidence de l'ampoule</li>
                        <li>Leur température de couleur permet de colorer le tout</li>""",
                },
                {
                    'Q': "Plus besoin des satellites alors ?",
                    'R': """
                        Cette méthodologie possède également ses limites.
                        Elle ne prend pas en compte les obstacles à la lumière comme les bâtiments par exemple.
                        La puissance des luminaires n'intervient pas (encore) dans les résultats, c'est également un problème."""
                },
                {
                    'Q': 'Quels sont les avantages de cette méthode ?',
                    'R': """
                        Outre le fait de ne pas être affecté par les nuages, elles utilise des données mises à jour plusieurs fois par mois, ce qui permet d'avoir une carte régulièrement à jour.
                        A titre d'exemple, les images satellites disponibles au grand public sont mises à jour à peine une fois par an.
                        Les contraintes technologiques sont aussi bien moindres :
                        un ordinateur de bureau est plus accessible qu'un satellite."""
                }
            ]
        }
    }
