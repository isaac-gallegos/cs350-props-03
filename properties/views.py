# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from geopy.distance import distance
from geopy.geocoders import Nominatim

from .models import Property
from .forms import LookupForm
from .forms import DistanceForm

# Show the all the properties in the db.

class PropertyListView(generic.ListView):
    model = Property
    template_name = "properties/list.html"


class PropertyDetailView(generic.DetailView):
    model = Property
    template_name = "properties/detail.html"


class PropertyCreateView(generic.CreateView):
    model = Property  # what type of object we are creating?
    template_name = "properties/create.html"  # the page to display the form.
    fields = ['prop_type', 'address', 'zip_code', 'description', 'picture_url', 'price',]
    success_url = reverse_lazy('properties:list')


class PropertyUpdateView(generic.UpdateView):
    model = Property  # what type of object we are editing?
    template_name = "properties/edit.html"  # the page to display the form.
    fields = ['prop_type', 'address', 'zip_code', 'description', 'picture_url', 'price',]
    success_url = reverse_lazy('properties:list')

class PropertyLookupView(generic.FormView):
    template_name = 'properties/lookup.html'
    form_class = LookupForm
    success_url = reverse_lazy('properties:lookup')

    def get_context_data(self, **kwargs):
        context = super(PropertyLookupView, self).get_context_data(**kwargs) 
        try:
            result = []
            q = self.request.GET['search']
            properties = Property.objects.all()
            for i in properties:
                if q in i.prop_type:
                    result.append(i)

            context['result'] = result

        except Exception as e:
            print e
            pass
        
        return context


class PropertyDistanceView(generic.FormView):
    model = Property
    form_class = LookupForm
    template_name = "properties/distance.html"

    def get_context_data(self, **kwargs):
        context = super(PropertyDistanceView, self).get_context_data(**kwargs)
        try:
            result = []
            q = self.request.GET['address']
            distance = self.request.GET['distance']
            geolocator = Nominatim()
            loc = geolocator.geocode(q)


            if not loc:
                context['result'] = 'Cannot find that location'
            else:
                for i in Property.object.all:
                    loc2 = geolocator.geocode(i.address)
                    d = distance((loc.latitude, loc.longitude), (loc2.latitude, loc2.longitude)).miles
                    if d < distance:
                        result.append(i)
                        
                print (results)
                context['result'] = result
        except Exception as e:
            print e
            pass

        return context