from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db import transaction
from .models import User, Customer
from django.contrib.auth.forms import AuthenticationForm

class CustomerSignUpForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        min_length=6,  # Set a custom minimum password length
        error_messages={
            'min_length': 'Password must be at least 6 characters long.'
        }
    )

    email = forms.EmailField(
        label="Email",
        error_messages={
            'invalid': 'Enter a valid email address.',
        }
    )

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

class CustomerLoginForm(AuthenticationForm):
    '''
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # You can customize form widgets or labels if necessary
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'
    
class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    phone_num = forms.CharField(max_length=12, required=False)

    class Meta:
        model = User
        fields = ['profile_pic', 'first_name', 'last_name', 'phone_num']

    def save(self, commit=True):
        user = super(ProfileForm, self).save(commit=False)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.phone_num = self.cleaned_data.get('phone_num')
        user.profile_pic = self.cleaned_data.get('profile_pic')

        if commit:
            user.save()
        return user






