from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'senex.views.home', name='home'),
    url(r'^about/$', 'senex.views.about', name='about'),
    url(r'^contact/$', 'senex.views.contact', name='contact'),
    url(r'^contact/thanks/$', 'senex.views.contact_thanks', name='contact_thanks'),
    url(r'^mountain/$', 'senex.views.mountain', name='mountain'),
    url(r'^road/$', 'senex.views.road', name='road'),
    # url(r'^senex/', include('senex.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
