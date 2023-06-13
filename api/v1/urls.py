from django.urls import path

from .views import Search


urlpatterns = [
    path('search', Search.as_view(), name='api-v1-search'),
    path('search/<resource_type>', Search.as_view(), name='api-v1-search'),
    ]
