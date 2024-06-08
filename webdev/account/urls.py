from django.contrib.auth.views import PasswordChangeDoneView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, reverse_lazy

from . import views

app_name = 'account'

urlpatterns = [
    path('login/',
         views.LoginUserView.as_view(),
         name='login'),
    path('logout/',
         views.user_logout,
         name='logout'),
    path('profile/follow/<int:pk>/',
         views.CreateUserFollowingView.as_view(),
         name='follow'),
    path('password-change/',
         views.UserPasswordChangeView.as_view(),
         name='password_change'),
    path('password-change/done/',
         PasswordChangeDoneView.as_view(template_name="account/password_change_done.html"),
         name='password_change_done'),
    path('password-reset/',
         PasswordResetView.as_view(template_name='account/password_reset_form.html',
                                   email_template_name='account/password_reset_email.html',
                                   success_url=reverse_lazy('account:password_reset_done')),
         name='password_reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name="account/password_reset_confirm.html",
                                          success_url=reverse_lazy('account:password_reset_complete')),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(template_name="account/password_reset_complete.html"),
         name='password_reset_complete'),
    path('register/',
         views.RegisterUserView.as_view(),
         name='register'),
    path('profile/<int:user_pk>/',
         views.ProfileUserView.as_view(),
         name='profile'),
    path('edit_profile/',
         views.EditProfileUserView.as_view(),
         name='edit_profile'),
]
