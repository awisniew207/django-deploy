from django.test import TestCase
from django.contrib.auth import get_user_model
from .forms import CustomerSignUpForm, CustomerLoginForm

class CustomerSignUpFormTest(TestCase):
    def test_valid_signup_form(self):
        user_count_before = get_user_model().objects.count()
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = CustomerSignUpForm(data)
        self.assertTrue(form.is_valid())
        form.save()
        user_count_after = get_user_model().objects.count()
        self.assertEqual(user_count_after, user_count_before + 1)

    def test_invalid_signup_form(self):
        data = {
            'username': 'testuser',
            'email': 'invalid-email',
            'password1': 'short',
            'password2': 'password_mismatch',
        }
        form = CustomerSignUpForm(data)
        self.assertFalse(form.is_valid())

class CustomerLoginFormTest(TestCase):
    def test_valid_login_form(self):
        user = get_user_model().objects.create_user(username='testuser', password='testpassword123')
        data = {
            'username': 'testuser',
            'password': 'testpassword123',
        }
        form = CustomerLoginForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_login_form(self):
        user = get_user_model().objects.create_user(username='testuser', password='testpassword123')
        data = {
            'username': 'testuser',
            'password': 'wrong_password',
        }
        form = CustomerLoginForm(data)
        self.assertFalse(form.is_valid())

    def test_blank_login_form(self):
        data = {}
        form = CustomerLoginForm(data)
        self.assertFalse(form.is_valid())
