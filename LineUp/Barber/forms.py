from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db import transaction
from .models import User, Customer, Barber, Review, Shop, Owner, Service
from django.contrib.auth.forms import AuthenticationForm
    

class CustomerSignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput, validators=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial values for the username and email fields
        if self.instance:
            self.fields['username'].initial = self.instance.username
            self.fields['email'].initial = self.instance.email

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()

        # Check for an existing UserProfile or create a new one
        try:
            profile = Customer.objects.get(user=user)
        except Customer.DoesNotExist:
            profile = Customer(user=user)

        # Now you can populate the UserProfile fields from the form
        profile.username = self.cleaned_data['username']
        profile.email = self.cleaned_data['email']

        profile.save()
        return user
     

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # You can customize form widgets or labels if necessary
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'
    
class CustomerProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    phone_num = forms.CharField(max_length=12, required=False)

    class Meta:
        model = User
        fields = ['profile_pic', 'first_name', 'last_name', 'phone_num']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.phone_num = self.cleaned_data.get('phone_num')

        if 'profile_pic' in self.changed_data:
            user.profile_pic = self.cleaned_data.get('profile_pic')

        if commit:
            user.save()
        return user

#-------------------------------------------------------------------------------
class BarberSignUpForm(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput, validators=[])
    email = forms.EmailField(label="Email")
    affiliation_code = forms.CharField(label="Affiliation Code", max_length=10, required=False, help_text="Enter your shop's affiliation code if you have one.")
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(label="Email")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'affiliation_code')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_barber = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()

        # Create or get a Barber profile
        profile, created = Barber.objects.get_or_create(user=user)
        profile.save()

        # If an affiliation code is provided, link the barber to the shop
        affiliation_code = self.cleaned_data.get('affiliation_code')
        if affiliation_code:
            try:
                shop = Shop.objects.get(affiliation_code=affiliation_code)
                profile.shops.add(shop)
            except Shop.DoesNotExist:
                pass  # If the shop doesn't exist, ignore the code

        return user


class BarberProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    phone_num = forms.CharField(max_length=12, required=False)
    affiliation_code = forms.CharField(max_length=10, required=False, help_text="Enter your shop's affiliation code if you have one.")

    class Meta:
        model = User
        fields = ['profile_pic', 'first_name', 'last_name', 'phone_num', 'affiliation_code']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.phone_num = self.cleaned_data.get('phone_num')

        if 'profile_pic' in self.changed_data:
            user.profile_pic = self.cleaned_data.get('profile_pic')

        if commit:
            user.save()

            # Handle the affiliation code
            affiliation_code = self.cleaned_data.get('affiliation_code')
            if affiliation_code:
                try:
                    shop = Shop.objects.get(affiliation_code=affiliation_code)
                    barber_profile = Barber.objects.get(user=user)
                    barber_profile.shops.add(shop)
                except Shop.DoesNotExist:
                    print("Shop with provided code does not exist")  # You might want to handle this more gracefully

        return user
            
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content', 'rating']
        # Add other fields and widgets as needed


class BarberWorkingHoursForm(forms.ModelForm):
    class Meta:
        model = Barber
        fields = ['work_start_time', 'work_end_time']


class OwnerSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(label="Email", required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_owner = True
        user.email = self.cleaned_data.get('email')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')

        if commit:
            user.save()
            # Create the Owner profile
            Owner.objects.create(user=user)

        return user

class ShopRegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True, max_length=12)

    class Meta:
        model = Shop
        fields = ['name', 'address', 'email', 'phone_number', 'description']

    def __init__(self, *args, **kwargs):
        super(ShopRegistrationForm, self).__init__(*args, **kwargs)
        # Customize your form initialization or add extra fields here if needed

class OwnerProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    phone_num = forms.CharField(max_length=12, required=False)

    class Meta:
        model = User
        fields = ['profile_pic', 'first_name', 'last_name', 'phone_num']

    def __init__(self, *args, **kwargs):
        super(OwnerProfileForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Set the initial values for the form fields
            self.fields['first_name'].initial = self.instance.first_name
            self.fields['last_name'].initial = self.instance.last_name
            self.fields['phone_num'].initial = self.instance.phone_num

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.phone_num = self.cleaned_data.get('phone_num')

        if 'profile_pic' in self.changed_data:
            user.profile_pic = self.cleaned_data.get('profile_pic')

        if commit:
            user.save()
        return user
        
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description', 'price', 'duration']

    def save(self, barber, commit=True):
        service = super().save(commit=False)
        service.barber = barber  # Set the barber for the service
        service.description = self.description
        service.title = self.title
        service.price = self.price
        service.duration = self.duration
        service.save()
        
        return service


    def clean_duration(self):
        # Convert the duration to the desired format (in minutes)
        duration = self.cleaned_data.get('duration')
        return duration  # Keep it in minutes

    def save(self, commit=True):
        # Convert the duration to seconds before saving to the database
        self.instance.duration = self.cleaned_data.get('duration') * 60
        return super().save(commit)
