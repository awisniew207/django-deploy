from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import *
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView
from .forms import *
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from .models import Customer, Barber
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.views import View
from .models import Barber, TimeSlot, create_or_update_timeslots_for_barber, Service
from django.core.serializers import serialize
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pytz
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render
from .models import TimeSlot
from django.utils import timezone

class CustomerSignUpView(CreateView):
    model = Customer
    form_class = CustomerSignUpForm
    template_name = 'Barber/customerSignUp.html'

    def form_valid(self, form):
        # Save the new user first
        user = form.save()
        # Then log the user in
        login(self.request, user)

        # After successful registration and login, redirect to a specific page
        # For example, redirect to the barber's profile page
        return redirect('customerProfileView', slug=user.slug)

    def form_invalid(self, form):
        # Logging form errors can be helpful for debugging
        print("Form is invalid:", form.errors)
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
        if user.is_barber:
            # Debugging statement
            print("Redirecting to barber profile view")
            # Redirect to the barber profile page
            return redirect('barberProfileView', slug=user.slug)
        if user.is_owner:
            # Debugging statement
            print("Redirecting to owner profile view")
            # Redirect to the barber profile page
            return redirect('ownerProfileView', slug=user.slug)
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

#---------------------------------------------------------------------------------------

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

    def form_invalid(self, form):
        # Logging form errors can be helpful for debugging
        print("Form is invalid:", form.errors)
        return super().form_invalid(form)

class BarberUpdateProfile(UpdateView):
    model = User
    form_class = BarberProfileForm
    template_name = 'Barber/barberProfileEdit.html'

    def get_object(self, queryset=None):
        return get_object_or_404(User, username=self.request.user.username, is_barber=True)

    def form_valid(self, form):
        user = form.save(commit=False)
        affiliation_code = form.cleaned_data.get('affiliation_code')
        
        if affiliation_code:
            try:
                shop = Shop.objects.get(affiliation_code=affiliation_code)
                barber_profile = Barber.objects.get(user=user)
                barber_profile.shops.add(shop)
            except Shop.DoesNotExist:
                pass  # Ignore if the shop doesn't exist

        user.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('barberProfileView', kwargs={'slug': self.object.slug})

def index_view(request):
    all_barbers = list(Barber.objects.all())
    all_shops = list(Shop.objects.all())

    random_barbers = random.sample(all_barbers, min(len(all_barbers), 5))
    random_shops = random.sample(all_shops, min(len(all_shops), 5))

    context = {
        'random_barbers': random_barbers,
        'random_shops': random_shops,
    }

    return render(request, 'Barber/index.html', context)

def search_barbers(request):
    query = request.GET.get('query', '')

    if query:
        # Filter barbers whose user's username contains the query string
        barbers = Barber.objects.filter(user__username__icontains=query)
    else:
        # If no query is provided, return all barbers
        barbers = Barber.objects.all()

    context = {
        'barbers': barbers,
        'query': query  # Include the query in the context to display it in the search bar
    }
    return render(request, 'Barber/search_template.html', context)

def search_shops(request):
    query = request.GET.get('query', '')
    shops = Shop.objects.filter(name__icontains=query)
    return render(request, 'Barber/shop_search_template.html', {'shops': shops, 'query': query})


def redir_view(request):
    # Your view logic here
    return render(request, 'Barber/redirect.html')

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

#--------------------------------------------------------------------------------------------------
class OwnerSignUpView(CreateView):
    model = Owner
    form_class = OwnerSignUpForm
    template_name = 'Barber/ownerSignUp.html'

    def form_valid(self, form):
        # Save the new user first
        user = form.save()
        # Then log the user in
        login(self.request, user)
    
    def form_invalid(self, form):
        # Logging form errors can be helpful for debugging
        print("Form is invalid:", form.errors)
        return super().form_invalid(form)

