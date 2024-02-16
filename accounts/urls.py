from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    
    # path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name="logout_view"),
    path('register/', views.register_view, name='register_view'),
    # path('change_password/', views.change_password, name="change_password"),
    # path("password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),   

    path('account/account-menu/', views.account_view, name='account-menu'),
    path('account/account_edit/', views.edit_account, name='account-edit'),
]