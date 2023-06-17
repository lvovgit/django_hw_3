from django.urls import path

from blog.apps import BlogConfig
from blog.views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, toggle_publish

app_name = BlogConfig.name

urlpatterns = [
    path('blog/', PostListView.as_view(), name='post_list'),
    path('posts/<slug:post_slug>/', PostDetailView.as_view(), name='post_item'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('posts/update/<slug:post_slug>/', PostUpdateView.as_view(), name='post_update'),
    path('posts/delete/<slug:post_slug>/', PostDeleteView.as_view(), name='post_delete'),
    path('posts/toggle/<slug:post_slug>/', toggle_publish, name='toggle_publish')
]