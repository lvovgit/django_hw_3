from django.conf.urls.static import static
from django.urls import path
from catalog.views import home, info
from catalog.apps import CatalogConfig
from config import settings

app_name = CatalogConfig.name
urlpatterns = [

                  path('', home, name='home'),
                  path('contacts/', info, name='contacts'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)
