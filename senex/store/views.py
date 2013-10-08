from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from .models import Category, Product, OptionGroup


def store_home(request, template_name="store_home.html"):
    categories = Category.objects.filter(parent=None)
    context = {
        'child_categories': categories
    }
    return render_to_response(template_name, context, RequestContext(request))


def category(request, path=None, template_name="category.html"):
    category = get_object_or_404(Category, path=path)
    child_categories = Category.objects.filter(parent=category)
    products = Product.objects.filter(category=category)
    context = {
        'category': category,
        'child_categories': child_categories,
        'products': products
    }

    return render_to_response(template_name, context, RequestContext(request))


def product_detail(request, path=None, slug=None, template_name="product.html"):
    if request.method == 'POST':
        from pprint import pprint
        pprint(vars(request.POST))
    product = get_object_or_404(Product, slug=slug)
    if product.option_group:
        option_group = product.option_group

    context = {
        'product': product,
        'option_group': option_group,
    }
    return render_to_response(template_name, context, RequestContext(request))
