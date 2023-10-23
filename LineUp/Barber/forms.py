from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User

class CustomerSignUpForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        min_length=6,  # Set a custom minimum password length
        error_messages={
            'min_length': 'Password must be at least 6 characters long.'
        }
    )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        customer = Customer.objects.create(user=user)
        return user
