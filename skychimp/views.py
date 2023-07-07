from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.http import Http404
from skychimp.models import *
from django.conf import settings
from skychimp.services import send_email
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

class IndexView(TemplateView):
    template_name = 'skychimp/skychimp_index.html'
    extra_context = {
        'title': 'Главная страница',
        'object_list': Sending.objects.all()
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class CustomerListView(ListView):
    model = Customer
    # extra_context = {
    #     'object_list': Customer.objects.all(),
    #     'title': 'Все клиенты'  # дополнение к статической информации
    # }

class CustomerDetailView(DetailView):
    model = Customer


class CustomerCreateView(CreateView):
    model = Customer
    fields = ('name', 'email', 'comment', 'created_by',)
    success_url = reverse_lazy('skychimp:customer_list')


class CustomerUpdateView(UpdateView):
    model = Customer
    fields = ('name', 'email', 'comment', 'created_by', 'is_active',)

    def get_success_url(self):
        return reverse('skychimp:customer_view', args=[str(self.object.pk)])


class CustomerDeleteView(DeleteView):
    model = Customer
    success_url = reverse_lazy('skychimp:customer_list')

class MessageListView(ListView):
    model = Message
    extra_context = {
        'message_list': Message.objects.all(),
        'title': 'Все Сообщения'  # дополнение к статической информации
    }


class MessageDetailView(DetailView):
    model = Message


class MessageCreateView(CreateView):
    model = Message
    fields = ('subject', 'body', )
    success_url = reverse_lazy('skychimp:message_list')


class MessageUpdateView(UpdateView):
    model = Message
    fields = ('subject', 'body', )

    def get_success_url(self):
        return reverse('skychimp:sending_view', args=[str(self.object.pk)])


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('skychimp:message_list')


class SendingListView(ListView):
    model = Sending
    extra_context = {
        'object_list': Sending.objects.all(),
        'title': 'Все Рассылки'  # дополнение к статической информации
    }
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     if self.request.user.has_perm('skychimp.view_sending'):
    #         return queryset
    #     return Sending.objects.filter(created=self.request.user)

class SendingDetailView(DetailView):
    model = Sending


class SendingCreateView(CreateView):
    model = Sending
    fields = ('message', 'frequency', 'status', 'created')
    success_url = reverse_lazy('skychimp:sending_list')
    send_email(Sending.ONCE)

class SendingUpdateView(UpdateView):
    model = Sending
    fields = ('message', 'frequency', 'status', )

    def get_success_url(self):
        return reverse('skychimp:sending_view', args=[str(self.object.pk)])


class SendingDeleteView(DeleteView):
    model = Sending
    success_url = reverse_lazy('skychimp:sending_list')

class AttemptListView(ListView):
    model = Attempt
    extra_context = {
        'object_list': Attempt.objects.all(),
        'title': 'Все Рассылки'  # дополнение к статической информации
    }


class AttemptDetailView(DetailView):
    model = Attempt

def set_is_active(request, pk):
    customer_item = get_object_or_404(Customer, pk=pk)  # get_object_or_404 ищет объект модели если не находит выводит ошибку
    if customer_item.is_active:
        customer_item.is_active = False
    else:
        customer_item.is_active = True
    customer_item.save()
    return redirect(reverse('skychimp:customer_list'))


def set_status_sending(request, pk):
    sending_item = get_object_or_404(Sending, pk=pk)  # get_object_or_404 ищет объект модели если не находит выводит ошибку
    if sending_item.status == Sending.CREATED:
        sending_item.status = Sending.COMPLETED
        sending_item.save()
    else:
        sending_item.status = Sending.CREATED
        sending_item.save()
    return redirect(reverse('skychimp:sending_list'))