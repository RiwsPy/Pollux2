from django.contrib import admin
from django.http import JsonResponse

from .models.trees import Trees
from .models.lamps import Lamps
from .models.highways import Highways
from .models.crossings import Crossings
from .models.parking_public import Parking_public
from .algo.lamp_impact_tree import Cross as Cross_lamp_impact_tree
from .algo.tree_impacted_by_lamp import Cross as Cross_tree_impact_lamp
from .algo.set_orientation_to_lamps import Cross as Cross_orientation_lamps


@admin.register(Trees)
class TreesAdmin(admin.ModelAdmin):
    search_fields = ['code', 'taxon']
    readonly_fields = ['day_impact', 'night_impact']
    list_display = ('code', 'taxon', 'planted_date', 'height', 'day_impact', 'night_impact')
    actions = ['update_tree_impact']

    @admin.action(description='MaJ Impact jour et nuit')
    def update_tree_impact(self, request, queryset):
        Cross_tree_impact_lamp().run(queryset)


@admin.register(Lamps)
class LampsAdmin(admin.ModelAdmin):
    readonly_fields = ['day_impact', 'night_impact', 'nearest_way_dist']
    list_display = ('code', 'power', 'lumens', 'colour', 'height', 'irc', 'orientation_int', 'lowering_night',
                    'day_impact', 'night_impact')
    search_fields = ['code']
    actions = ['update_orientation', 'update_tree_impact', 'export_json']
    list_per_page = 1000

    @admin.display(description='Orientation (°)')
    def orientation_int(self, obj):
        return round(obj.orientation)

    @admin.display(description='Lumens')
    def lumens(self, obj):
        return obj.power * obj.lumens_per_watt

    @admin.action(description='MaJ Impact jour et nuit')
    def update_tree_impact(self, request, queryset):
        Cross_lamp_impact_tree().run(queryset)

    @admin.action(description='MaJ Orientation')
    def update_orientation(self, request, queryset):
        Cross_orientation_lamps().run(queryset)

    @admin.action(description='Export données JSON')
    def export_json(self, request, queryset):
        itm = queryset.first()
        if itm:
            json_data = itm.__class__.serialize(queryset)
            return JsonResponse(json_data)


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
