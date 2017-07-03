from django.conf.urls import url
from kegpiapp import views


urlpatterns = [url(r'^$', views.view_main, name="main"),
               url(r'^edit_keg/$', views.edit_keg, name="new keg"),
               url(r'^edit_keg/(?P<pk>[0-9]+)/$', views.edit_keg, name="edit keg"),
               url(r'^edit_keg/(?P<pk>[0-9]+)/remove/$', views.remove_keg, name="remove keg"),
               url(r'^view_kegs/$', views.view_kegs, name="view kegs"),

               url(r'^edit_sensor/$', views.edit_sensor, name="new sensor"),
               url(r'^edit_sensor/(?P<pk>[0-9]+)/$', views.edit_sensor, name="edit sensor"),
               url(r'^edit_sensor/(?P<pk>[0-9]+)/remove/$', views.remove_sensor, name="remove sensor"),
               url(r'^view_sensors/$', views.view_sensors, name="view sensors"),

               url(r'^edit_beverage/$', views.edit_beverage, name="new beverage"),
               url(r'^edit_beverage/(?P<pk>[0-9]+)/$', views.edit_beverage, name="edit beverage"),
               url(r'^edit_beverage/(?P<pk>[0-9]+)/remove/$', views.remove_beverage, name="remove beverage"),
               url(r'^view_beverages/$', views.view_beverages, name="view beverages"),

               url(r'^keg_info/$', views.get_keg_info, name="keg info"),
               url(r'^keg_block/$', views.get_keg_block, name="keg block"),
               ]
