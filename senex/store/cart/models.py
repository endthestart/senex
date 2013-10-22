from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from store.models import Product

USER_MODULE_PATH = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class CartManager(models.Manager):
    def get_for_request(self, request):
        if request.user.is_authenticated():
            return self.get_or_create(user=request.user)[0]
        if 'cart' in request.session:
            try:
                return self.get(pk=request.session['cart'])
            except self.model.DoesNotExist:
                pass
        cart = self.create(user=None)
        request.session['cart'] = cart.pk
        return cart


class Cart(models.Model):
    """
    Store items currently in a cart.
    """
    description = models.CharField(
        _("description"),
        blank=True,
        null=True,
        max_length=10,
    )
    created = models.DateTimeField(
        _("created"),
        auto_now_add=True,
    )
    user = models.ForeignKey(
        USER_MODULE_PATH,
        verbose_name=_("customer"),
        blank=True,
        null=True,
    )

    objects = CartManager()

    def _get_count(self):
        item_count = 0
        for item in self.cartitem_set.all():
            item_count += item.quantity
        return item_count
    num_items = property(_get_count)

    def _get_total(self):
        total = Decimal('0')
        for item in self.cartitem_set.all():
            total += item.line_total
        return total
    total_price = property(_get_total)

    def add_item(self, chosen_item, number_added, details=[]):
        already_in_cart = False
        item_to_modify = CartItem(cart=self, product=chosen_item, quantity=Decimal('0'))
        if 'CustomProduct' not in chosen_item.get_subtypes():
            for similar_item in self.cartitem_set.filter(product__id = chosen_item.id):
                looks_the_same = len(details) == similar_item.details.count()
                if looks_the_same:
                    for detail in details:
                        try:
                            similar_item.details.get(
                                name=detail['name'],
                                value=unicode(detail['value']),
                                price_change=detail['price_change']
                            )
                        except CartItemDetails.DoesNotExist:
                            looks_the_same = False
                if looks_the_same:
                    item_to_modify = similar_item
                    already_in_cart = True
                    break
        if not already_in_cart:
            self.cartitem_set.add(item_to_modify)

        item_to_modify.quantity += number_added
        item_to_modify.save()
        if not already_in_cart:
            for data in details:
                item_to_modify.add_detail(data)

        return item_to_modify

    def remove_item(self, chosen_item_id, number_removed=None):
        item_to_modify = self.cartitem_set.get(id=chosen_item_id)
        if number_removed:
            item_to_modify.quantity -= number_removed
        else:
            item_to_modify.quantity = 0
        if item_to_modify.quantity <= 0:
            item_to_modify.delete()
        else:
            item_to_modify.save()

    def empty(self):
        for item in self.cartitem_set.all():
            item.delete()
        self.save()

    def _is_empty(self):
        if self.num_items > 0:
            return False
        return True
    is_empty = property(_is_empty)

    class Meta:
        verbose_name = _("Shopping Cart")
        verbose_name_plural = _("Shopping Carts")


class CartItem(models.Model):
    """
    An Individual item in the cart.
    """
    cart = models.ForeignKey(
        Cart,
        verbose_name=_("cart"),
    )
    product = models.ForeignKey(
        Product,
        verbose_name=_("product"),
    )
    quantity = models.DecimalField(
        _("quantity"),
        max_digits=18,
        decimal_places=6,
    )

    def _get_line_unit_price(self):
        return self.product.price
    unit_price = property(_get_line_unit_price)

    def get_detail_price(self):
        """
        Get the delta price based on detail modifications.
        """
        delta = Decimal('0')
        if self.has_details:
            for detail in self.details.all():
                if detail.price_change and detail.value:
                    delta += detail.price_change
        return delta

    def _get_line_total(self):
        return self.unit_price * self.quantity
    line_total = property(_get_line_total)

    def _get_description(self):
        return self.product.name
    description = property(_get_description)

    def add_detail(self, data):
        detail = CartItemDetails(
            cartitem=self,
            name=data['name'],
            value=data['value'],
            sort_order=data['sort_order'],
            price_change=data['price_change']
        )
        detail.save()

    def _has_details(self):
        return(self.details.count() > 0)

    has_details = property(_has_details)

    def __unicode__(self):
        return u"{quantity} - {name} {price}".format(quantity=self.quantity, name=self.product.name, price=self.line_total)

    class Meta:
        verbose_name = _("Cart Item")
        verbose_name_plural = _("Cart Items")
        ordering = ('id',)


class CartItemDetails(models.Model):
    """
    An arbitrary detail about a cart item.
    """
    cartitem = models.ForeignKey(
        CartItem,
        related_name='details',
    )
    value = models.TextField(_("detail"))
    name = models.CharField(
        _("name"),
        max_length=100,
    )
    price_change = models.DecimalField(
        _("price change"),
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("The cost change of the detail."),
    )
    sort_order = models.IntegerField(
        _("sort order"),
        help_text=_("The display order for this group."),
    )

    class Meta:
        ordering = ('sort_order',)
        verbose_name = _("Cart Item Detail")
        verbose_name_plural = _("Cart Item Details")
