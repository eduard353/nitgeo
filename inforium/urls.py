from django.urls import path

from inforium import views

app_name = 'inforium'

urlpatterns = [


    path("<int:client_id>/instances/", views.InstanceListView.as_view(), name='client_instance_list'),
    path("<int:client_id>/equipments/", views.EquipmentListView.as_view(), name='client_equipment_list'),
    path("<int:client_id>/", views.ClientDetailView.as_view(), name='client_detail'),
    path("", views.ClientListView.as_view(), name='clients_list'),


]