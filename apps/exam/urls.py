from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^travels$', views.travels),
    url(r'^join/(?P<id>\d+)$', views.join),
    url(r'^travels/destination/(?P<id>\d+)$', views.trip),
    url(r'^add$', views.add),
    url(r'^addtravel$', views.addtravel),
]
