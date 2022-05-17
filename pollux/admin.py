from django.contrib import admin
from .models.trees import Trees
from .models.lamps import Lamps
from .models.highways import Highways


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
