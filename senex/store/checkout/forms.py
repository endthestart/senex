from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

from store.contact.forms import AbstractAddressForm
from store.contact.models import ShippingAddress
from store.contact.utils import normalize_email
from custom_auth.models import User


class ShippingAddressForm(AbstractAddressForm):
    def __init__(self, *args, **kwargs):
        super(ShippingAddressForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ShippingAddress
        exclude = ('user')


class GatewayForm(AuthenticationForm):
    username = forms.EmailField(label=_("My email address is"))
    GUEST, NEW, EXISTING = 'anonymous', 'new', 'existing'
    CHOICES = (
        (GUEST, _("I am a new customer and want to checkout as a guest")),
        (NEW, _("I am a new customer and want to create an account before checkout uut")),
        (EXISTING, _("I am a returning customer, and my password is"))
    )
    options = forms.ChoiceField(widget=forms.widgets.RadioSelect, choices=CHOICES, initial=GUEST)

    def clean_username(self):
        return normalize_email(self.cleaned_data['username'])

    def clean(self):
        if self.is_guest_checkout() or self.is_new_account_checkout():
            if 'password' in self.errors:
                del self.errors['password']
            if 'username' in self.cleaned_data:
                email = normalize_email(self.cleaned_data['username'])
                if User.objects.filter(email=email).exists():
                    msg = "A user with that email already exists"
                    self._errors["username"] = self.error_class([msg])
            return self.cleaned_data
        return super(GatewayForm, self).clean()

    def is_guest_checkout(self):
        return self.cleaned_data.get('options', None) == self.GUEST

    def is_new_account_checkout(self):
        return self.cleaned_data.get('options', None) == self.NEW
