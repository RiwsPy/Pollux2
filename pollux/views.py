from django.shortcuts import render
import json
import os
from json.decoder import JSONDecodeError
from .maps import Configs
from .works import BASE_DIR
from .models import lamps, trees, highways
from .map_desc import ORIGIN_DATA
from .formats.geojson import Geojson
from .utils import in_bound
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.gis.geos import Polygon
from django.views import View
from django.views.generic.base import ContextMixin
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse

CONFIGS = Configs()
CONFIGS.load()


class ShowMap(View):
    template_name = 'maps/map.html'

    def get(self, request, map_id):
        if not CONFIGS.get(map_id):
            return HttpResponseRedirect(reverse('home'))

        context = CONFIGS[map_id]
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

        return render(request,
                      self.template_name,
                      context=context)


class JsonDetails(View):
    db_name_to_cls = {
        'trees': trees.Trees,
        'lamps': lamps.Lamps,
        'highways': highways.Highways,
    }
    db_dir = {'db', 'db/cross'}
    no_way_files = ()

    def get(self, request, filename):
        if filename not in self.no_way_files:
            try:
                return self.print_db_to_json(self.db_name_to_cls[filename], **request.GET)
            except KeyError:
                return self.print_file_to_json(filename, **request.GET)

        return HttpResponseForbidden()

    def print_file_to_json(self, filename, **kwargs):
        # TODO: ajouter un équivalent au filter(position__within) ??
        error_msg = 'db_dir: empty'
        for directory in self.db_dir:
            try:
                with open(os.path.join(BASE_DIR, 'pollux', directory, filename), 'r') as file:
                    if kwargs.get('bound'):
                        kwargs['bound'] = kwargs['bound'][0].split(',')
                        kwargs['bound'] = [float(pos) for pos in kwargs['bound']]
                        kwargs['bound'] = [kwargs['bound'][1],
                                           kwargs['bound'][0],
                                           kwargs['bound'][3],
                                           kwargs['bound'][2]]
                    geo = Geojson()
                    geo.load(json.load(file), in_bound, **kwargs)
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

    @staticmethod
    def print_db_to_json(cls, **kwargs):
        if 'bound' in kwargs:
            bound = kwargs['bound'][0].split(',')
            try:
                queryset = cls.objects.filter(position__within=Polygon.from_bbox(bound))
            except ValueError:
                # nombre d'argument erroné (!= 4)
                queryset = cls.objects.all()
        else:
            queryset = cls.objects.all()

        if cls is not lamps.Lamps:
            return JsonResponse(cls.serialize(queryset))

        # Python 3.8+ only
        # TODO: Spécifité à indiquer dans request et non par défaut
        # TODO: possibilité d'enlever des attributs pour alléger les données sortantes ?
        response = cls.serialize(queryset)

        for lamp, geo_lamp in zip(queryset, response['features']):
            geo_lamp['properties']['max_range_day'] = lamp.max_range(nb_lux=5, time='day')
            geo_lamp['properties']['max_range_night'] = lamp.max_range(nb_lux=5, time='night')
            geo_lamp['properties']['expense'] = lamp.expense

        return JsonResponse(response)


class MixinContext(ContextMixin):
    def get_context_data(self, **kwargs):
        return super().get_context_data(**self.extra_content, **kwargs)


class MixinSecondaryPages(MixinContext, View):
    template_name = ""
    extra_content = {
        'page_title': 'Pollux',
        'maps_data': CONFIGS}

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
