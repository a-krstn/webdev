from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, AuthenticationForm

from .models import User


class LoginForm(AuthenticationForm):
    """Форма аутентификации пользователя"""

    username = forms.CharField(label='Email')
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


class UserRegistrationForm(UserCreationForm):
    """Форма регистрации пользователя"""

    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль',
                                widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email']

    # def clean_password2(self):
    #     cd = self.cleaned_data
    #     if cd['password'] != cd['password2']:
    #         raise forms.ValidationError('Пароли не совпадают')
    #     return cd['password2']

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Этот адрес электронной почты уже используется')
        return data


class ProfileUserForm(forms.ModelForm):
    """Форма редактирования профиля пользователя"""

    username = forms.CharField(disabled=True, label='Имя пользователя')
    email = forms.CharField(disabled=True, label='Email')

    class Meta:
        model = get_user_model()
        fields = ['photo', 'username', 'email', 'first_name', 'last_name']


class UserPasswordChangeForm(PasswordChangeForm):
    """Форма изменения пароля"""

    old_password = forms.CharField(label='Старый пароль')
    new_password1 = forms.CharField(label='Новый пароль')
    new_password2 = forms.CharField(label='Повторите новый пароль')
