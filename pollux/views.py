from django.shortcuts import render
from maps import Configs
from json import load, loads
from json.decoder import JSONDecodeError
import os
from .works import BASE_DIR
from django.http import JsonResponse
from .models import lamps, trees, highways
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.gis.geos import Polygon
from .map_desc import DICT_DATA

CONFIGS = Configs()
CONFIGS.load()


def index(request):
    context = {'is_mainpage': True,
               'page_title': "Accueil",
               'maps_data': CONFIGS}
    return render(request, 'index.html', context=context)


@ensure_csrf_cookie
def show_map(request, map_id):
    # if map_id[0] == '-':  # map with invert intensity
    #    map_id = map_id[1:]
    if CONFIGS.get(map_id):
        context = {**CONFIGS[map_id]}
        if request.method == 'GET':
            if request.GET.get('zoom'):
                zoom = request.GET['zoom']
                if zoom.isdigit():
                    context['options']['zoom']['init'] = zoom
            if request.GET.get('layers'):
                layers = request.GET['layers'].split('/')
                for ind, layer in enumerate(context['layers']):
                    if str(ind) in layers:
                        layer['isActive'] = 1
                    else:
                        layer['isActive'] = 0
            if request.GET.get('bound'):
                bound = request.GET['bound'].split('/')
                if len(bound) == 4:
                    context['options']['bbox'] = bound

        return render(request, 'maps/map.html', context=context)
    return index(request)


db_name_to_cls = {
    'trees': trees.Trees,
    'lamps': lamps.Lamps,
    'highways': highways.Highways,
}
no_way_files = ()


@ensure_csrf_cookie
def print_json(request, filename):
    # if request.method != 'POST':
    #    return JsonResponse({'Error': f'ErrorMethod: {request.method}'})

    if filename in no_way_files:
        return JsonResponse({'Error': f'FileNotFoundError: {filename} not found'})

    if filename in db_name_to_cls:
        return print_db_to_json(request, filename)

    directory = 'db'
    try:
        with open(os.path.join(BASE_DIR.parent, directory, filename), 'r') as file:
            return JsonResponse(load(file))
    except FileNotFoundError:
        return JsonResponse({'Error':
                            f'FileNotFoundError: {filename} not found'})
    except JSONDecodeError:
        return JsonResponse({'Error':
                            f'JSONDecodeError: {filename} : format incorrect.'})


def print_db_to_json(request, filename):
    bbox = None
    for k in request.POST:
        bbox = loads(k).get('bbox')
        if bbox:
            break

    cls = db_name_to_cls[filename]
    if bbox:
        queryset = cls.objects.filter(position__within=Polygon.from_bbox(bbox))
    else:
        queryset = cls.objects.all()

    if filename != 'lamps':
        return JsonResponse(cls.serialize(queryset))

    # Python 3.8+ only
    # possibilité d'enlever des attributs pour alléger les données sortantes ?
    response = cls.serialize(queryset)
    for lamp, geo_lamp in zip(queryset, response['features']):
        geo_lamp['properties']['max_range_day'] = lamp.max_range(nb_lux=5, time='day')
        geo_lamp['properties']['max_range_night'] = lamp.max_range(nb_lux=5, time='night')
    return JsonResponse(response)


def mentions_legales(request):
    context = {'page_title': "Mentions légales",
               'maps_data': CONFIGS,
               'dict_data': DICT_DATA}
    return render(request,
                  'mentions_legales.html',
                  context=context)


def about(request):
    context = {
        'page_title': "A propos",
        'maps_data': CONFIGS
    }
    return render(request,
                  'about.html',
                  context=context)


def show_map_description(request, map_id):
    if not CONFIGS.get(map_id):
        return index(request)

    context = {'maps_data': CONFIGS,
               'map_data': CONFIGS[map_id]}
    return render(request,
                  'map_description.html',
                  context=context)
