from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.core.exceptions import *
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.db.utils import IntegrityError
from django.db.models import Q
from django.views.generic.edit import CreateView
from .forms import *
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'Barber/customerSignUp.html'
    success_url = '/index/'  # Set the success URL after registration

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)  # Redirect to the success_url

class CustomerLoginView(LoginView):
    form_class = CustomerLoginForm
    template_name = 'Barber/customerLogin.html'  # Specify your login template
    success_url = reverse_lazy('index')  # Set the success URL after login

class CustomerLogoutView(LogoutView):
    template_name = 'Barber/logout.html'
    next_page = reverse_lazy('custom_logout')


def index_view(request):
    # Your view logic here
    return render(request, 'Barber/index.html')




