from django.urls import re_path

from dataset_elastic import views

urlpatterns = [
    # url(r'^index', views.index, name='index'),
    re_path(r'^rest', views.rest, name='rest'),
    re_path(r'^genericsearch', views.genericsearch, name='genericsearch'),

]
