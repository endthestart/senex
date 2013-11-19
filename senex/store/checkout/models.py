from django.db import models
from decimal import Decimal
from django.utils.translation import ugettext_lazy as _

from ..cart.models import Cart
from ..contact.models import BillingAddress, ShippingAddress

from django.conf import settings


USER_MODULE_PATH = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Sale(models.Model):
    def __init__(self, *args, **kwargs):
        super(Sale, self).__init__(*args, **kwargs)

        import stripe
        stripe.api_key = settings.STRIPE_SECRET_KEY

        self.stripe = stripe

    charge_id = models.CharField(max_length=32)

    def charge(self, price_in_cents, number, exp_month, exp_year, cvc):
        """
        Takes a price and credit card details: number, exp_month, exp_year, and cvc.

        Returns a tuple: (Boolean, Class) Where:
        The boolean is if the charge was successful.
        The Class is the response (or error) instance.
        """

        if self.charge_id:
            return False, Exception(message="This has already been charged.")

        try:
            response = self.stripe.Charge.create(
                amount = price_in_cents,
                currency = "usd",
                card = {
                    "number": number,
                    "exp_month": exp_month,
                    "exp_year": exp_year,
                    "cvc": cvc,
                },
                description='Thank you for your purchase!'
            )

            self.charge_id = response.id

        except self.stripe.CardError, ce:
            # charge failed
            return False, ce

        return True, response


class Order(models.Model):
    number = models.CharField(
        _("order number"),
        max_length=128,
        db_index=True,
    )
    cart = models.ForeignKey(
        Cart,
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        USER_MODULE_PATH,
        blank=True,
        null=True,
        verbose_name=_("user"),
    )
    billing_address = models.ForeignKey(
        BillingAddress,
        null=True,
        blank=True,
        verbose_name=_("billing address"),
    )
    total_incl_tax = models.DecimalField(
        _("order total (inc. tax)"),
        decimal_places=2,
        max_digits=12,
    )
    total_excl_tax = models.DecimalField(
        _("order total (excl tax)"),
        decimal_places=2,
        max_digits=12,
    )
    shipping_incl_tax = models.DecimalField(
        _("shipping charge (inc. tax)"),
        decimal_places=2,
        max_digits=12,
    )
    shipping_excl_tax = models.DecimalField(
        _("shipping charge (excl. tax)"),
        decimal_places=2,
        max_digits=12,
    )
    shipping_address = models.ForeignKey(
        ShippingAddress,
        null=True,
        blank=True,
        verbose_name=_("shipping address")
    )
    shipping_method = models.CharField(
        _("shipping method"),
        max_length=128,
        null=True,
        blank=True,
    )
    shipping_code = models.CharField(
        blank=True,
        max_length=128,
        default='',
    )
    status = models.CharField(
        _("status"),
        max_length=100,
        null=True,
        blank=True,
    )
    guest_email = models.EmailField(
        _("guest email address"),
        null=True,
        blank=True,
    )
    date_ordered = models.DateField(
        auto_now_add=True,
        db_index=True,
    )

    @property
    def is_anonymous(self):
        return self.user is None

    @property
    def email(self):
        if not self.user:
            return self.guest_email
        return self.user.email
