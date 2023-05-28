from django.db.models import Q
from django.views.generic import ListView, DetailView

from nitmap.models import Client, Equipment, Instance


# Create your views here.


class ClientDetailView(DetailView):
    model = Client
    template_name = 'inforium/client_detail.html'
    context_object_name = 'client'
    pk_url_kwarg = 'client_id'


class ClientListView(ListView):
    model = Client
    template_name = 'inforium/client_list.html'
    context_object_name = 'clients'
    paginate_by = 10  # Show 10 clients per page

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(full_name__icontains=search_query) |
                Q(phone__icontains=search_query)
            )
        return queryset

class EquipmentListView(ListView):
    model = Equipment
    template_name = 'inforium/equipment_list.html'
    context_object_name = 'equipments'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(client=self.kwargs['client_id'])
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(inv_number__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client'] = Client.objects.get(pk=self.kwargs['client_id'])
        return context


class InstanceListView(ListView):
    model = Instance
    template_name = 'inforium/instance_list.html'
    context_object_name = 'instances'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(client=self.kwargs['client_id'])
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(lan__icontains=search_query) |
                Q(speed__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client'] = Client.objects.get(pk=self.kwargs['client_id'])
        return context