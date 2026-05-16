from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('menu/', views.menu, name = 'menu'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.register, name='register'),
]