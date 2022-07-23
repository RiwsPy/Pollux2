from django.shortcuts import render
import json
import os
from json.decoder import JSONDecodeError

import bank.models
from .maps import Configs
from .works import BASE_DIR
from .models import lamps, trees, highways, crossings, parking_public
from bank.models import LampsMairin00, LampsCoccia00
from .map_desc import ORIGIN_DATA
from .formats.geojson import Geojson
from .utils import in_bound
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.gis.geos import Polygon
from django.core.exceptions import FieldError
from django.views import View
from django.views.generic import DetailView
from django.views.generic.base import ContextMixin
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q, F
from django.contrib.gis.measure import D
from copy import deepcopy

_CONFIGS = Configs()
_CONFIGS.load()
CONFIGS = deepcopy(_CONFIGS)


class ShowMap(View):
    template_name = 'maps/map.html'

    def get(self, request, map_id):
        if not CONFIGS.get(map_id):
            return HttpResponseRedirect(reverse('home'))

        context = deepcopy(_CONFIGS[map_id])
        template_name = self.template_name
        if map_id == 'mapbox':
            template_name = 'maps/map_box.html'
            context['mapbox_access_token'] = os.getenv('MAPBOX_ACCESS_TOKEN')

        context['ID'] = map_id
        context['options']['ID'] = map_id
        kwargs = request.GET

        zoom = kwargs.get('zoom')
        if zoom and zoom.isdigit():
            context['options']['zoom']['init'] = zoom

        layers = kwargs.get('layers', '').split('/')
        if layers != ['']:
            for ind, layer in enumerate(context['layers']):
                layer['isActive'] = int(str(ind) in layers)

        bound = kwargs.get('bound', '').split('/')
        if bound and len(bound) == 4:
            context['options']['bbox'] = bound

        # update des filters des calques en fonction des filters présents dans l'url
        filters = kwargs.get('filters', '').split(',')
        for fltr in filters:
            k, _, v = fltr.partition(':')
            if k and v:
                for layer in context['layers']:
                    layer['filters'][k] = v

        # Q n'est pas transmit car incompatible avec le type str
        for layer in context['layers']:
            try:
                del layer['Q']
            except KeyError:
                pass

        return render(request,
                      template_name,
                      context=context)


