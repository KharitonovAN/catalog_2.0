from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView, PasswordResetView, PasswordResetConfirmView
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from users.utils import register_confirm
from django.views import View
from django.views.generic import CreateView, UpdateView
from config import settings
from users.forms import RegisterForm, UserProfileForm, UserForgotPasswordForm, UserSetNewPasswordForm
from users.models import User


class LoginView(BaseLoginView):
    template_name = 'users/login.html'


def logout_user(request):
    logout(request)
    return redirect('catalog:home')


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:confirm_register')

    def form_valid(self, form):
        new_user = form.save()
        new_user.user_token = token_generator.make_token(new_user)
        form.save()
        register_confirm_ = register_confirm(self.request, user=new_user)
        if form.is_valid():
            new_user = form.save()
            send_mail(
                subject='Подтверждение почты',
                message=register_confirm_['message'],
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[new_user.email]
            )
        return super().form_valid(form)


class ConfirmUserView(View):
    def get(self, request, uuid):
        try:
            user = User.objects.get(field_uuid=uuid)
            user.is_active = True
            user.has_perm('catalog.view_product')
            user.has_perm('blog.view_product')
            user.save()
            return render(request, 'users/confirm_register.html')
        except User.DoesNotExist:
            return render(request, 'users/error_register.html')


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    success_url = reverse_lazy('users:profile')
    form_class = UserProfileForm

    def get_object(self, queryset=None):
        return self.request.user


class UserForgotPasswordView(PasswordResetView):
    form_class = UserForgotPasswordForm
    template_name = 'users/user_password_reset.html'
    success_url = reverse_lazy('catalog:home')
    success_message = 'Письмо с инструкцией по восстановлению пароля отправлена на ваш email'
    subject_template_name = 'users/password_subject_reset_mail.txt'
    email_template_name = 'users/password_reset_mail.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = UserSetNewPasswordForm
    template_name = 'users/user_password_set_new.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Пароль успешно изменен. Можете авторизоваться на сайте.'
