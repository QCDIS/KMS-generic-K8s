import os
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.urls import re_path
from django.views.generic.base import RedirectView

#base_path = os.environ.get('BASE_PATH').strip()
base_path = "search"
if base_path:
    base_path += '/'

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^'+base_path, include([
        re_path(r'^dataset_elastic/',
                include(('dataset_elastic.urls', 'dataset_elastic'), namespace="dataset_elastic")),
        re_path(r'^notebookSearch/', include(('notebookSearch.urls', 'notebookSearch'), namespace="notebookSearch")),
        re_path(r'^webSearch/', include(('webSearch.urls', 'webSearch'), namespace="webSearch")),
        re_path(r'^genericpages/', include(('genericpages.urls', 'genericpages'), namespace="genericpages")),
        re_path(r'^webAPI/', include(('webAPI.urls', 'webAPI'), namespace="webAPI")),
        re_path(r'^api/', include(('api.urls', 'api'), namespace='api')),
        re_path(r'^accounts/', include(('login.urls', 'login'), namespace='login')),
        re_path(r'^accounts/', include(('register.urls', 'register'), namespace='register')),
        re_path(r'^users/', include(('users.urls', 'users'), namespace='users')),
        path('', include(('genericpages.urls', 'genericpages'), namespace="genericpages"))
    ])),
]

# Nafis: API Endpoint (api/) was for testing purposes only. It is not fully implemented, nor needed at this point. Oct 22, '24

if base_path:
    urlpatterns.append(
        re_path(r'^/?$', RedirectView.as_view(url=base_path, permanent=False)),
        )

# urlpatterns = [
# 	path('admin/', admin.site.urls),
# 	re_path(r'^dataset_elastic/', include(('dataset_elastic.urls', 'dataset_elastic'), namespace="dataset_elastic")),
# 	re_path(r'^notebookSearch/', include(('notebookSearch.urls', 'notebookSearch'), namespace="notebookSearch")),
# 	re_path(r'^webSearch/', include(('webSearch.urls', 'webSearch'), namespace="webSearch")),
# 	re_path(r'^genericpages/', include(('genericpages.urls', 'genericpages'), namespace="genericpages")),
# 	re_path(r'^webAPI/', include(('webAPI.urls', 'webAPI'), namespace="webAPI")),
# 	re_path(r'^DSS/', include(('DSS.urls', 'DSS'), namespace="DSS")),
# 	re_path(r'^accountManagement/', include(('accountManagement.urls', 'accountManagement'), namespace="accountManagement")),
# 	path('', include(('genericpages.urls', 'genericpages'), namespace="genericpages")),
#
# ]
