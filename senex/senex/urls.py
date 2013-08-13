from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'senex.views.home', name='home'),
    url(r'^contact/$', 'senex.views.contact', name='contact'),
    url(r'^contact/thanks/$', 'senex.views.contact_thanks', name='contact_thanks'),
    url(r'^custom/$', 'senex.views.custom', name='custom'),
    url(r'^mountain/$', 'senex.views.mountain', name='mountain'),
    url(r'^road/$', 'senex.views.road', name='road'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^cart/', include('tinycart.urls'))
)

urlpatterns += patterns('django.contrib.flatpages.views',
    url(r'^about/$', 'flatpage', {'url': '/about/'}, name='about'),
)