def book_view(request):
    barbers = Barber.objects.all()
    print("Barbers: ", barbers)
    timeslots_data = {}

    for barber in barbers:
        timeslots = TimeSlot.objects.filter(barber=barber, is_booked=False)
        # Use barber.user.id as the key since Barber's primary key is User
        timeslots_data[barber.user.id] = json.loads(serialize('json', timeslots))
    
    print("Timeslots Data:", timeslots_data)

    context = {
        'barbers': barbers, 
        'timeslots_data': json.dumps(timeslots_data)
    }
    return render(request, 'Barber/book.html', context)

@csrf_exempt
def book_timeslot(request):
    if request.method == 'POST':
        timeslot_id = request.POST.get('timeslot_id')
        try:
            timeslot = TimeSlot.objects.get(pk=timeslot_id)
            if not timeslot.is_booked:
                timeslot.is_booked = True
                timeslot.booked_by = request.user
                timeslot.save()

                # Notify the barber via email (example)
                send_mail(
                    'New Appointment Booking',
                    f'You have a new appointment booked for {timeslot.start_time}.',
                    settings.DEFAULT_FROM_EMAIL,
                    [timeslot.barber.user.email],
                    fail_silently=False,
                )

                success_url = reverse('booking_success')  # 'booking_success' is the name of your success page URL
                return JsonResponse({'status': 'success', 'redirect_url': success_url})
            else:
                return JsonResponse({'status': 'error', 'message': 'This timeslot is already booked.'}, status=400)
        except TimeSlot.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid timeslot ID.'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
def update_working_hours(request):
    barber = get_object_or_404(Barber, user=request.user)
    
    if request.method == 'POST':
        form = BarberWorkingHoursForm(request.POST, instance=barber)
        if form.is_valid():
            form.save()
            create_or_update_timeslots_for_barber(barber)
            return redirect('barberEditProfileView', slug=barber.user.slug)
    else:
        form = BarberWorkingHoursForm(instance=barber)

    return render(request, 'Barber/update_working_hours.html', {'form': form})

def convert_utc_to_pacific(utc_time):
    pacific_zone = pytz.timezone('America/Los_Angeles')
    return utc_time.astimezone(pacific_zone)
'''
def update_or_create_barber_timeslots(barber):
    # Logic to update/create timeslots based on the barber's new working hours
    # For example, delete existing timeslots and create new ones
    # within the new working hours timeframe
    TimeSlot.objects.filter(barber=barber).delete()
    create_or_update_timeslots_for_barber(barber)
    '''

class OwnerSignUpView(CreateView):
    model = Owner
    form_class = OwnerSignUpForm
    template_name = 'Barber/ownerSignUp.html'
    def form_valid(self, form):
            # Save the new user first
            user = form.save()
            # Then log the user in
            login(self.request, user)

            # After successful registration and login, redirect to a specific page
            # For example, redirect to the barber's profile page
            return redirect('shopRegistration')

class ShopRegistrationView(CreateView):
    model = Shop
    form_class = ShopRegistrationForm
    template_name = 'Barber/shopRegistration.html'
    success_url = reverse_lazy('index')  # Replace with the URL to redirect after successful registration

    def form_valid(self, form):
        # Assuming the owner is the currently logged-in user
        owner = Owner.objects.get(user=self.request.user)
        shop = form.save(commit=False)
        shop.owner = owner
        shop.save()
        return super().form_valid(form)

class OwnerProfileView(DetailView):
    model = Owner
    template_name = 'Barber/ownerProfileView.html'
    context_object_name = 'owner'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg)
        return Owner.objects.filter(user__slug=slug).first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        owner = self.get_object()
        # Retrieve all shops associated with the owner
        owner_shops = Shop.objects.filter(owner=owner)
        context['owner_shops'] = owner_shops
        context['is_own_profile'] = self.request.user == owner.user
        return context

