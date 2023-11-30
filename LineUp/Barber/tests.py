from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
import datetime
from .forms import (
    CustomerSignUpForm,
    LoginForm,
    CustomerProfileForm,
    BarberSignUpForm,
    BarberProfileForm,
    ReviewForm,
    BarberWorkingHoursForm,
    OwnerSignUpForm,
    ShopRegistrationForm,
    OwnerProfileForm,
    ServiceForm,
)
from .models import Customer, Barber, Review, Shop, Owner, Service


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
            'username': 'testuser2',
            'email': 'invalid-email',
            'password1': 'short',
            'password2': 'password_mismatch',
        }
        form = CustomerSignUpForm(data)
        self.assertFalse(form.is_valid())

    def test_signup_form_saves_user_and_customer_profile(self):
        data = {
            'username': 'testuser3',
            'email': 'testuser3@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = CustomerSignUpForm(data)
        self.assertTrue(form.is_valid())
        user = form.save()

        self.assertTrue(user.is_customer)
        self.assertEqual(user.username, 'testuser3')
        self.assertEqual(user.email, 'testuser3@example.com')
        # Add more assertions for customer profile fields


class LoginFormTest(TestCase):
    def test_valid_login_form(self):
        user = get_user_model().objects.create_user(username='testuser', password='testpassword123')
        data = {
            'username': 'testuser4',
            'password': 'testpassword123',
        }
        form = LoginForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_login_form(self):
        data = {
            'username': 'testuser5',
            'password': 'wrong_password',
        }
        form = LoginForm(data)
        self.assertFalse(form.is_valid())


class CustomerProfileFormTest(TestCase):
    def test_valid_customer_profile_form(self):
        user = get_user_model().objects.create_user(username='testuser', password='testpassword123')
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_num': '1234567890',
        }
        form = CustomerProfileForm(data, instance=user)
        self.assertTrue(form.is_valid())
        form.save()
        updated_user = get_user_model().objects.get(pk=user.pk)
        self.assertEqual(updated_user.first_name, 'John')
        self.assertEqual(updated_user.last_name, 'Doe')
        self.assertEqual(updated_user.phone_num, '1234567890')

    def test_blank_customer_profile_form(self):
        data = {}
        user = get_user_model().objects.create_user(username='testuser', password='testpassword123')
        form = CustomerProfileForm(data, instance=user)
        self.assertTrue(form.is_valid())
        form.save()
        updated_user = get_user_model().objects.get(pk=user.pk)
        self.assertEqual(updated_user.first_name, '')
        self.assertEqual(updated_user.last_name, '')
        self.assertEqual(updated_user.phone_num, '')


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
        form = BarberSignUpForm(data)
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
        form = BarberSignUpForm(data)
        self.assertFalse(form.is_valid())

    # Add more tests for BarberSignUpForm as needed


class BarberProfileFormTest(TestCase):
    def test_valid_profile_form(self):
        user = get_user_model().objects.create_user(username='testbarber', password='testpassword123')
        data = {
            'first_name': 'Barry',
            'last_name': 'Barber',
            'phone_num': '1234567890',
        }
        form = BarberProfileForm(data, instance=user)
        self.assertTrue(form.is_valid())
        form.save()
        updated_user = get_user_model().objects.get(pk=user.pk)
        self.assertEqual(updated_user.first_name, 'Barry')
        self.assertEqual(updated_user.last_name, 'Barber')
        self.assertEqual(updated_user.phone_num, '1234567890')

    def test_blank_profile_form(self):
        data = {}
        user = get_user_model().objects.create_user(username='testbarber', password='testpassword123')
        form = BarberProfileForm(data, instance=user)
        self.assertTrue(form.is_valid())
        form.save()
        updated_user = get_user_model().objects.get(pk=user.pk)
        self.assertEqual(updated_user.first_name, '')
        self.assertEqual(updated_user.last_name, '')
        self.assertEqual(updated_user.phone_num, '')

    def test_profile_form_links_to_shop_with_affiliation_code(self):
        shop = Shop.objects.create(name='Test Shop', affiliation_code='test123')
        data = {
            'first_name': 'Barry',
            'last_name': 'Barber',
            'phone_num': '1234567890',
            'affiliation_code': 'test123',
        }
        user = get_user_model().objects.create_user(username='testbarber', password='testpassword123')
        form = BarberProfileForm(data, instance=user)
        self.assertTrue(form.is_valid())
        form.save()
        updated_user = get_user_model().objects.get(pk=user.pk)
        barber_profile = Barber.objects.get(user=updated_user)
        self.assertTrue(shop in barber_profile.shops.all())

    # Add more tests for BarberProfileForm as needed


class ReviewFormTest(TestCase):
    def test_valid_review_form(self):
        barber = Barber.objects.create(user=get_user_model().objects.create_user(username='testbarber', password='testpassword123'))
        customer = Customer.objects.create(user=get_user_model().objects.create_user(username='testcustomer', password='testpassword123'))
        data = {
            'content': 'Great service!',
            'rating': 5,
        }
        form = ReviewForm(data)
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
        form = ReviewForm(data)
        self.assertFalse(form.is_valid())

    # Add more tests for ReviewForm as needed


