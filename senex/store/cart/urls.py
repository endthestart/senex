from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       url(r'^$', 'store.cart.views.cart', name='cart'),
                       url(r'^add/$', 'store.cart.views.add', name='cart_add'),
                       url(r'^remove/$', 'store.cart.views.remove', name='cart_remove'),
                       url(r'^quantity/$', 'store.cart.views.set_quantity', name='cart_quantity'),
)
