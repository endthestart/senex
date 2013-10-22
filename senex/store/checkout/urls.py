from django.conf.urls import patterns, include, url
from store.checkout import views

from store.checkout.views import IndexView, ShippingAddressView, ShippingMethodView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='checkout_start'),
    url(r'^shipping-address/$', ShippingAddressView.as_view(), name='checkout_shipping_address'),
    url(r'^shipping-method/$', ShippingMethodView.as_view(), name='checkout_shipping_method'),
#    #url(r'^payment/$', 'store.checkout.views.home', name='checkout_payment'),
#    #url(r'^preview/$', 'store.checkout.views.home', name='checkout_preview'),
#    #url(r'^thank-you/$', 'store.checkout.views.home', name='checkout_thank_you'),
)
