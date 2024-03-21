from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import logoutUser
from discussion_board import settings
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('logout/', logoutUser, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('settings/change_password', auth_views.PasswordChangeView.as_view(template_name='change_password.html'), name='change_password'),
    path('settings/change_password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='change_password_done.html'), name='password_change_done'),
]