class DataDetails(View):
    # TODO: meilleur moyen d'automatiser (ou d'isoler) cette méthode ?
    db_name_to_cls = {
        'trees': trees.Trees,
        'lamps': lamps.Lamps,
        'highways': highways.Highways,
        'crossings': crossings.Crossings,
        'parking_public': parking_public.Parking_public,
        'lamps_coccia00': LampsCoccia00,
        'lamps_mairin00': LampsMairin00,
    }
    db_dirs = {'db', 'db/cross'}
    no_way_files = ()

    def get(self, request, filename):
        if filename not in self.no_way_files:
            try:
                return self.print_db_to_json(self.db_name_to_cls[filename], **request.GET)
            except KeyError:
                return self.print_file_to_json(filename, **request.GET)

        return HttpResponseForbidden()

    def print_file_to_json(self, filename, **kwargs):
        error_msg = 'db_dirs: empty'
        for directory in self.db_dirs:
            try:
                with open(os.path.join(BASE_DIR, 'pollux', directory, filename), 'r') as file:
                    geo = Geojson()
                    if 'filters' in kwargs:
                        filters = json.loads(kwargs['filters'][0])
                        filters = [float(pos) for pos in filters['position__within']]
                        filters = [filters[1],
                                   filters[0],
                                   filters[3],
                                   filters[2]]
                        kwargs['filters'] = filters
                        geo.load(json.load(file), in_bound, **kwargs)
                    else:
                        geo.load(json.load(file))
                    return JsonResponse(geo)
            except FileNotFoundError:
                error_msg = f'FileNotFoundError: {filename} not found'
                continue
            except JSONDecodeError:
                error_msg = f'JSONDecodeError: {filename} : format incorrect.'
                break
            except:
                error_msg = f'{filename} : erreur inconnue.'
                break

        return JsonResponse({'Error': error_msg})

    def print_db_to_json(self, cls, **kwargs):
        queryset = cls.objects.all()

        filters_updated = dict()
        if kwargs['layer_id'][0] != '-1' and kwargs['map_id'][0] != '-1':
            map_id = kwargs['map_id'][0]
            layer_id = int(kwargs['layer_id'][0])

            filters_updated.update(CONFIGS[map_id]['layers'][layer_id].get('filters', {}))
            if 'Q' in CONFIGS[map_id]['layers'][layer_id]:
                queryset = queryset.filter(CONFIGS[map_id]['layers'][layer_id]['Q'])
        if 'filters' in kwargs:
            filters_updated.update(json.loads(kwargs['filters'][0]))

        for k, v in filters_updated.items():
            if '.' in k:
                # filters=trees.heigth__lge:5
                db, _, k = k.partition('.')
                if self.db_name_to_cls.get(db) is not cls:
                    continue
            try:
                do_filter = True
                if k == 'position__within':
                    v = Polygon.from_bbox(v)
                # provisoire
                elif k == 'position__dwithin' and filters_updated.get('position__within'):
                    cls_from_elt = self.db_name_to_cls.get(v)
                    bbox = Polygon.from_bbox(filters_updated['position__within'])
                    elts = cls_from_elt.objects.filter(position__within=bbox)
                    fat_Q = Q(pk=-1)
                    for elt in elts:
                        fat_Q |= Q(position__distance_lte=(elt.position, D(m=20)))
                    queryset = queryset.filter(fat_Q)
                    do_filter = False

                if do_filter:
                    queryset = queryset.filter(**{k: v})
                    print(f'Filtre {k}: {v} appliqué.')
            except FieldError:
                print(f'Warning: Filtre {k}: {v} non appliqué.')
                continue
            except ValueError:
                print(f'ValueError {k}: {v} ; position incorrecte ?')
                continue

        response = cls.serialize(queryset)
        if cls is not lamps.Lamps and cls.Meta.app_label != 'bank':
            return JsonResponse(response)

        # Python 3.8+ only
        # TODO: Spécifité à indiquer dans request et non par défaut
        # TODO: possibilité d'enlever des attributs pour alléger les données sortantes ?
        for lamp, geo_lamp in zip(queryset, response['features']):
            geo_lamp['properties']['max_range_day'] = lamp.max_range(nb_lux=3, time='day')
            geo_lamp['properties']['max_range_night'] = lamp.max_range(nb_lux=3, time='night')
            colour_impact = (60 + 20 * max(0, min(4000, lamp.colour - 2000)) / 4000) / 80
            geo_lamp['properties']['impact_tree_on_ground'] = (lamp.lux_with_distance(lamp.height, 'day') +
                                                               lamp.lux_with_distance(lamp.height, 'night')) / 2 * \
                                                            colour_impact
            geo_lamp['properties']['expense'] = lamp.expense

        return JsonResponse(response)


class MixinContext(ContextMixin):
    def get_context_data(self, **kwargs):
        return super().get_context_data(**self.extra_content, **kwargs)


class MixinSecondaryPages(MixinContext, View):
    template_name = ""
    extra_content = {"page_title": "Pollux", "maps_data": _CONFIGS}

    def get(self, request, *args, **kwargs):
        return render(request,
                      self.template_name,
                      context=self.get_context_data())


class Index(MixinSecondaryPages):
    template_name = 'index.html'
    page_title = 'Accueil'

    @property
    def extra_content(self) -> dict:
        return {**super().extra_content, **{'is_mainpage': True}}


class MentionsLegales(MixinSecondaryPages):
    template_name = "mentions_legales.html"
    page_title = "Mentions légales"


class About(MixinSecondaryPages):
    template_name = "about.html"
    page_title = "A propos"

    @property
    def extra_content(self) -> dict:
        return {**super().extra_content, **{'origin_data': ORIGIN_DATA}}


class ShowMapDescription(MixinSecondaryPages):
    template_name = "map_description.html"
    map_id = None

    def get(self, request, map_id, *args, **kwargs):
        if not CONFIGS.get(map_id):
            return HttpResponseRedirect(reverse('home'))
        self.map_id = map_id

        return super().get(request, *args, **kwargs)

    @property
    def extra_content(self) -> dict:
        return {**super().extra_content, **{'map_data': CONFIGS[self.map_id]}}

