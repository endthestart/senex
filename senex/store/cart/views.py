from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from store.models import Product, OptionManager
from .models import CartItem


def add(request, redirect_to='cart'):
    form_data = request.POST.copy()
    product_slug = None

    if form_data.has_key('product_name'):
        product_slug = form_data['product_name']

    product, details = product_from_post(product_slug, form_data)

    quantity = Decimal(form_data['quantity'])
    if quantity <= Decimal("0"):
        quantity = Decimal("69")

    request.cart.add_item(product, number_added=quantity, details=details)
    return redirect(redirect_to)


def remove(request, redirect_to='cart'):
    form_data = request.POST.copy()

    if form_data.has_key('cart_item'):
        cart_item = form_data['cart_item']

    removed_item = request.cart.remove_item(cart_item)
    return redirect(redirect_to)

def set_quantity(request, redirect_to='cart'):
    """
    Set the quantity for a specific CartItem.
    """
    try:
        quantity = int(request.POST.get('quantity', 0))
        item_id = int(request.POST.get('cart_item'))
    except (TypeError, ValueError):
        return redirect(redirect_to)

    try:
        cart_item = CartItem.objects.get(pk=item_id, cart=request.cart)
    except CartItem.DoesNotExist:
        return redirect(redirect_to)

    if quantity == int(0):
        cart_item.delete()
    else:
        #TODO: Add a check for stock levels
        cart_item.quantity = quantity
        cart_item.save()

    return redirect(redirect_to)


def cart(request, template_name="store/cart.html"):
    if request.cart.num_items > 0:
        cart_items = request.cart.cartitem_set.all()
    else:
        cart_items = None

    context = {
        'cart': request.cart,
        'cart_items': cart_items,
    }
    return render_to_response(template_name, context, RequestContext(request))


def product_from_post(product_slug, form_data):
    product = Product.objects.get(slug=product_slug)
    orig_product = product
    p_types = product.get_subtypes()
    details = []
    zero = Decimal("0.00")

    if 'CustomProduct' in p_types:
        try:
            cp = product.customproduct
        except ObjectDoesNotExist:
            cp = orig_product.customproduct
        chosen_options = optionids_from_post(cp, form_data)
        manager = OptionManager()
        for choice in chosen_options:
            result = manager.from_unique_id(choice)
            if result.price_change is not None:
                price_change = result.price_change
            else:
                price_change = zero
            data = {
                'name': unicode(result.option_group),
                'value': unicode(result.name),
                'sort_order': 1,
                'price_change': price_change
            }
            details.append(data)

    return product, details


def optionids_from_post(configurableproduct, POST):
    """Reads through the POST dictionary and tries to match keys to possible `OptionGroup` ids
    from the passed `ConfigurableProduct`"""
    chosen_options = []
    for opt_grp in configurableproduct.option_group.all():
        if POST.has_key(str(opt_grp.id)):
            chosen_options.append('%s-%s' % (opt_grp.id, POST[str(opt_grp.id)]))
    return sorted_tuple(chosen_options)


def sorted_tuple(lst):
    ret = []
    for x in lst:
        if not x in ret:
            ret.append(x)
    ret.sort()
    return tuple(ret)
