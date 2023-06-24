import os

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import ListView

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Version
from config import settings

# @login_required
# @permission_required('main:view_product')
def home(request):
    path = settings.MEDIA_ROOT
    img_list = os.listdir(path + '/images')
    extra_context = {
        'product_list': Product.objects.all()[:3],
        'title': 'Главная',
        'images': img_list,
        'object_list': Product.objects.filter(status='Активна')
    }
    return render(request, 'catalog/home.html', extra_context)


class ProductListView(LoginRequiredMixin, generic.ListView):
    model = Product
    extra_context = {'title': 'Список продукции', 'object_list': Product.objects.filter(status='Активна')}

    def get_object(self, queryset=None):
        return self.request.user
# def products(request):
#     path = settings.MEDIA_ROOT
#     img_list = os.listdir(path + '/images')
#     context = {
#         'product_list': Product.objects.all(),
#         'title': 'Список продукции',
#         'images': img_list
#     }
#     return render(request, 'catalog/product_list.html', context)
class ProductDetailView(LoginRequiredMixin,  generic.DetailView):
    model = Product
    permission_required = 'catalog.view_product'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = context_data['object']
        #context_data['description'] = self.get_object()
        context_data['versions'] = Version.objects.filter(name_of_product=self.object, actual_version=True)
        return context_data
    def get_object(self, queryset=None):
        return self.request.user

# def product(request, pk):
#     product_item = Product.objects.get(pk=pk)
#     context = {
#         'object': product_item,
#         'title': product_item
#     }
#     return render(request, 'catalog/product_detail.html', context)

class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Product
    fields = ('name', 'description', 'preview', 'category', 'price', 'date_create', 'date_change')
    success_url = reverse_lazy('main:product_list')
    permission_required = 'catalog.add_product'
    def get_object(self, queryset=None):
        return self.request.user

class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form_with_formset.html'
    #fields = ('name', 'description', 'preview', 'category', 'price', 'date_create', 'date_change')
    success_url = reverse_lazy('main:product_list')
    permission_required = 'catalog.change_product'

    def get_success_url(self, *args, **kwargs):
        return reverse('main:product_update', args=[self.get_object().pk])
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)

    def get_object(self, queryset=None):
        return self.request.user
class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Product
    success_url = reverse_lazy('main:product_list')
    def test_func(self):
        return self.request.user.is_superuser

    def get_object(self, queryset=None):
        return self.request.user
class VersionListView(ListView):
    model = Version

# @login_required
def info(request):
    context = {
        'title': 'Контакты',

    }
    return render(request, 'catalog/info.html')
