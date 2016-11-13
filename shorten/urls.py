from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^!.*', views.item, name='item'),
    url(r'^.*', views.redirect, name='redirect'),
]
