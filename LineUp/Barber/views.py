from django.shortcuts import render
from django.shortcuts import HttpResponse
from .models import Customer, BarberUser
from django.core.exceptions import *
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.db.utils import IntegrityError
from django.db.models import Q


def index(request):
    return render(request, 'Barber/index.html')

def createCustomer(username, email, password):
    user = User.objects.create_user(username=username, email=email, password=password)
    user.save()
    return user

def createBarber(username, email, password, firstname, lastname):
    user = BarberUser.objects.create(username=username, email=email, password=password, f_name=firstname, l_name=lastname)
    return user

def user_exists(username, email):
    # Check if a user with the given username or email already exists
    return User.objects.filter(Q(username=username) | Q(email=email)).exists()

def buser_exists(username, email):
    # Check if a user with the given username or email already exists
    return BarberUser.objects.filter(Q(username=username) | Q(email=email)).exists()

def customer_signup(request):
    if request.method == 'POST':
        # Handle form submission
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if user_exists(username, email):
            # Handle the case where the username or email is not unique
            return render(request, 'Barber/customerSignUp.html', {'error_message': 'Username or email already taken'})

        try:
            # Call the createUser function to create the user
            user = createCustomer(username, email, password)
            group = Group.objects.get(name='Customers')  # Assuming the group already exists
            user.groups.add(group)
            
        # Redirect the user to a success page
            return redirect('index') 

        except IntegrityError:
            # Handle other potential errors related to user creation or database constraints
            return render(request, 'Barber/customerSignUp.html', {'error_message': 'An error occurred during registration'})
    else:
        return render(request, 'Barber/customerSignUp.html')

def barber_signup(request):
    if request.method == 'POST':
        # Handle form submission
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        
        if buser_exists(username, email):
            # Handle the case where the username or email is not unique
            return render(request, 'Barber/barberSignUp.html', {'error_message': 'Username or email already taken'})

        try:
            # Call the createBarber function to create the user
            user = createBarber(username, email, password, firstname, lastname)
            group = Group.objects.get(name='Barbers')  # Assuming the group already exists
            user.groups.add(group)
            
            # Redirect the user to a success page
            return redirect('index') 

        except IntegrityError as e:
            # Handle the specific IntegrityError and provide a more specific error message
            if 'UNIQUE constraint' in str(e):
                return render(request, 'Barber/barberSignUp.html', {'error_message': 'Username or email already taken'})
            else:
                return render(request, 'Barber/barberSignUp.html', {'error_message': 'An error occurred during registration'})
    else:
        return render(request, 'Barber/barberSignUp.html')

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



