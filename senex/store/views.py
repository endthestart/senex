from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from .models import Category, Product


def store_home(request, template_name="store_home.html"):
    context = {}
    categories = Category.objects.filter(parent=None)
    context.update({'child_categories': categories})
    return render_to_response(template_name, context, RequestContext(request))


def category(request, path=None, template_name="category.html"):
    category = get_object_or_404(Category, path=path)
    context = {}
    context.update({'category': category})
    child_categories = Category.objects.filter(parent=category)
    context.update({'child_categories': child_categories})
    products = Product.objects.filter(category=category)
    context.update({'products': products})

    return render_to_response(template_name, context, RequestContext(request))


def product_detail(request, path=None, slug=None, template_name="product.html"):
    product = get_object_or_404(Product, slug=slug)
    context = {"product": product}
    return render_to_response(template_name, context, RequestContext(request))
