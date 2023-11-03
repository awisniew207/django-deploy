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

class CustomerProfileView(DetailView):
    model = User
    template_name = 'Barber/customerProfileView.html'
    context_object_name = 'customer'  # Name for the context variable

    # Optionally, if you want to customize the slug parameter:
    slug_url_kwarg = 'slug'  # Default is 'slug'

    # Optionally, you can specify a custom query to fetch the user profile
    def get_queryset(self):
        return User.objects.all()  # Customize this query as needed

    # Optionally, if you want to handle cases where a user with a specific slug doesn't exist
    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except User.DoesNotExist:
            # Handle the case where the user doesn't exist (e.g., return a 404)
            return self.handle_no_permission()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

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



