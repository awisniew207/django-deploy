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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
#from .views import book_view
import debug_toolbar

from Barber import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/customer/', views.CustomerSignUpView.as_view(), name='customerSignup'),
    path('signup/barber/', views.BarberSignUpView.as_view(), name='barberSignup'),
    path('registration/shop/', views.ShopRegistrationView.as_view(), name='shopRegistration'),
    path('signup/owner/', views.OwnerSignUpView.as_view(), name='ownerSignup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.CustomerLogoutView.as_view(), name='custom_logout'),
    path('profile/customer/edit/<slug:slug>/', views.CustomerUpdateProfile.as_view(), name='customerEditProfileView'),
    path('profile/barber/edit/<slug:slug>/', views.BarberUpdateProfile.as_view(), name='barberEditProfileView'),
    path('profile/owner/edit/<slug:slug>/', views.OwnerUpdateProfile.as_view(), name='ownerEditProfileView'),
    path('profile/', views.UserProfileRedirectView.as_view(), name='user_profile_redirect'),
    path("profile/customer/<slug:slug>", views.CustomerProfileView.as_view(), name="customerProfileView"),
    path('profile/barber/<slug:slug>/', views.BarberProfileView.as_view(), name='barberProfileView'),
    path("profile/owner/<slug:slug>", views.OwnerProfileView.as_view(), name="ownerProfileView"),
    path('review/write/<slug:slug>/', views.WriteReviewView.as_view(), name='write_review'),
    path('index/', views.index_view, name='index'),
    path('', views.redir_view, name='redir'),    
    path('__debug__/', include(debug_toolbar.urls)),
    #path('book/', views.book_view, name='book'),
    path('barber_book/<slug:barber_slug>', views.barber_book_view, name='barber_book'),
    path('book-timeslot/', views.book_timeslot, name='book_timeslot'),
    path('update-working-hours/', views.update_working_hours, name='update_working_hours'),
    path('search-barbers/', views.search_barbers, name='search_barbers'),
    path('search/shops/', views.search_shops, name='search_shops'),
    path('shop/<slug:slug>/', views.ShopDetailView.as_view(), name='shop_detail'),
    path('booking-success/', views.booking_success, name='booking_success'),
    path('inbox/', views.inbox_view, name='inbox'),
    path('barber-appointments/', views.barber_appointments_view, name='barber_appointments_view'),
    path('manage_services/', views.ManageServicesView.as_view(), name='manage_services'),
    path('edit_service/<int:service_id>/', views.ManageServicesView.as_view(), name='edit_service'),
    path('manage_services/<int:service_id>/delete/', views.DeleteServiceView.as_view(), name='delete_service'),
    path('not_a_barber/', views.not_a_barber_view, name='not_a_barber'),
    path('shop/<int:shop_id>/barbers/', views.barbers_list_view, name='barbers_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    