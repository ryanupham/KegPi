from django.conf.urls import url
from kegpiapp import views


urlpatterns = [url(r'^$', views.view_main, name="main"),
               url(r'^edit_keg/$', views.edit_keg, name="new keg"),
               url(r'^edit_keg/(?P<pk>[0-9]+)/$', views.edit_keg, name="edit keg"),
               url(r'^edit_keg/(?P<pk>[0-9]+)/remove/$', views.remove_keg, name="remove keg"),
               url(r'^view_kegs/$', views.view_kegs, name="view kegs"),

               url(r'^edit_beverage/$', views.edit_beverage, name="new beverage"),
               url(r'^edit_beverage/(?P<pk>[0-9]+)/$', views.edit_beverage, name="edit beverage"),
               url(r'^edit_beverage/(?P<pk>[0-9]+)/remove/$', views.remove_beverage, name="remove beverage"),
               url(r'^view_beverages/$', views.view_beverages, name="view beverages"),

               url(r'^edit_gas/$', views.edit_gas, name="new gas tank"),
               url(r'^edit_gas/(?P<pk>[0-9]+)/$', views.edit_gas, name="edit gas tank"),
               url(r'^edit_gas/(?P<pk>[0-9]+)/remove/$', views.remove_gas, name="remove gas tank"),
               url(r'^view_gas/$', views.view_gas, name="view gas tanks"),

               url(r'^edit_sensor/$', views.edit_sensor, name="new sensor"),
               url(r'^edit_sensor/(?P<pk>[0-9]+)/$', views.edit_sensor, name="edit sensor"),
               url(r'^edit_sensor/(?P<pk>[0-9]+)/remove/$', views.remove_sensor, name="remove sensor"),
               url(r'^view_sensors/$', views.view_sensors, name="view sensors"),

               url(r'^state_info/$', views.get_state_info, name="state info"),
               url(r'^data_block/$', views.get_keg_block, name="data block"),
               ]
