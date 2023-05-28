from django.contrib import admin
from django.db import models
from .models import Points, Lines, Client, Equipment, Speed, Instance, ClientGroups, Streets

from leaflet.admin import LeafletGeoAdmin
from dal import autocomplete
from django import forms


SETTINGS_OVERRIDES = {
    'TILES': [('', 'http://localhost:8080/styles/basic-preview/{z}/{x}/{y}.png', '')],
    'DEFAULT_CENTER': (54.872, 69.139),
    'DEFAULT_ZOOM': 12,
    'MIN_ZOOM': 12,
    'MAX_ZOOM': 17,


}


class InstanceForm(forms.ModelForm):
    model = Instance
    fields = ('__all__')
    class Meta:
        widgets = {

            'point': autocomplete.ModelSelect2(url='nitmap:point-autocomplete')
        }


@admin.register(Points)
class PointsAdmin(LeafletGeoAdmin):
    list_display = ('street', 'number', 'with_circle')
    settings_overrides = SETTINGS_OVERRIDES
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'size': '10'})}
    }
    map_height = '75vh'
    map_width = '100%'
    # form = PointForm
    autocomplete_fields = ['street']
    search_fields = ['number', 'street']
    list_editable = ('with_circle',)


@admin.register(Lines)
class LinesAdmin(LeafletGeoAdmin):
    list_display = ('name',)
    settings_overrides = SETTINGS_OVERRIDES
    map_height = '75vh'
    map_width = '100%'


@admin.register(ClientGroups)
class ClientGroupsAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Streets)
class StreetsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'full_name', 'phone')
    search_fields = ['name', 'full_name']


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'inv_number')


@admin.register(Speed)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Instance)
class InstanceAdmin(admin.ModelAdmin):
    list_display = ('is_my', 'is_active', 'client', 'point')
    list_filter = ('is_my', 'is_active', 'client', 'point')
    search_fields = ('client__name', 'point__name')
    list_editable = ('is_my', 'is_active', )
    list_display_links = ('client', 'point')
    radio_fields = {'port_type': admin.VERTICAL, 'service_type': admin.VERTICAL}
    form = InstanceForm
    autocomplete_fields = ['client', 'point']
