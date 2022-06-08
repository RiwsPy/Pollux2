from django.contrib import admin
from .models.trees import Trees
from .models.lamps import Lamps
from .models.highways import Highways
from .models.crossings import Crossings
from .models.parking_public import Parking_public


@admin.register(Trees)
class TreesAdmin(admin.ModelAdmin):
    search_fields = ['code', 'day_impact', 'night_impact']
    readonly_fields = ['code', 'day_impact', 'night_impact']


@admin.register(Lamps)
class LampsAdmin(admin.ModelAdmin):
    search_fields = ['code', 'irc', 'colour', 'day_impact', 'night_impact']
    readonly_fields = ['code', 'day_impact', 'night_impact', 'nearest_way_dist']
    list_display = ('code', 'power', 'irc', 'colour', 'height')


@admin.register(Highways)
class HighwaysAdmin(admin.ModelAdmin):
    search_fields = ['name', 'type']
    readonly_fields = ['name']
    list_display = ('name', 'parking_r', 'parking_l')


@admin.register(Crossings)
class CrossingsAdmin(admin.ModelAdmin):
    pass


@admin.register(Parking_public)
class ParkingsAdmin(admin.ModelAdmin):
    list_display = ('code', 'parking_type', 'fee')
