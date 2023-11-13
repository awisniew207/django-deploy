from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db import transaction
from .models import User, Customer, Barber, Review
from django.contrib.auth.forms import AuthenticationForm

class CustomerSignUpForm(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput, validators=[])

    email = forms.EmailField(label="Email")

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
        user = super(CustomerProfileForm, self).save(commit=False)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.phone_num = self.cleaned_data.get('phone_num')
        user.profile_pic = self.cleaned_data.get('profile_pic')

        if commit:
            user.save()
        return user

#-------------------------------------------------------------------------------
class BarberSignUpForm(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput, validators=[])

    email = forms.EmailField(label="Email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial values for the username and email fields
        if self.instance:
            self.fields['username'].initial = self.instance.username
            self.fields['email'].initial = self.instance.email
            self.fields['first_name'].initial = self.instance.first_name
            self.fields['last_name'].initial = self.instance.last_name

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email','first_name', 'last_name',)

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_barber = True
        user.save()

        # Check for an existing UserProfile or create a new one
        try:
            profile = Barber.objects.get(user=user)
        except Barber.DoesNotExist:
            profile = Barber(user=user)

        # Now you can populate the UserProfile fields from the form
        profile.username = self.cleaned_data['username']
        profile.email = self.cleaned_data['email']
        profile.first_name = self.cleaned_data['first_name']
        profile.last_name = self.cleaned_data['last_name']

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