class BarberWorkingHoursFormTest(TestCase):
    def test_valid_working_hours_form(self):
        barber = Barber.objects.create(user=get_user_model().objects.create_user(username='testbarber', password='testpassword123'))
        data = {
            'work_start_time': '08:00',
            'work_end_time': '17:00',
        }
        form = BarberWorkingHoursForm(data, instance=barber)
        self.assertTrue(form.is_valid())
        form.save()
        updated_barber = Barber.objects.get(pk=barber.pk)
        self.assertEqual(updated_barber.work_start_time, timezone.datetime.strptime('08:00', '%H:%M').time())
        self.assertEqual(updated_barber.work_end_time, timezone.datetime.strptime('17:00', '%H:%M').time())

    def test_invalid_working_hours_form(self):
        data = {
            'work_start_time': '25:00',  # Invalid time
            'work_end_time': '17:00',
        }
        barber = Barber.objects.create(user=get_user_model().objects.create_user(username='testbarber', password='testpassword123'))
        form = BarberWorkingHoursForm(data, instance=barber)
        self.assertFalse(form.is_valid())

    # Add more tests for BarberWorkingHoursForm as needed


class OwnerSignUpFormTest(TestCase):
    def test_valid_owner_signup_form(self):
        user_count_before = get_user_model().objects.count()
        data = {
            'username': 'testowner',
            'email': 'testowner@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'first_name': 'Owner',
            'last_name': 'Test',
        }
        form = OwnerSignUpForm(data)
        self.assertTrue(form.is_valid())
        form.save()
        user_count_after = get_user_model().objects.count()
        self.assertEqual(user_count_after, user_count_before + 1)

        user = get_user_model().objects.get(username='testowner')
        self.assertTrue(user.is_owner)
        self.assertEqual(user.first_name, 'Owner')
        self.assertEqual(user.last_name, 'Test')
        # Add more assertions for owner profile fields

    def test_invalid_owner_signup_form(self):
        data = {
            'username': 'testowner2',
            'email': 'invalid-email',
            'password1': 'short',
            'password2': 'password_mismatch',
            'first_name': 'Owner',
            'last_name': 'Test',
        }
        form = OwnerSignUpForm(data)
        self.assertFalse(form.is_valid())

    # Add more tests for OwnerSignUpForm as needed


class ShopRegistrationFormTest(TestCase):
    def test_valid_shop_registration_form(self):
        data = {
            'name': 'Test Shop',
            'address': '123 Main St',
            'email': 'testshop@example.com',
            'phone_number': '1234567890',
            'description': 'A test shop',
        }
        form = ShopRegistrationForm(data)
        self.assertTrue(form.is_valid())
        form.save()

        shop = Shop.objects.get(name='Test Shop')
        self.assertEqual(shop.address, '123 Main St')
        self.assertEqual(shop.email, 'testshop@example.com')
        self.assertEqual(shop.phone_number, '1234567890')
        self.assertEqual(shop.description, 'A test shop')

    def test_invalid_shop_registration_form(self):
        data = {
            'name': 'Test Shop',
            'address': '123 Main St',
            'email': 'invalid-email',
            'phone_number': 'invalid-phone',
            'description': 'A test shop',
        }
        form = ShopRegistrationForm(data)
        self.assertFalse(form.is_valid())

    # Add more tests for ShopRegistrationForm as needed


class OwnerProfileFormTest(TestCase):
    def test_valid_owner_profile_form(self):
        user = get_user_model().objects.create_user(username='testowner', password='testpassword123')
        data = {
            'first_name': 'Owner',
            'last_name': 'Test',
            'phone_num': '1234567890',
        }
        form = OwnerProfileForm(data, instance=user)
        self.assertTrue(form.is_valid())
        form.save()
        updated_user = get_user_model().objects.get(pk=user.pk)
        self.assertEqual(updated_user.first_name, 'Owner')
        self.assertEqual(updated_user.last_name, 'Test')
        self.assertEqual(updated_user.phone_num, '1234567890')

    # Add more tests for OwnerProfileForm as needed


class ServiceFormTest(TestCase):
    def test_valid_service_form(self):
        barber = Barber.objects.create(user=get_user_model().objects.create_user(username='testbarber', password='testpassword123'))
        data = {
            'title': 'Haircut',
            'description': 'A standard haircut',
            'price': 20.00,
            'duration': 30,
        }
        form = ServiceForm(data)
        self.assertTrue(form.is_valid())
        form.save(barber)

        service = Service.objects.get(title='Haircut')
        self.assertEqual(service.description, 'A standard haircut')
        self.assertEqual(service.price, 20.00)
        self.assertEqual(service.duration, datetime.timedelta(seconds=1800))

    def test_invalid_service_form(self):
        data = {
            'title': 'Haircut',
            'description': 'A standard haircut',
            'price': -10.00,  # Invalid price
            'duration': 'invalid-duration',  # Invalid duration
        }
        barber = Barber.objects.create(user=get_user_model().objects.create_user(username='testbarber', password='testpassword123'))
        form = ServiceForm(data)
        self.assertFalse(form.is_valid())

    # Add more tests for ServiceForm as needed