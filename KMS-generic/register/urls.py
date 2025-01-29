from django.urls import path
from . import views
from django.urls import re_path as url

app_name = 'users'

urlpatterns = [
    #path('register/', views.register_view, name="register"),
    #path('login', views.login_view, name="login"),

    url('register', views.register_view, name='register'),
]