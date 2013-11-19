from django.conf.urls import patterns, url

from store.checkout.views import IndexView, ShippingAddressView, ShippingMethodView, PaymentMethodView, PaymentDetailsView, UserAddressUpdateView, UserAddressDeleteView

urlpatterns = patterns('',
                       url(r'^$', IndexView.as_view(), name='checkout_start'),
                       url(r'^shipping-address/$', ShippingAddressView.as_view(), name='checkout_shipping_address'),
                       url(r'^shipping-address/$', UserAddressUpdateView.as_view(),
                           name='checkout_user_address_update'),
                       url(r'^shipping-address/$', UserAddressDeleteView.as_view(),
                           name='checkout_user_address_delete'),
                       url(r'^shipping-method/$', ShippingMethodView.as_view(), name='checkout_shipping_method'),
                       url(r'^payment-method/$', PaymentMethodView.as_view(), name='checkout_payment_method'),
                       url(r'^payment-details/$', PaymentDetailsView.as_view(), name='checkout_payment_details'),
                       #    #url(r'^preview/$', 'store.checkout.views.home', name='checkout_preview'),
                       #    #url(r'^thank-you/$', 'store.checkout.views.home', name='checkout_thank_you'),
)
