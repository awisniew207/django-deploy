"""
URL configuration for LineUp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from Barber import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/customer/', views.CustomerSignUpView.as_view(), name='customerSignup'),
    path('signup/barber/', views.BarberSignUpView.as_view(), name='barberSignup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.CustomerLogoutView.as_view(), name='custom_logout'),
    path('profile/customer/edit/<slug:slug>/', views.CustomerUpdateProfile.as_view(), name='customerEditProfileView'),
    path('profile/barber/edit/<slug:slug>/', views.BarberUpdateProfile.as_view(), name='barberEditProfileView'),
    path('profile/', views.UserProfileRedirectView.as_view(), name='user_profile_redirect'),
    path("profile/customer/<slug:slug>", views.CustomerProfileView.as_view(), name="customerProfileView"),
    path("profile/barber/<slug:slug>", views.BarberProfileView.as_view(), name="barberProfileView"),
    path('index/', views.index_view, name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)