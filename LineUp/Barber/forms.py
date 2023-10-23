from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User, Customer

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

    
