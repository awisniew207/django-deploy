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
from django.contrib.auth.views import LoginView
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


def index_view(request):
    # Your view logic here
    return render(request, 'Barber/index.html')
'''
def shop_signup(request):
    if request.method == 'POST':
        # Handle form submission
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if user_exists(username, email):
            # Handle the case where the username or email is not unique
            return render(request, 'Barber/signup.html', {'error_message': 'Username or email already taken'})

        try:
            # Call the createUser function to create the user
            user = createUser(username, email, password)
            group = Group.objects.get(name='Customers-Sign')  # Assuming the group already exists
            user.groups.add(group)
            
        # Redirect the user to a success page
            return redirect('index') 

        except IntegrityError:
            # Handle other potential errors related to user creation or database constraints
            return render(request, 'Barber/signup.html', {'error_message': 'An error occurred during registration'})
    else:
        return render(request, 'Barber/signup.html')
'''



