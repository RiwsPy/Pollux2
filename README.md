# Projet Pollux

Projet Pollux dans le cadre du CivicLab de Grenoble, proposé par la Fabrique.coop.
Pour le défi *Lux, Led, Lumens* porté par GreenAlp.
https://grenoble.civiclab.eu


Le prototype du projet est visible sur : https://green-pollux.herokuapp.com


### Prérequis:
* Python3
* pipenv


### Téléchargement :
```
git clone https://github.com/RiwsPy/Pollux.git
```

### Installation :
```
cd Pollux/
pipenv install
pipenv shell
```

### Démarrage de l'application :
```
./engine.py
```

En local, par défaut, l'application sera visible sur l'url :\
http://127.0.0.1:5000/


### Flask
Le framework utilisé est Flask, il a été choisi pour sa simplicité mais aussi parce qu'il est utilisable par plusieurs membres de l'équipe.\
Un passage sous Django est envisageable si le projet venait à prendre de l'ampleur.

### Clips
Le module Clips génère les recommandations d'usage pour la carte des Recommandations.\
Son contenu n'est actuellement pas disponible.

### Pollux API :
Pollux utilise de nombreux jeux de données.\
Chaque jeu de données est représenté par un fichier présent dans *works/*.\
Les données récoltées sont présentes dans *db/*.\
Les différentes requêtes sont générées dans *api_ext/*.

**Jeux de données**
Fichier works | Contenu | Origine des données | Mise à jour automatique | Détails
 --- | --- | ---  | --- | ---
accidents | Accidents de voiture 2019-2020 | https://www.data.gouv.fr/fr/ | Non | Le format csv a évolué en 2019
birds | Observations d'oiseaux 2012-2021 | https://openobs.mnhn.fr/ | Non | Récupération contraignante
crossings | Passages piétons | https://overpass-turbo.eu/ (OpenStreetMap) | Oui | /
highways | Artères principales de Grenoble | / | Non | Retranscription manuelle
lamps | Emplacement des luminaires | https://data.metropolegrenoble.fr | Non | Données pas encore disponibles
parks | Parcs | https://overpass-turbo.eu/ (OpenStreetMap) | Oui | /
shops | Bâtiments dont les horaires d'ouverture sont connues | https://overpass-turbo.eu/ (OpenStreetMap) | Oui | /
tc_stops | Arrêts de bus | https://data.metropolegrenoble.fr/ | Oui | /
tc_ways | Voies de bus | https://data.metropolegrenoble.fr/ | Oui | /
trees | Arbres | https://data.metropolegrenoble.fr/ | Oui | /


Ces données étant sous licence ouverte, il nous a paru évident de redistribuer ces informations ainsi que celles générées par Pollux.
Les requêtes passent l'endpoint **api/**.

```
https://green-pollux.herokuapp.com/api/nom_du_fichier
```
Par exemple :
https://green-pollux.herokuapp.com/api/crossings_output.json

3 types de données sont présents :
* Les données originelles, par exemple *parks.json*, *tc_stops.json*
* Les données filtrées par Pollux, elles commencent par le même nom que le fichier originel et se termine par *_output* : *parks_output.json*, *tc_stops_output.json*
* Les données créées ou enrichies par Pollux : *conflict_lamps__trees_birds.json* (qui est la base utilisée par la carte Impact : conflits entre les luminaires d'une part et les arbres et oiseaux d'autres part).

### Conversion en Geojson
L'extension des fichiers récupérés est variable. Pollux les convertis par défaut en Geojson.\
Les méthodes de conversion sont présentes dans *formats/*.

### Les mises à jour automatique des données :
Il est possible de mettre à jour la base de données, grâce à la commande -uDB.
Pour une base, par exemple :
```
./engine.py -uDB works/trees.py
```
Ou plusieurs bases :
```
./engine.py -uDB works/parks.py works/shops.py
```

De la même façon il est possible de mettre à jour la base de données croisée grâce à -uCDB.
Pour une base, par exemple :
```
./engine.py -uCDB works/cross/proximity.py
```
Il est possible d'y associer l'attribut *-mr* pour *--maxRange* afin de choisir le rayon de recherche de l'algorithme :
```
./engine.py -uCDB works/cross/proximity.py -mr 500
```
Un croisement de données volumineux doublé d'un *-mr* élevé peut demander une grande quantité de temps.


### Tests :
Les tests sont réalisés grâce à la librairie **pytest**.\
Actuellement, seule la partie python est testée unitairement, sa couverture est d'environ 90%.

```
pytest
```
ou encore
```
coverage run -m pytest
```

### Architecture:
- .env
- Pipfile
- Pipfile.lock
- Procfile
- api_ext/
    - clips.py
    - grenoble_alpes_metropole.py
    - osm.py
    - smmag.py
- db/
  - cross/
- formats/
- maps/
- website/
    - static/
        - css/
        - fonts/
        - img/
        - js/
    - templates/
        - index.html
        - map.html
        - ...
    - views.py
- works/
    - cross/
    - accidents.py
    - birds.py
    - ...

