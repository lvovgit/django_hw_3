from django.shortcuts import redirect #get_object_or_404,
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, \
    UpdateView, DeleteView

from blog.models import Post


class PostListView(ListView):
    model = Post

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(published=True)
        return queryset


class PostDetailView(DetailView):
    model = Post

    def get_object(self, **kwargs):
        views = super().get_object()
        views.increase_view_count()
        return views


class PostCreateView(CreateView):
    model = Post
    fields = ('name', 'content', 'image', 'published')
    success_url = reverse_lazy('blog:post_list', )

    # def post(self, request, *args, **kwargs):
    #     post_object = Post()
    #     post_object.name = request.POST.get('name')
    #     post_object.content = request.POST.get('content')
    #     post_object.image = request.POST.get('image')
    #     post_object.published = request.POST.get('published')
    #     slug = slugify(request.POST.get('name'))
    #     post_object.slug = slug
    #
    #     if request.POST.get('published'):
    #         post_object.published = True
    #     else:
    #         post_object.published = False
    #
    #     post_object.save()
    #
    #     return redirect(f'/posts/{slug}/')


class PostUpdateView(UpdateView):
    model = Post
    fields = ('name', 'content', 'image', 'published')

    def get_success_url(self):
        return reverse('blog:post_item', kwargs={'slug': self.object.slug})


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')


# def toggle_publish(slug):
#     post_item = get_object_or_404(Post, slug=slug)
#     if post_item.published:
#         post_item.published = False
#     else:
#         post_item.published = True
#
#     post_item.save()
#
#     return redirect(reverse('blog:blog_item', args=[post_item.slug]))
