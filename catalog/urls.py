from django.urls import path
from django.views.decorators.cache import cache_page, never_cache
from catalog.apps import CatalogConfig
from catalog.views import home, info, ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView, VersionListView, CategoriesListView

app_name = CatalogConfig.name
urlpatterns = [

    path('', home, name='home'),
    path('contacts/', info, name='contacts'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('categories/', CategoriesListView.as_view(), name='categories_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_item'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('products/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('products/versions/<int:pk>/', VersionListView.as_view(), name='version'),
]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)
