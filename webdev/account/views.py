from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core.cache import cache
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View, generic
from django.conf import settings

from .forms import *
from services import services


class LoginUserView(LoginView):
    """
    Аутентификация пользователя
    """

    form_class = LoginForm
    template_name = 'account/login.html'
    extra_context = {'title': "Авторизация"}

    def get(self, request, *args, **kwargs):
        """
        Перенаправление на главную страницу, если пользователь уже авторизован
        """

        if request.user.is_authenticated:
            return redirect('index')
        return super().get(self, request, *args, **kwargs)


def user_logout(request):
    """
    Выход пользователя
    """

    logout(request)
    return redirect('index')


class RegisterUserView(generic.CreateView):
    """
    Регистрация пользователя
    """

    form_class = UserRegistrationForm
    template_name = 'account/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('account:login')

    def get(self, request, *args, **kwargs):
        """
        Перенаправление на главную страницу, если пользователь уже зарегистрирован и авторизован
        """

        if request.user.is_authenticated:
            return redirect('index')
        return super().get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            services.create_user(form)
            return redirect('account:login')
        return render(request, self.template_name, {'form': form})


class ProfileUserView(LoginRequiredMixin, generic.DetailView):
    """
    Профиль пользователя
    """

    model = get_user_model()
    template_name = 'account/profile.html'
    context_object_name = 'username'
    pk_url_kwarg = 'user_pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user_pk = kwargs['object'].pk
        last_user_posts = cache.get(f'last_user_posts_{profile_user_pk}')
        if not last_user_posts:
            last_user_posts = services.all_objects(kwargs['object'].blog_posts)[:5]
            cache.set('last_user_posts', last_user_posts)
        context['username_posts'] = last_user_posts
        context['default_image'] = settings.DEFAULT_USER_IMAGE
        context['title'] = f'Профиль: {self.request.user.username}'
        return context


class EditProfileUserView(LoginRequiredMixin, generic.UpdateView):
    """
    Изменение данных пользователя
    """

    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'account/edit_profile.html'
    extra_context = {'title': 'Профиль пользователя',
                     'default_image': settings.DEFAULT_USER_IMAGE}

    def get_success_url(self):
        return reverse_lazy('account:profile', args=(self.request.user.pk,))

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChangeView(PasswordChangeView):
    """
    Изменение пароля
    """

    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('account:password_change_done')
    template_name = 'account/password_change_form.html'
    extra_context = {'title': 'Изменение пароля'}


class CreateUserFollowingView(LoginRequiredMixin, View):
    """
    Оформление подписки на пользователя
    """

    model = get_user_model()

    def post(self, request, pk):
        user = services.get_instance_by_unique_field(self.model, pk=pk)
        follower = request.user
        services.subscribe(user, follower)
        return redirect(user.get_absolute_url())
