from django.urls import path
from django.views.decorators.cache import never_cache

from blog.apps import BlogConfig
from blog.views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView  #, toggle_publish

app_name = BlogConfig.name

urlpatterns = [
    path('blog/', never_cache(PostListView.as_view()), name='post_list'),
    path('posts/<slug:slug>/', PostDetailView.as_view(), name='post_item'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('posts/update/<slug:slug>/', PostUpdateView.as_view(), name='post_update'),
    path('posts/delete/<slug:slug>/', PostDeleteView.as_view(), name='post_delete'),
    # path('posts/toggle/<slug>/', toggle_publish, name='toggle_publish')
]