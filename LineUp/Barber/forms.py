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


class BarberSignUpForm(UserCreationForm):
    # Add first_name and last_name fields
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(label="Email")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['username'].initial = self.instance.username
            self.fields['email'].initial = self.instance.email

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

        return user

class BarberProfileForm(forms.ModelForm):
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

        # Only update the profile_pic if a new picture is provided
        if 'profile_pic' in self.changed_data:
            user.profile_pic = self.cleaned_data.get('profile_pic')

        if commit:
            user.save()
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
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput, validators=[])
    email = forms.EmailField(label="Email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize username and email if instance is available
        if self.instance:
            self.fields['username'].initial = self.instance.username
            self.fields['email'].initial = self.instance.email

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_owner = True
        user.save()

        # Create or get a Barber profile
        profile, created = Owner.objects.get_or_create(user=user)
        profile.first_name = self.cleaned_data.get('first_name', '')
        profile.last_name = self.cleaned_data.get('last_name', '')
        profile.save()

        return user

class ShopRegistrationForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'address', 'description']

    def __init__(self, *args, **kwargs):
        super(ShopRegistrationForm, self).__init__(*args, **kwargs)
        # Customize your form initialization or add extra fields here if needed

class OwnerProfileForm(forms.ModelForm):
    shop_choices = [(shop.id, shop.name) for shop in Shop.objects.all()]
    shop = forms.ChoiceField(choices=shop_choices, required=False)

    class Meta:
        model = Owner
        fields = ['user', 'shop']

    def __init__(self, *args, **kwargs):
        super(OwnerProfileForm, self).__init__(*args, **kwargs)
        # Ensure that instance is an Owner instance and not a User instance
        if self.instance and hasattr(self.instance, 'owned_shop'):
            # Assuming the Owner model has a relation to a Shop
            self.fields['shop'].initial = self.instance.owned_shop.id if self.instance.owned_shop else None

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description', 'price', 'duration']

    def clean_duration(self):
        # Convert the duration to the desired format (in minutes)
        duration = self.cleaned_data.get('duration')
        return duration  # Keep it in minutes

    def save(self, commit=True):
        # Convert the duration to seconds before saving to the database
        self.instance.duration = self.cleaned_data.get('duration') * 60
        return super().save(commit)
