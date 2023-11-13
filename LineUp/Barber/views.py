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
from django.views import View
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
    model = User
    form_class = CustomerProfileForm
    template_name = 'Barber/customerProfileEdit.html'  # Adjust the template path as needed

    def get_object(self, queryset=None):
        # Get the User instance for the logged-in customer
        return get_object_or_404(User, username=self.request.user.username)

    def form_valid(self, form):
        print("Form is valid. Saving changes.")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form is invalid:", form.errors)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('customerProfileView', kwargs={'slug': self.object.slug})


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
    context_object_name = 'customer'  # This will be the customer instance
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        # Fetch the Customer instance using the slug from the URL
        slug = self.kwargs.get(self.slug_url_kwarg)
        customer = Customer.objects.filter(user__slug=slug).first()
        return customer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the Customer instance related to the profile being viewed
        customer = self.get_object()

        if customer:
            # Fetch reviews written by the customer
            context['reviews'] = Review.objects.filter(customer=customer.user)

            # Check if the logged-in user is viewing their own profile
            context['is_own_profile'] = self.request.user == customer.user

            # Pass additional customer information if needed
            context['customer_info'] = {
                'first_name': customer.user.first_name,
                'last_name': customer.user.last_name,
                'phone_number': customer.user.phone_num,
                # Any other fields you want to include
            }
        else:
            # Handle the case where the customer does not exist
            context['reviews'] = []
            context['is_own_profile'] = False
            context['customer_info'] = {}

        return context

class BarberProfileView(LoginRequiredMixin, DetailView):
    model = Barber
    template_name = 'Barber/barberProfileView.html'
    context_object_name = 'barber'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg)
        return Barber.objects.filter(user__slug=slug).first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        barber = self.get_object()

        reviews_list = Review.objects.filter(barber=barber).order_by('-created_at')
        paginator = Paginator(reviews_list, 3)  # Show 3 reviews per page

        page = self.request.GET.get('page')

        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results
            page_obj = paginator.page(paginator.num_pages)

        context['reviews'] = page_obj
        context['is_own_profile'] = self.request.user == barber.user

        return context


#---------------------------------------------------------------------------------------
class BarberSignUpView(CreateView):
    model = Barber
    form_class = BarberSignUpForm
    template_name = 'Barber/barberSignUp.html'

    def form_valid(self, form):
        # Save the new user first
        user = form.save()
        # Then log the user in
        login(self.request, user)

        # After successful registration and login, redirect to a specific page
        # For example, redirect to the barber's profile page
        return redirect('barberProfileView', slug=user.slug)

    def get_success_url(self):
        # This method might be redundant if you're redirecting within form_valid
        # You can keep it if you have a specific use case for it
        return reverse_lazy('login')

    def form_invalid(self, form):
        # Logging form errors can be helpful for debugging
        print("Form is invalid:", form.errors)
        return super().form_invalid(form)

class BarberUpdateProfile(UpdateView):
    model = User
    form_class = BarberProfileForm
    template_name = 'Barber/barberProfileEdit.html'

    def get_object(self, queryset=None):
        # Get the User instance for the logged-in barber
        return get_object_or_404(User, username=self.request.user.username)

    def form_valid(self, form):
        # Save the user instance
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the barber's profile page after successful update
        return reverse_lazy('barberProfileView', kwargs={'slug': self.object.slug})

def index_view(request):
    # Your view logic here
    return render(request, 'Barber/index.html')

class WriteReviewView(View):
    def get(self, request, slug):
        barber = get_object_or_404(Barber, user__slug=slug)
        form = ReviewForm()  # Assuming you have a ReviewForm
        return render(request, 'Barber/write_review.html', {'form': form, 'barber': barber})

    def post(self, request, slug):
        barber = get_object_or_404(Barber, user__slug=slug)
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.barber = barber
            review.customer = request.user  # Assuming the reviewer is the logged-in user
            review.save()
            return redirect('barberProfileView', slug=slug)  # Redirect to the barber's profile
        return render(request, 'Barber/write_review.html', {'form': form, 'barber': barber})



