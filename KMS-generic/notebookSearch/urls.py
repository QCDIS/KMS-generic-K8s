from django.urls import re_path as url

from notebookSearch import views

urlpatterns = [
    url(r'^genericsearch', views.genericsearch, name='genericsearch'),
]
