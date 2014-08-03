from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'senex.views.home', name='home'),
                       url(r'^account/login/$', 'senex.views.login', name='login'),
                       url(r'^account/logout/$', 'senex.views.logout', name='logout'),
                       url(r'^account/register/$', 'senex.views.register', name='register'),
                       url(r'^contact/$', 'senex.views.contact', name='contact'),
                       url(r'^contact/thanks/$', 'senex.views.contact_thanks', name='contact_thanks'),
                       url(r'^checkout/', include('senex_shop.checkout.urls')),
                       url(r'^cart/', include('senex_shop.cart.urls')),
                       url(r'^shop/', include('senex_shop.urls')),
                       url(r'^news/', include('senex_shop.news.urls')),
                       url(r'^account/', include('django.contrib.auth.urls')),
                       url(r'^grappelli/', include('grappelli.urls')),
                       url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('django.contrib.flatpages.views',
                        url(r'^about/$', 'flatpage', {'url': '/about/'}, name='about'),
                        url(r'^custom/$', 'flatpage', {'url': '/custom/'}, name='custom'),
)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
                            (r'media/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}),
    )
