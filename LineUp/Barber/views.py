from django.shortcuts import render
from django.shortcuts import HttpResponse
from .models import Customer
from django.core.exceptions import *
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.db.utils import IntegrityError
from django.db.models import Q

def index(request):
    return render(request, 'Barber/index.html')

def createUser(username, email, password):
    user = User.objects.create_user(username=username, email=email, password=password)
    # You can also set additional user attributes here if needed
    user.save()
    return user

def user_exists(username, email):
    # Check if a user with the given username or email already exists
    return User.objects.filter(Q(username=username) | Q(email=email)).exists()

def signup(request):
    if request.method == 'POST':
        # Handle form submission
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if user_exists(username, email):
            # Handle the case where the username or email is not unique (e.g., show an error message)
            return render(request, 'Barber/signup.html', {'error_message': 'Username or email already taken'})

        try:
            # Call the createUser function to create the user
            user = createUser(username, email, password)
            group = Group.objects.get(name='Customers-Sign')  # Assuming the group already exists
            user.groups.add(group)
            
        # Redirect the user to a success page
            return redirect('index')  # Replace 'welcome' with the actual URL name

        except IntegrityError:
            # Handle other potential errors related to user creation or database constraints
            return render(request, 'Barber/signup.html', {'error_message': 'An error occurred during registration'})
    else:
        return render(request, 'Barber/signup.html')





