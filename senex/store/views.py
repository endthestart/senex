from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from .models import Category, Product


def mountain(request, template_name="mountain_index.html"):

    return render_to_response(template_name, {}, RequestContext(request))


def mountain_bikes(request, template_name="mountain_bikes.html"):
    category = Category.objects.get(name='Mountain Bike')
    products = Product.objects.filter(category=category)
    return render_to_response(template_name, {"products":products,}, RequestContext(request))


def mountain_bike_model(request, template_name="mountain_bike_model.html", slug=None):
    category = Category.objects.get(name='Mountain Bike')
    products = Product.objects.get(slug=slug)
    return render_to_response(template_name, {"p": products, }, RequestContext(request))


def mountain_frames(request, template_name="mountain_frames.html"):
    return render_to_response(template_name, {}, RequestContext(request))


def road(request, template_name="road_index.html"):
    return render_to_response(template_name, {}, RequestContext(request))
