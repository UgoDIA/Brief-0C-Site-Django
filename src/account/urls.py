from urllib.parse import urlparse
from django.urls import path
from account import views


urlpatterns = [
    path('register', views.register, name="register"),
    path('login', views.log_user, name='login'),
    path('logout', views.log_out, name='logout'),
]
