from django.conf.urls import patterns, url

from .models import Product


urlpatterns = patterns('',
    url(r'^mountain/$', 'store.views.mountain', name='mountain'),
    url(r'^mountain/bikes/$', 'store.views.mountain_bikes', name='mountain_bikes'),
    url(r'^mountain/bikes/(?P<slug>[-\w]+)/$', 'store.views.mountain_bike_model', name='mountain_bike_model'),
    url(r'^mountain/frames/$', 'store.views.mountain_frames', name='mountain_frames'),
    #url(r'^mountain/frames/(?P<model>)/$', 'store.views.mountain_frame_model', name='mountain_frame_model'),
    url(r'^road/$', 'store.views.road', name='road'),
    #url(r'^road/bikes$', 'store.views.road_bikes', name='road_bikes'),
    #url(r'^road/bikes/(?P<model>)/$', 'store.views.road_bike_model', name='road_bike_model'),
    #url(r'^road/frames/$', 'store.views.road_frames', name='road_frames'),
    #url(r'^road/frames/(?P<model>)/$', 'store.views.road_frame_model', name='road_frame_model'),
    )
