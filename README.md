# Projet Pollux

Continuité du Projet Pollux dans le cadre du CivicLab de Grenoble, proposé par la Fabrique.coop.
Pour le défi *Lux, Led, Lumens* porté par GreenAlp.\
https://grenoble.civiclab.eu

Pollux est un outil de visualisation cartographique, pensé pour représenter l'éclairage public, son impact, ses manques en intégrant autant que possible son environnement réel.

La version actuelle n'est pas encore disponible.\
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
./manage.py uDB works/trees.py
./manage.py uDB works/lamps.py
./manage.py uDB works/highways.py
```

### Complétion des données :
```
./manage.py uCDB algo/complete_lamp_with_greenalpdata.py
./manage.py uCDB algo/set_orientation_to_lamps.py
./manage.py uCDB algo/lamp_impact_tree.py
```

### Démarrage de l'application :
```
./manage.py runserver
```

En local, par défaut, l'application sera visible sur l'url :\
http://127.0.0.1:8000/


### Pollux API :
Pollux utilise de nombreux jeux de données.\
Chaque jeu de données est représenté par un fichier présent dans *works/*.\
Les données récoltées sont présentes dans *db/*.\
Les différentes requêtes sont générées dans *api_ext/*.

Les requêtes passent l'endpoint **api/**.

```
https://green-pollux.herokuapp.com/api/nom_du_fichier
```
Par exemple :
https://green-pollux.herokuapp.com/api/trees_output.json


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


### Architecture:
- .env
- Pipfile
- Pipfile.lock
- algo/
- db/
- maps/
- pollux/
  - api_ext/
    - grenoble_alpes_metropole.py
    - osm.py
    - smmag.py
  - formats/
  - management/
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
  - views.py
  - works/
    - cross/
