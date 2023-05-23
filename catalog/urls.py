from django.urls import path
from catalog.views import home, info
from catalog.apps import CatalogConfig
app_name = CatalogConfig.name
urlpatterns = [

    path('', home, name='home'),
    path('contacts/', info, name='contacts'),
]
