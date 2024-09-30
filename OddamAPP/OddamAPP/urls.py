"""
URL configuration for OddamAPP project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from donations.views import landing_page, user_profile, user_settings, login_view, register_view, logout_view, AddDonation

urlpatterns = [
    path('ustawienia/', user_settings, name='user_settings'),
    path('profil/', user_profile, name='user_profile'),
    path('admin/', admin.site.urls),
    path('', landing_page, name='landing-page'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('form/', AddDonation.as_view(), name='form'),
    path('logout/', logout_view, name='logout'),
    path('form-confirmation/', AddDonation.as_view(), name='form-confirmation')
]
