from urllib.parse import urlparse
from django.urls import path,include
from home import views

urlpatterns = [
    path('', views.home, name="home"),
    path('dashboard/', include('dashboard.urls')),
    
]