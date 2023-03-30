from django.urls import re_path

from webSearch import views

urlpatterns = [
    # url(r'^index', views.index, name='index'),
    re_path(r'^genericsearch', views.genericsearch, name='genericsearch'),
    re_path(r'^addToBasket', views.addToBasket, name='addToBasket'),
    re_path(r'^downloadCart', views.downloadCart, name='downloadCart'),
]
