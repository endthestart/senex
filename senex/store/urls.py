from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       url(r'^$', 'store.views.store_home', name='store_home'),
                       url(r'^(?P<path>.+)/p/(?P<slug>[-\w]+)/$', 'store.views.product_detail', name='product_detail'),
                       url(r'^(?P<path>.+)/$', 'store.views.category', name='category'),
)
