from json import load
from json.decoder import JSONDecodeError
import os
from pathlib import Path
from . import app, CONFIGS
from flask import render_template, jsonify, request
from api_ext.clips import Clips
from api_ext import BadStatusError
from .map_desc import DICT_DATA

BASE_DIR = Path(__file__).resolve().parent.parent


@app.route('/')
def index():
    return render_template('index.html',
                           is_mainpage=True,
                           page_title="Accueil",
                           maps_data=CONFIGS)


@app.route('/map/<map_id>')
def show_map(map_id):
    if map_id[0] == '-':  # map with invert intensity
        map_id = map_id[1:]

    if CONFIGS.get(map_id):
        return render_template(**CONFIGS[map_id])
    return index()


@app.route('/api/<filename>', methods=['GET'])
def print_json(filename, directory='db/'):
    no_way_files = ()
    if filename in no_way_files:
        return jsonify({'Error': f'FileNotFoundError: {filename} not found'})

    try:
        with open(os.path.join(BASE_DIR, directory + filename), 'r') as file:
            return jsonify(load(file))
    except FileNotFoundError:
        return jsonify({'Error':
                        f'FileNotFoundError: {filename} not found'})
    except JSONDecodeError:
        return jsonify({'Error':
                        f'JSONDecodeError: {filename} : format incorrect.'})


@app.route('/api/<directory>/<filename>', methods=['GET'])
def print_cross_json(directory, filename):
    return print_json(filename, directory='db/' + directory + '/')


@app.route('/clips/', methods=['POST'])
def clips_recommendation():
    cl = Clips()
    try:
        req = cl.call(url="", data=request.data)
    except BadStatusError:
        return jsonify({"recommendation": "Erreur"})

    return jsonify(req)


@app.route('/mentions_legales/', methods=['GET'])
def mentions_legales():
    return render_template('mentions_legales.html',
                           page_title="Mentions légales",
                           maps_data=CONFIGS,
                           dict_data=DICT_DATA)


@app.route('/about/', methods=['GET'])
def about():
    return render_template('about.html',
                           page_title="A propos",
                           maps_data=CONFIGS)


@app.route('/encyclopedia/', methods=['GET'])
def encyclopedia():
    return render_template('encyclopedia.html',
                           page_title="Encyclopédie",
                           maps_data=CONFIGS)


@app.route('/map_desc/<map_id>', methods=['GET'])
def show_map_description(map_id):
    if not CONFIGS.get(map_id):
        return index()

    return render_template('map_description.html',
                           maps_data=CONFIGS,
                           map_data=CONFIGS[map_id])
