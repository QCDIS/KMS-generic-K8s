from django.urls import re_path as url

from webAPI import views

urlpatterns = [
    url(r'^genericsearch', views.genericsearch, name='genericsearch'),
]
