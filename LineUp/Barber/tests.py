from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db import transaction
from .models import User, Customer
from django.contrib.auth.forms import AuthenticationForm
from django.test import TestCase
from django.contrib.auth import get_user_model
from . import forms as barber_forms
from datetime import time

class CustomerSignUpFormTest(TestCase):
    def test_valid_signup_form(self):
        user_count_before = get_user_model().objects.count()
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = barber_forms.CustomerSignUpForm(data)
        self.assertTrue(form.is_valid())
        form.save()
        user_count_after = get_user_model().objects.count()
        self.assertEqual(user_count_after, user_count_before + 1)

    def test_invalid_signup_form(self):
        data = {
            'username': 'testuser2',
            'email': 'invalid-email',
            'password1': 'short',
            'password2': 'password_mismatch',
        }
        form = barber_forms.CustomerSignUpForm(data)
        self.assertFalse(form.is_valid())

    def test_email_already_in_use(self):
        user = get_user_model().objects.create_user(username='existinguser', email='existinguser@example.com', password='testpassword123')
        data = {
            'username': 'newuser',
            'email': 'existinguser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = barber_forms.CustomerSignUpForm(data)
        self.assertFalse(form.is_valid())

    def test_password_too_short(self):
        data = {
            'username': 'testuser3',
            'email': 'testuser3@example.com',
            'password1': 'short',
            'password2': 'short',
        }
        form = barber_forms.CustomerSignUpForm(data)
        self.assertFalse(form.is_valid())

    def test_password_mismatch(self):
        data = {
            'username': 'testuser4',
            'email': 'testuser4@example.com',
            'password1': 'testpassword123',
            'password2': 'mismatch',
        }
        form = barber_forms.CustomerSignUpForm(data)
        self.assertFalse(form.is_valid())

class CustomerLoginFormTest(TestCase):
    def test_invalid_login_form(self):
        user = get_user_model().objects.create_user(username='testuser', password='testpassword123')
        data = {
            'username': 'testuser5',
            'password': 'wrong_password',
        }
        form = barber_forms.CustomerLoginForm(data)
        self.assertFalse(form.is_valid())

    def test_blank_login_form(self):
        data = {}
        form = barber_forms.CustomerLoginForm(data)
        self.assertFalse(form.is_valid())

class BarberSignUpFormTest(TestCase):
    def test_valid_signup_form(self):
        user_count_before = get_user_model().objects.count()
        data = {
            'username': 'testbarber',
            'email': 'testbarber@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'first_name': 'Barry',
            'last_name': 'Barber',
        }
        form = barber_forms.BarberSignUpForm(data)
        self.assertTrue(form.is_valid())
        form.save()
        user_count_after = get_user_model().objects.count()
        self.assertEqual(user_count_after, user_count_before + 1)

        user = get_user_model().objects.get(username='testbarber')
        self.assertEqual(user.first_name, 'Barry')
        self.assertEqual(user.last_name, 'Barber')
        self.assertTrue(user.is_barber)

    def test_invalid_signup_form(self):
        data = {
            'username': 'testbarber2',
            'email': 'invalid-email',
            'password1': 'short',
            'password2': 'password_mismatch',
            'first_name': 'Barry',
            'last_name': 'Barber',
        }
        form = barber_forms.BarberSignUpForm(data)
        self.assertFalse(form.is_valid())

    def test_email_already_in_use(self):
        get_user_model().objects.create_user(username='existingbarber', email='existingbarber@example.com', password='testpassword123')
        data = {
            'username': 'newbarber',
            'email': 'existingbarber@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'first_name': 'Barry',
            'last_name': 'Barber',
        }
        form = barber_forms.BarberSignUpForm(data)
        self.assertFalse(form.is_valid())

    def test_password_mismatch(self):
        data = {
            'username': 'testbarber3',
            'email': 'testbarber3@example.com',
            'password1': 'testpassword123',
            'password2': 'mismatch',
            'first_name': 'Barry',
            'last_name': 'Barber',
        }
        form = barber_forms.BarberSignUpForm(data)
        self.assertFalse(form.is_valid())

class BarberProfileFormTest(TestCase):
    def test_valid_profile_form(self):
        user = get_user_model().objects.create_user(username='testbarber', password='testpassword123')
        data = {
            'first_name': 'Barry',
            'last_name': 'Barber',
            'phone_num': '1234567890',
        }
        form = barber_forms.BarberProfileForm(data, instance=user)
        self.assertTrue(form.is_valid())
        form.save()
        updated_user = get_user_model().objects.get(pk=user.pk)
        self.assertEqual(updated_user.first_name, 'Barry')
        self.assertEqual(updated_user.last_name, 'Barber')
        self.assertEqual(updated_user.phone_num, '1234567890')

    def test_blank_profile_form(self):
        data = {}
        user = get_user_model().objects.create_user(username='testbarber', password='testpassword123')
        form = barber_forms.BarberProfileForm(data, instance=user)
        self.assertTrue(form.is_valid())
        form.save()
        updated_user = get_user_model().objects.get(pk=user.pk)
        self.assertEqual(updated_user.first_name, '')
        self.assertEqual(updated_user.last_name, '')
        self.assertEqual(updated_user.phone_num, '')

class ReviewFormTest(TestCase):
    def test_valid_review_form(self):
        barber = barber_forms.Barber.objects.create(user=get_user_model().objects.create_user(username='testbarber', password='testpassword123'))
        customer = Customer.objects.create(user=get_user_model().objects.create_user(username='testcustomer', password='testpassword123'))
        data = {
            'content': 'Great service!',
            'rating': 5,
        }
        form = forms.ReviewForm(data)
        self.assertTrue(form.is_valid())
        review = form.save(commit=False)
        review.barber = barber
        review.customer = customer 
        review.save()

        self.assertEqual(review.content, 'Great service!')
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.barber, barber)
        self.assertEqual(review.customer, customer)

    def test_invalid_review_form(self):
        data = {
            'content': '',  # Empty content
            'rating': 6,  # Invalid rating
        }
        form = barber_forms.ReviewForm(data)
        self.assertFalse(form.is_valid())

class BarberWorkingHoursFormTest(TestCase):
    def test_valid_working_hours_form(self):
        barber = barber_forms.Barber.objects.create(user=get_user_model().objects.create_user(username='testbarber', password='testpassword123'))
        data = {
            'work_start_time': '08:00',
            'work_end_time': '17:00',
        }
        form = barber_forms.BarberWorkingHoursForm(data, instance=barber)
        self.assertTrue(form.is_valid())
        form.save()
        updated_barber = barber_forms.Barber.objects.get(pk=barber.pk)
        self.assertEqual(updated_barber.work_start_time, time(8, 0))  
        self.assertEqual(updated_barber.work_end_time, time(17, 0))  

    def test_invalid_working_hours_form(self):
        data = {
            'work_start_time': '25:00',  # Invalid time
            'work_end_time': '17:00',
        }
        barber = barber_forms.Barber.objects.create(user=get_user_model().objects.create_user(username='testbarber', password='testpassword123'))
        form = barber_forms.BarberWorkingHoursForm(data, instance=barber)
        self.assertFalse(form.is_valid())
