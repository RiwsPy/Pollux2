# Projet Pollux

Continuité du Projet Pollux dans le cadre du CivicLab de Grenoble, proposé par la Fabrique.coop.
Pour le défi *Lux, Led, Lumens* porté par GreenAlp.\
https://grenoble.civiclab.eu

Pollux est un outil de caractérisation et de visualisation cartographique de l'espace public. \
Initialement pensé pour représenter l'éclairage public, il s'avère que pour répondre correctement à cette problématique, une perception accrue de l'espace public soit nécessaire. \
Et une fois, cette perception acquise, elle est utile pour tous les éléments constituant cet espace public : l'éclairage, la biodiversité, le stationnenement, le logement....

Deux piliers constituent la base de Pollux :
* le fond : récupérer, mettre à jour, stocker des données, les croiser, les décupler, les fiabiliser, avec une approche rigoureusement scientifique
* la forme : représenter ces informations sur des cartes interactives, en mettant en avant leur accessibilité, à des fins de sensibilisation et de compréhension


La version actuelle est actuellement disponible : http://164.92.163.211/  \
La version du prototype du projet est visible sur : https://green-pollux.herokuapp.com \
Son repo : https://github.com/RiwsPy/Pollux

### Prérequis:
* Python3
* pipenv
* PostgreSQL avec l'extension PostGIS


### Téléchargement :
```
git clone https://github.com/RiwsPy/Pollux2.git
```

### Installation :
```
cd Pollux2/
pipenv install
pipenv shell
```

### Première utilisation :
Après avoir rempli le fichier **.env** à la racine projet et configuré votre base de données :
```
./manage.py makemigrations
./manage.py migrate
```

### Création et mise à jour des bases de données :
```
./manage.py uDB pollux/works/trees.py
./manage.py uDB pollux/works/lamps.py
./manage.py uDB pollux/works/highways.py
./manage.py uDB pollux/works/crossings.py
```

### Complétion des données :
```
./manage.py uCDB pollux/algo/complete_lamp_with_greenalpdata.py
./manage.py uCDB pollux/algo/set_orientation_to_lamps.py
./manage.py uCDB pollux/algo/lamp_impact_tree.py
./manage.py uCDB pollux/algo/set_lux_on_crossings.py
```

### Démarrage de l'application :
```
./manage.py runserver
```

En local, par défaut, l'application sera visible sur l'url :\
http://127.0.0.1:8000/


### Les mises à jour automatique des données :
Il est possible de mettre à jour la base de données, grâce à la commande -uDB.
Pour une base, par exemple :
```
./engine.py -uDB pollux/works/trees.py
```
Ou plusieurs bases :
```
./engine.py -uDB pollux/works/parks.py pollux/works/shops.py
```


### Architecture:
- manage.py
- .env
- Pipfile
- Pipfile.lock
- pollux/
  - algo/
  - api_ext/
    - grenoble_alpes_metropole.py
    - osm.py
    - smmag.py
  - db/
  - formats/
  - management/
  - maps/
  - models/
  - static/
      - css/
      - fonts/
      - img/
      - js/
  - templates/
      - index.html
      - map.html
      - ...
  - tests/
  - views.py
  - works/
    - cross/
