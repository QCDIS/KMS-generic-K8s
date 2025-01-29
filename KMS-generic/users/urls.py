from django.urls import path
from . import views
from django.urls import re_path as url

app_name = 'users'

urlpatterns = [
    #path('register/', views.register_view, name="register"),
    #path('login', views.login_view, name="login"),

    url('scheduler', views.scheduler, name='scheduler'),
    url('createschedule', views.create_schedule, name="createschedule"),
    #url('edit/<int:schedule_id>/', views.edit_schedule, name='editschedule'),
    path('edit/<int:schedule_id>/', views.edit_schedule, name='editschedule'),
    path('delete/<int:schedule_id>/', views.delete_schedule, name='deleteschedule'),
    path('saveprofile/<int:id>/', views.save_profile, name='saveprofile'),
    path('request/<str:id>/', views.request_resolve, name='requestresolve'),


]

