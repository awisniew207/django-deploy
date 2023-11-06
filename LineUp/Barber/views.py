from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.core.exceptions import *
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.db.utils import IntegrityError
from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView
from .forms import *
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from .models import Customer, Barber
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views.generic.base import View

class CustomerSignUpView(CreateView):
    model = Customer
    form_class = CustomerSignUpForm
    template_name = 'Barber/customerSignUp.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # Log in the user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('login')

    def form_invalid(self, form):
        # Set initial values for the username and email fields
        form.fields['username'].initial = self.request.POST.get('username')
        form.fields['email'].initial = self.request.POST.get('email')
        return super().form_invalid(form)

class LoginView(LoginView):
    form_class = LoginForm
    template_name = 'Barber/login.html'

    def get_success_url(self):
        # Redirect to the user's profile using their slug
        return reverse_lazy('index')

class CustomerLogoutView(LogoutView):
    template_name = 'Barber/logout.html'
    next_page = reverse_lazy('custom_logout')

class CustomerUpdateProfile(UpdateView):
    model = Customer
    form_class = ProfileForm
    template_name = 'Barber/customerProfileEdit.html'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        # Perform additional actions upon form submission if needed
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the user's profile using their slug
        return reverse_lazy('profileView', kwargs={'slug': self.request.user.slug})

class UserProfileRedirectView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user

        if user.is_customer:
            # Debugging statement
            print("Redirecting to customer profile view")
            # Redirect to the customer profile page
            return redirect('customerProfileView', slug=user.slug)
        elif user.is_barber:
            # Debugging statement
            print("Redirecting to barber profile view")
            # Redirect to the barber profile page
            return redirect('barberProfileView', slug=user.slug)
        else:
            # Handle other user types or scenarios as needed
            return redirect('index')  # Redirect to the home page or an appropriate fallback
            
class CustomerProfileView(LoginRequiredMixin, DetailView):
    model = Customer
    template_name = 'Barber/customerProfileView.html'
    context_object_name = 'customer'
    slug_url_kwarg = 'slug'

    # Ensure that only the user's own profile is accessible
    def get_object(self, queryset=None):
        user = super().get_object(queryset)
        return user

    # Optionally, you can specify a custom query to fetch the user profile
    def get_queryset(self):
        return User.objects.all()

    # Set a context variable indicating whether the user is viewing their own profile
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_own_profile'] = self.request.user == self.object
        return context

class BarberProfileView(LoginRequiredMixin, DetailView):
    model = Barber
    template_name = 'Barber/barberProfileView.html'
    context_object_name = 'barber'  # Name for the context variable
    slug_url_kwarg = 'slug'  # Optionally, customize the slug parameter as needed

    # Ensure that only the user's own profile is accessible
    def get_object(self, queryset=None):
        user = super().get_object(queryset)
        return user

    # Optionally, you can specify a custom query to fetch the user profile
    def get_queryset(self):
        return User.objects.all()  # Customize this query as needed

    # Set a context variable indicating whether the user is viewing their own profile
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_own_profile'] = self.request.user == self.object
        return context


#---------------------------------------------------------------------------------------
class BarberSignUpView(CreateView):
    model = Barber
    form_class = BarberSignUpForm
    template_name = 'Barber/barberSignUp.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # Log in the user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('login')

    def form_invalid(self, form):
        # Set initial values for the username and email fields
        form.fields['username'].initial = self.request.POST.get('username')
        form.fields['email'].initial = self.request.POST.get('email')

        return super().form_invalid(form)

def index_view(request):
    # Your view logic here
    return render(request, 'Barber/index.html')



