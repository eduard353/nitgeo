from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404
from django.views import View
from geojson import Feature, FeatureCollection, Point, dumps
from django.views.generic import TemplateView, DetailView
from django.core.serializers import serialize
from django.http import HttpResponse
from django.shortcuts import render
from .models import Points, Lines, Instance, Client, Equipment, Streets
from dal import autocomplete
from django.db.models import Q


class PointAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        if not self.request.user.is_authenticated:
            return Client.objects.none()
        qs = Points.objects.all()
        if self.q:
            qs = qs.filter(Q(street__name__icontains=self.q) | Q(number__icontains=self.q))
        return qs



class MapView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'


class PointsDatasetView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        result = []
        points = Points.objects.all()

        for point in points:
            props = {'point': '', 'info': []}
            connects = Instance.objects.filter(point=point.id).values()

            my_point = Point(point.points)
            props['point'] = str(point)

            for connect in connects:
                client = Client.objects.get(id=connect['client_id'])
                client_id = client.id
                client_name = str(client)

                props['info'].append(
                    [client_name + '<br>' + connect['lan'] + '/' + str(connect['lan_mask']) + '\n', client_id, connect['id']])

            my_feature = Feature(geometry=my_point, properties=props)
            result.append(my_feature)

        return HttpResponse(dumps(FeatureCollection(result)), content_type='json')


class BspdCircleView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        polygons = serialize('geojson', Points.objects.filter(with_circle=True))
        return HttpResponse(polygons, content_type='json')


class LinesDatasetView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        lines = serialize('geojson', Lines.objects.all())
        return HttpResponse(lines, content_type='json')
