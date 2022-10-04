from django.urls import path

from users import views


urlpatterns = [
    path('registration', views.RegistrationView.as_view(), name='registration'),
    path('login', views.LoginView.as_view(), name='login'),
    path('user', views.UserView.as_view(), name='user'),
    path('logout', views.LogoutView.as_view(), name='logout'),
]
