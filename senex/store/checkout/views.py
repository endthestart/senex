import json

from django.contrib import messages
from django.contrib.auth import login
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, TemplateView

from .forms import GatewayForm, ShippingAddressForm
from .session import CheckoutSessionMixin
from store.contact.models import UserAddress


class IndexView(CheckoutSessionMixin, FormView):
    template_name = 'checkout/gateway.html'
    form_class = GatewayForm
    success_url = reverse_lazy('checkout_shipping_address')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return self.get_success_response()
        return super(IndexView, self).get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(IndexView, self).get_form_kwargs()
        email = self.checkout_session.get_guest_email()
        if email:
            kwargs['initial'] = {
                'username': email,
            }
        return kwargs

    def form_valid(self, form):
        if form.is_guest_checkout() or form.is_new_account_checkout():
            email = form.cleaned_data['username']

            if form.is_new_account_checkout():
                messages.info(
                    self.request,
                    _("Create your account and then you will be redirected back to the checkout process")
                )
                self.success_url = "{0}?next={1}&email={2}".format(
                    reverse('customer:register'),
                    reverse('checkout:shipping-address'),
                    email
                )
        else:
            user = form.get_user()
            login(self.request, user)

        return self.get_success_response()

    def get_success_response(self):
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.success_url


class ShippingAddressView(CheckoutSessionMixin, FormView):
    """
    Determine the shipping for the order.
    """
    template_name = 'checkout/shipping_address.html'
    form_class = ShippingAddressForm

    def get(self, request, *args, **kwargs):
        # Check if the user has items in the cart
        if request.cart.is_empty:
            messages.error(request, _("You need to add some items to your cart to checkout."))
            return HttpResponseRedirect(reverse('cart'))

        # Check that guests have entered an email address
        if not request.user.is_authenticated() and not self.checkout_session.get_guest_email():
            messages.error(request, _("Please sign in or enter your email address."))
            return HttpResponseRedirect(reverse('checkout_start'))

        #TODO: Enable shipping status on carts
        # Ensure that the shipping address is needed
        #if not request.cart.is_shipping_required():
        #    messages.info(request, _("Your cart does not require a shipping address to be submitted."))
        #    return HttpResponseRedirect(self.get_success_url())

        return super(ShippingAddressView, self).get(request, *args, **kwargs)

    def get_initial(self):
        return self.checkout_session.new_shipping_address_fields()

    def get_context_data(self, **kwargs):
        kwargs = super(ShippingAddressView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            kwargs['addresses'] = self.get_available_addresses()
        return kwargs

    def get_available_addresses(self):
        return UserAddress.objects.filter(user=self.request.user).order_by('-is_default_shipping')

    def post(self, request, *args, **kwargs):
        # Check is shipping address was selected directly
        if self.request.user.is_authenticated() and 'address_id' in self.request.POST:
            address = UserAddress.objects.get(pk=self.request.POST['address_id'], user=self.request.user)
            action = self.request.POST.get('action', None)
            if action == 'ship_to':
                # User has selected a previous address to ship to
                self.checkout_session.ship_to_user_address(address)
                return HttpResponseRedirect(self.get_success_url())
            elif action == 'delete':
                address.delete()
                messages.info(self.request, _("Address deleted from your address book"))
                return HttpResponseRedirect(reverse('checkout_shipping_method'))
            else:
                return HttpResponseBadRequest()
        else:
            return super(ShippingAddressView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        # Store the address details in the sessions and redirect to the next step.
        address_fields = dict(
            (k, v) for (k, v) in form.instance.__dict__.items()
            if not k.startswith('_')
        )
        self.checkout_session.ship_to_new_address(address_fields)
        return super(ShippingAddressView, self).form_valid(form)

    def get_success_url(self):
        return reverse('checkout_shipping_method')

#TODO: Add UserAddressUpdateView
#TODO: Add UserAddressDeleteView

class ShippingMethodView(CheckoutSessionMixin, TemplateView):
    template_name = 'checkout/shipping_methods.html'

    def get(self, request, *args, **kwargs):
        if request.cart.is_empty:
            messages.error(request, _("You need to add some items to your cart to checkout."))
            return HttpResponseRedirect(reverse('cart'))

        if not request.cart.is_shipping_required():
            self.checkout_session.use_shipping_method(NoShippingRequired().code)
            return self.get_success_response()

        if not self.checkout_session.is_shipping_address_set():
            messages.error(request, _("Please choose a shipping address"))
            return HttpResponseRedirect(reverse('checkout_shipping_address'))

        self._methods = self.get_available_shipping_methods()
        if len(self._methods) == 0:
            messages.warning(request, _("Shipping is unavailable for your chosen address - please choose another."))
            return HttpResponseRedirect(reverse('checkout_shipping_address'))
        elif len(self._methods) == 1:
            self.checkout_session.use_shipping_method(self._methods[0].code)
            return self.get_success_response()

        return super(ShippingMethodView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs = super(ShippingMethodView, self).get_context_data(**kwwargs)
        kwargs['methods'] = self._methods
        return kwargs

    def get_available_shipping_methods(self):
        return None

    def post(self, request, *args, **kwargs):
        method_code = request.POST.get('method_code', None)
        is_valid = False
        for method in self.get_available_shipping_methods():
            if method.code == method.code:
                is_valid = True
        if not is_valid:
            messages.error(request, _("Your submitted shipping method is not permitted."))
            return HttpResponseRedirect(reverse('checkout_shipping_method'))

        self.checkout_session.use_shipping_method(method_code)
        return self.get_success_response()

    def get_success_response(self):
        return HttpResponseRedirect(reverse('checkout_payment_method'))
