import random

from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView, PasswordContextMixin
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import UpdateView, CreateView, TemplateView, FormView

from config import settings
from users.forms import UserForm, UserRegisterForm
from users.models import User


class ProfileUpdateView(UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:profile')
    template_name = 'users/user_register.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Страница пользователя: {self.object.email}'
        return context


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/user_register.html'
    success_message = 'Вы успешно зарегистрировались. Проверьте почту для активации!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация на сайте'
        return context

    def form_valid(self, form):
        self.object = form.save()
        token = default_token_generator.make_token(self.object)
        uid = urlsafe_base64_encode(force_bytes(self.object.pk))
        activation_url = reverse_lazy('users:confirm_email', kwargs={'uidb64': uid, 'token': token})

        send_mail(
            subject='Подтверждение почты',
            message=f'Для подтверждения регистрации перейдите по ссылке: http://localhost:8000/{activation_url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.object.email],
            fail_silently=False
        )
        return redirect('users:email_confirmation_sent')
        # super().form_valid(form)


class UserConfirmEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('users:email_confirmed')
        else:
            return redirect('users:email_confirmation_failed')


class EmailConfirmationSentView(TemplateView):
    template_name = 'users/email_confirmation_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Письмо активации отправлено'
        return context


class EmailConfirmedView(TemplateView):
    template_name = 'users/email_confirmed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес активирован'
        return context


class EmailConfirmationFailedView(TemplateView):
    template_name = 'users/email_confirmation_failed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес не активирован'
        return context


def generate_new_password(request):
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])

    send_mail(
        subject='Вы сменили пароль',
        message=f'Ваш новый сгенерированный пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email],
        fail_silently=False
    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('users:login'))


def backup_pass(request):
    if request.method == "POST":
        email = request.POST.get('email')
        generate_new_password(email)
    return render(request, 'users/backup_pass.html')

# def form_valid(self, form):
#     if form.is_valid():
#         self.object = form.save()
#         self.object.is_active = False
#         self.object.token = secrets.token_urlsafe(18)[:15]
#         confirm_account(self.object)
#         self.object.save()
#         self.user_token = self.object.token
#         self.object = form.save()
#     return super().form_valid(form)

# def get_success_url(self):
#     new_url = super().get_success_url()
#     token = self.object.token
#     return str(new_url) + str(token)


# def page_after_registration(request, token):
#     if request.method == 'POST':
#         obj = get_object_or_404(User, token=token)
#         confirm_account(obj)
#     return render(request, 'users/page_after_registration.html')
#
#
# def activate_user(request, token):
#     user = User.objects.filter(token=token).first()
#     if user:
#         user.is_active = True
#         user.save()
#         return redirect('users:login')
#     return render(request, 'users/user_not_found.html')
#


# def generate_pass(request):
#     if request.method == "POST":
#         email = request.POST.get('email')
#         generate_new_password(email)
#
#     return render(request, 'users/backup_pass.html')


# def generate_new_password(request):
#     pass_ch = secrets.token_urlsafe(18)[:9]
#     send_mail(
#         subject='Смена пароля',
#         message=f'Ваш новый пароль {pass_ch}',
#         from_email=settings.EMAIL_HOST_USER,
#         recipient_list=[request.user.email]
#     )
#     # print(pass_ch)
#     request.user.set_password(pass_ch)
#     request.user.save()
#     return redirect(reverse('users:login'))


# class PasswordChangeView_(TemplateView):
#     form_class = UserBackupForm
#     success_url = reverse_lazy("users:generate_new_password")
#     template_name = "users/backup_pass.html"
#     success_message = 'Вы успешно сменили пароль. Проверьте почту!'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # context['title'] = 'Смена пароля на сгенерированный'
#         return context
#
#     # def backup_pass(self, request):
#     #     if request.method == "POST":
#     #         email = request.POST.get('email')
#     #         generate_new_password(email)
#     #     return redirect(reverse('users:login'))
#         # render(request, 'users/backup_pass.html')
# class WebPasswordResetView(PasswordResetView):
#     pass
