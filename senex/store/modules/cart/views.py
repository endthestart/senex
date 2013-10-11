from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from store.models import Product


def add(request, id=0, redirect_to='cart'):
    form_data = request.POST.copy()
    product_slug = None

    if form_data.has_key('productname'):
        product_slug = form_data['product_name']