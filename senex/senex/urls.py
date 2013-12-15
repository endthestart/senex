from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'senex.views.home', name='home'),
    url(r'^contact/$', 'senex.views.contact', name='contact'),
    url(r'^contact/thanks/$', 'senex.views.contact_thanks', name='contact_thanks'),
    url(r'^custom/$', 'senex.views.custom', name='custom'),
    url(r'^checkout/', include('store.checkout.urls')),
    url(r'^cart/', include('store.cart.urls')),
    url(r'^shop/', include('store.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('django.contrib.flatpages.views',
    url(r'^about/$', 'flatpage', {'url': '/about/'}, name='about'),
)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'media/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}),
    )
