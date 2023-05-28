
from django.urls import path

from .views import LinesDatasetView, MapView, BspdCircleView, PointAutocomplete, PointsDatasetView

app_name = 'nitmap'

urlpatterns = [

    path("points/", PointsDatasetView.as_view(), name='points'),
    path('point-autocomplete/$', PointAutocomplete.as_view(), name='point-autocomplete'),
    path("circle/", BspdCircleView.as_view(), name='circle'),
    path("lines/", LinesDatasetView.as_view(), name='lines'),
    path("", MapView.as_view(), name='home'),

]