class OwnerUpdateProfile(UpdateView):
    model = User
    form_class = OwnerProfileForm
    template_name = 'Barber/ownerProfileEdit.html'

    def get_object(self):
        # Get the User instance for the logged-in owner
        return get_object_or_404(User, username=self.request.user.username, is_owner=True)

    def get_success_url(self):
        # Redirect to the owner's profile page after successful update
        return reverse_lazy('ownerProfileView', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        owner = self.get_object().owner
        context['owner_shops'] = Shop.objects.filter(owner=owner)
        return context

    def form_valid(self, form):
        self.object = form.save()

        # Fetch all shop IDs from the form data
        shop_ids = self.request.POST.getlist('shop_id')
        for shop_id in shop_ids:
            # Fetch each field's data for the specific shop
            shop = Shop.objects.get(id=shop_id)
            shop_name = self.request.POST.get(f'name_{shop_id}')
            shop_address = self.request.POST.get(f'address_{shop_id}')
            shop_description = self.request.POST.get(f'description_{shop_id}')

            # Update the shop's details
            shop.name = shop_name if shop_name else shop.name
            shop.address = shop_address if shop_address else shop.address
            shop.description = shop_description if shop_description else shop.description
            shop.save()

        return super().form_valid(form)

#    return reverse_lazy('ownerProfileView', kwargs={'slug': self.object.slug})
            
class ShopDetailView(DetailView):
    model = Shop
    template_name = 'Barber/shop_detail.html'
    context_object_name = 'shop'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shop = self.get_object()
        context['barbers'] = shop.barbers.all()
        return context

def booking_success(request):
    return render(request, 'Barber/booking_success.html')       

def inbox_view(request):
    upcoming_appointments = TimeSlot.objects.filter(booked_by=request.user, start_time__gte=timezone.now()).order_by('start_time')
    print("Upcoming Appointments:", upcoming_appointments)
    for appointment in upcoming_appointments:
        print("Appointment:", appointment, "Barber:", appointment.barber.user.get_full_name(), "Start Time:", appointment.start_time)
    
    return render(request, 'Barber/inbox.html', {'upcoming_appointments': upcoming_appointments})

def barber_appointments_view(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'barber'):
        return redirect('some_login_or_error_page')

    upcoming_appointments = TimeSlot.objects.filter(barber=request.user.barber, start_time__gte=timezone.now()).order_by('start_time')
    print("Barber's Upcoming Appointments:", upcoming_appointments)  # Debugging statement
    return render(request, 'Barber/barber_appointments.html', {'upcoming_appointments': upcoming_appointments})

class ManageServicesView(View):
    model = Service
    form_class = ServiceForm
    template_name = 'Barber/manage_services.html'
    success_url = reverse_lazy('manage_services')

    def form_valid(self, form):
        # Associate the logged-in barber with the service
        form.instance.barber = Barber.objects.get(user=self.request.user)
        return super().form_valid(form)

    def get(self, request, service_id=None):
        services = Service.objects.all()
        form = ServiceForm(instance=get_object_or_404(Service, pk=service_id)) if service_id else ServiceForm()
        return render(request, self.template_name, {'services': services, 'form': form})

    def post(self, request, service_id=None):
        # Determine the action URL based on whether the form is for adding or editing
        action_url = reverse('manage_services') if service_id is None else reverse('edit_service', args=[service_id])
        
        form = ServiceForm(request.POST, instance=get_object_or_404(Service, pk=service_id)) if service_id else ServiceForm(request.POST)

        # Check if the form is valid
        if form.is_valid():
            # Get the logged-in barber
            barber = Barber.objects.get(user=request.user)

            # Set the barber field for the service instance
            service = form.save(commit=False)
            service.barber = barber
            service.save()

            return redirect('manage_services')

        return render(request, self.template_name, {'form': form})
    

class DeleteServiceView(View):
    def post(self, request, service_id):
        service_to_delete = get_object_or_404(Service, pk=service_id)
        service_to_delete.delete()
        return HttpResponseRedirect(reverse_lazy('manage_services'))
